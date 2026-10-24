#!/usr/bin/env node
/**
 * Puter Pool — สลับบัญชี Puter อัตโนมัติ
 *
 * ยิงตรงไป Puter API (api.puter.com/drivers/call) เพราะ bridge local ผูก token ตายตัว
 * เมื่อบัญชีหนึ่งเจอ insufficient_funds / rate limit → สลับตัวถัดไปทันที
 *
 * ใช้:
 *   node pool.js health                        # เช็กเครดิตทุกบัญชี (ยิง chat จริง)
 *   node pool.js chat "ข้อความ"                 # ถามสลี่ (สลับบัญชีอัตโนมัติ)
 *   node pool.js chat --model gpt-5.4 "..."
 *
 * token เก็บใน tokens.json (chmod 600) — ห้าม commit
 */

const fs = require('fs');
const path = require('path');

const DIR = __dirname;
const TOKENS_FILE = path.join(DIR, 'tokens.json');
const STATE_FILE = path.join(DIR, '.pool-state.json');
const API = 'https://api.puter.com';
const DEFAULT_MODEL = process.env.SALLY_MODEL || 'gpt-5.4';

const log = (...a) => process.stderr.write(a.join(' ') + '\n');

// ---------- tokens ----------
function loadTokens() {
  if (!fs.existsSync(TOKENS_FILE)) {
    log(`❌ ไม่พบ ${TOKENS_FILE} — ดูวิธีสร้างใน README.md แล้ว chmod 600`);
    process.exit(2);
  }
  let raw;
  try { raw = JSON.parse(fs.readFileSync(TOKENS_FILE, 'utf8')); }
  catch (e) { log(`❌ tokens.json อ่านไม่ได้: ${e.message}`); process.exit(2); }
  const accounts = (Array.isArray(raw) ? raw : raw.accounts) || [];
  const ok = accounts.filter(a => a && typeof a.token === 'string' && a.token.length > 20);
  if (!ok.length) { log('❌ tokens.json ต้องมี accounts[] อย่างน้อย 1 บัญชีที่ใช้ได้'); process.exit(2); }
  return ok;
}

function loadState() {
  try { return JSON.parse(fs.readFileSync(STATE_FILE, 'utf8')); }
  catch { return { dead: {} }; }
}
function saveState(s) {
  try { fs.writeFileSync(STATE_FILE, JSON.stringify(s, null, 2)); } catch {}
}

function orderAccounts(accounts, state) {
  return [
    ...accounts.filter(a => !state.dead[a.name]),
    ...accounts.filter(a => state.dead[a.name]),
  ];
}

// ---------- Puter API (ยิงตรง) ----------
async function puterChat(acc, messages, model) {
  const t0 = Date.now();
  try {
    const r = await fetch(`${API}/drivers/call`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${acc.token}`,
      },
      body: JSON.stringify({
        interface: 'puter-chat-completion',
        method: 'complete',
        args: { model, messages },
      }),
      signal: AbortSignal.timeout(120000),
    });
    const text = await r.text();
    let data;
    try { data = JSON.parse(text); } catch { data = { raw: text }; }
    return { status: r.status, data, ms: Date.now() - t0 };
  } catch (e) {
    return { status: 0, data: { error: e.name === 'TimeoutError' ? 'timeout' : e.message }, ms: Date.now() - t0 };
  }
}

// error ที่ควรสลับบัญชี
function shouldSwitch(status, data) {
  const code = (data && data.code) || '';
  const msg = JSON.stringify(data || '').toLowerCase();
  if (status === 429 || status === 402 || status === 403) return true;
  if (/insufficient_funds|insufficient|quota|rate.?limit|usage.?limit|unavailable|credits/.test(code + ' ' + msg)) return true;
  return false;
}

// ดึงข้อความตอบจาก response ของ Puter (รูปทรงต่างจาก OpenAI)
function extractContent(data) {
  const r = data && (data.result || data);
  if (!r) return null;
  // รูปทรง OpenAI-like
  if (r.choices && r.choices[0]) {
    const m = r.choices[0].message;
    if (m && typeof m.content === 'string') return m.content;
    if (typeof r.choices[0].text === 'string') return r.choices[0].text;
  }
  if (typeof r.message === 'string') return r.message;
  if (r.message && typeof r.message.content === 'string') return r.message.content;
  if (typeof r.text === 'string') return r.text;
  if (typeof r.content === 'string') return r.content;
  return null;
}

// ---------- commands ----------
async function cmdHealth(accounts) {
  log(`🔍 ตรวจเครดิต ${accounts.length} บัญชี (ยิง chat จริง)...\n`);
  const state = loadState();
  let alive = 0;
  for (const acc of accounts) {
    const { status, data, ms } = await puterChat(acc, [{ role: 'user', content: 'hi' }], DEFAULT_MODEL);
    const content = extractContent(data);
    if (status === 200 && content !== null) {
      alive++;
      delete state.dead[acc.name];
      console.log(`✅ ${(acc.name || '?').padEnd(14)} ${ms}ms  ${String(content).slice(0, 40)}`);
    } else if (shouldSwitch(status, data)) {
      state.dead[acc.name] = Date.now();
      console.log(`💀 ${(acc.name || '?').padEnd(14)} ${ms}ms  หมดเครดิต/โดน limit (${data.code || status})`);
    } else {
      console.log(`⚠️  ${(acc.name || '?').padEnd(14)} ${ms}ms  ${status} ${JSON.stringify(data).slice(0, 70)}`);
    }
  }
  saveState(state);
  console.log(`\n📊 ใช้ได้ ${alive}/${accounts.length}`);
  return alive > 0;
}

async function cmdChat(accounts, argv) {
  let model = DEFAULT_MODEL;
  const rest = [];
  for (let i = 0; i < argv.length; i++) {
    if (argv[i] === '--model' && argv[i + 1]) model = argv[++i];
    else rest.push(argv[i]);
  }
  const prompt = rest.join(' ');
  if (!prompt) { log('❌ ต้องใส่ข้อความ'); process.exit(2); }

  const state = loadState();
  const ordered = orderAccounts(accounts, state);
  const messages = [{ role: 'user', content: prompt }];
  const errs = [];

  for (const acc of ordered) {
    const { status, data } = await puterChat(acc, messages, model);
    const content = extractContent(data);
    if (status === 200 && content !== null) {
      delete state.dead[acc.name];
      state.lastGood = acc.name;
      saveState(state);
      process.stdout.write(content + '\n');
      log(`[บัญชี: ${acc.name} | โมเดล: ${model}]`);
      return 0;
    }
    if (shouldSwitch(status, data)) {
      state.dead[acc.name] = Date.now();
      saveState(state);
      errs.push(`${acc.name}(dead)`);
      log(`⚠️  ${acc.name} หมด → สลับ`);
      continue;
    }
    // error เชิงโค้ด (model ผิด ฯลฯ) ไม่สลับ
    log(`❌ ${acc.name}: ${status} ${JSON.stringify(data).slice(0, 200)}`);
    return 1;
  }
  log(`❌ ทุกบัญชีหมด: ${errs.join(', ')}`);
  return 1;
}

// ---------- main ----------
(async () => {
  const [cmd, ...argv] = process.argv.slice(2);
  if (!cmd || cmd === 'help' || cmd === '--help') {
    log('ใช้: node pool.js <health|chat> [--model M] [args]');
    process.exit(0);
  }
  const accounts = loadTokens();
  if (cmd === 'health') process.exit((await cmdHealth(accounts)) ? 0 : 1);
  if (cmd === 'chat') process.exit(await cmdChat(accounts, argv));
  log(`❌ ไม่รู้จักคำสั่ง: ${cmd}`);
  process.exit(2);
})().catch(e => { log('💥 ' + e.message); process.exit(1); });
