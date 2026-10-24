#!/usr/bin/env python3
"""Auto-generate Skillhub จาก SKILL.md ทุกไฟล์ — ฐานสกิลของสลี่"""
import os, re, json
from datetime import datetime

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'skills')
OUT  = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'index.html')

# หมวดหมู่ตาม prefix / keyword
CATEGORIES = [
    ('◆ สร้าง & เขียนโค้ด', ['implement', 'implement-spec', 'tdd', 'diagnosing-bugs', 'code-review',
        'code-reviewer', 'improve-codebase-architecture', 'codebase-design', 'migrate-to-shoehorn',
        'setup-pre-commit', 'setup-ts-deep-modules', 'prototype', 'git-guardrails-claude-code',
        'github', 'code-assistant', 'code-quality-assistant', 'codex-engineer']),
    ('◈ ออกแบบ & สร้างเว็บ', ['frontend-design', 'canvas-design', 'algorithmic-art', 'webapp-testing',
        'theme-factory', 'image-generation', 'ui-ux-designer', 'web-artifacts-builder',
        'browser-slilelo', 'terminal-css-modifier']),
    ('▤ เอกสาร & งานสำนักงาน', ['docx', 'pdf', 'pptx', 'xlsx', 'doc-coauthoring', 'internal-comms',
        'to-questionnaire', 'to-spec', 'to-tickets', 'pr', 'incident-playbook-automator']),
    ('◉ ค้นคว้า & วิเคราะห์', ['research', 'browser-research', 'domain-modeling', 'grilling',
        'grill-me', 'grill-with-docs', 'discernment-nudge', 'wait-what', 'wayfinder',
        'triage', 'retro', 'night-watchman']),
    ('▲ คิดเชิงกลยุทธ์', ['first-principles', 'impossible-mode', 'future-builder', 'elon-protocol',
        'boss-omni-godmode', 'chief-of-staff', 'ask-matt', 'mcp-builder', 'mcp-orchestrator']),
    ('⬡ ระบบ & ความรู้', ['knowledge-wiki', 'handoff', 'claude-handoff', 'wizard', 'eval-harness',
        'brand-manager', 'brand-guidelines', 'brand-compliance-guardian', 'academy-guide',
        'learning-license', 'skill-creator']),
    ('○ อื่น ๆ', ['film-making', 'live-slot-fetch', 'scaffold-exercises', 'setup-matt-pocock-skills',
        'slack-gif-creator', 'slot-game-simulator', 'teach', 'template-skill', 'writing-beats',
        'writing-for-agents', 'writing-fragments', 'writing-shape', 'loop-me', 'mix-mode',
        'claude-api', 'openclaw-tavily-search', 'pip-skill', 'short-video-creator']),
]

def parse_skill(path):
    txt = open(path, encoding='utf-8', errors='ignore').read()
    m = re.match(r'^---\s*\n(.*?)\n---', txt, re.S)
    nm = os.path.basename(os.path.dirname(path))
    desc = ''
    if m:
        nm_m = re.search(r'^name:\s*(.+)$', m.group(1), re.M)
        desc_m = re.search(r'^description:\s*(.+)$', m.group(1), re.M)
        if nm_m: nm = nm_m.group(1).strip()
        if desc_m: desc = desc_m.group(1).strip()
    if not desc:
        body = txt[m.end()+1:] if m else txt
        lines = [l.strip() for l in body.splitlines() if l.strip() and not l.strip().startswith('#')]
        desc = lines[0] if lines else ''
    desc = re.sub(r'&quot;|&#39;', '"', desc)
    desc = re.sub(r'<[^>]+>', '', desc)
    desc = re.sub(r'\s+', ' ', desc).strip()
    return {'dir': os.path.basename(os.path.dirname(path)), 'name': nm, 'desc': desc[:230]}

skills = []
for d in sorted(os.listdir(ROOT)):
    p = os.path.join(ROOT, d, 'SKILL.md')
    if os.path.isfile(p):
        skills.append(parse_skill(p))

assigned = set()
groups = []
for title, names in CATEGORIES:
    items = [s for s in skills if s['dir'] in names]
    for i in items: assigned.add(i['dir'])
    groups.append({'title': title, 'items': items})
# fallback: สกิลที่ยังไม่มีหมวด
leftover = [s for s in skills if s['dir'] not in assigned]
if leftover:
    groups.append({'title': '○ ยังไม่จัดหมวด', 'items': leftover})

html = f'''<!DOCTYPE html>
<html lang="th">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="generator" content="skillhub build.py — สลี่ auto-generated จาก SKILL.md">
<title>Skillhub · ฐานสกิลของสลี่ ({len(skills)} ความสามารถ)</title>
<style>
:root {{
  --bg:#08070c; --bg2:#0e0c16; --violet:#d5c6e0; --violet-dim:#a892b8;
  --accent:#9b7fd4; --accent2:#6ee7b7; --line:rgba(213,198,224,.12);
  --glass:rgba(255,255,255,.035); --glass2:rgba(255,255,255,.06);
  --font:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',system-ui,sans-serif;
}}
*{{margin:0;padding:0;box-sizing:border-box}}
html{{scroll-behavior:smooth}}
body{{background:var(--bg);color:var(--violet);font-family:var(--font);line-height:1.6;overflow-x:hidden;-webkit-font-smoothing:antialiased}}
body::before{{content:'';position:fixed;inset:0;pointer-events:none;z-index:0;background:radial-gradient(ellipse 70% 50% at 15% -5%,rgba(155,127,212,.16),transparent 60%),radial-gradient(ellipse 60% 50% at 95% 105%,rgba(110,231,183,.07),transparent 60%)}}
.wrap{{position:relative;z-index:1;max-width:1200px;margin:0 auto;padding:0 26px}}

/* HERO */
.hero{{padding:100px 0 60px;text-align:left}}
.badge{{display:inline-flex;align-items:center;gap:9px;font-size:12px;letter-spacing:.02em;color:var(--accent2);padding:7px 15px;border-radius:100px;background:rgba(110,231,183,.06);border:1px solid rgba(110,231,183,.22);margin-bottom:30px}}
.pulse{{width:7px;height:7px;border-radius:50%;background:var(--accent2);box-shadow:0 0 0 0 rgba(110,231,183,.5);animation:pulse 2.4s infinite}}
@keyframes pulse{{70%{{box-shadow:0 0 0 9px rgba(110,231,183,0)}}100%{{box-shadow:0 0 0 0 rgba(110,231,183,0)}}}}
h1{{font-size:clamp(38px,7vw,74px);font-weight:800;line-height:.98;letter-spacing:-.035em;margin-bottom:22px;color:#fff}}
h1 em{{font-style:normal;background:linear-gradient(105deg,var(--violet) 10%,var(--accent) 55%,var(--accent2) 100%);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}}
.lede{{font-size:clamp(15px,2vw,18px);color:var(--violet-dim);max-width:640px;line-height:1.7}}
.lede strong{{color:var(--violet);font-weight:600}}
.stat-row{{display:flex;flex-wrap:wrap;gap:34px;margin-top:44px;padding-top:32px;border-top:1px solid var(--line)}}
.stat b{{display:block;font-size:30px;font-weight:800;color:#fff;letter-spacing:-.03em;line-height:1}}
.stat span{{font-size:12.5px;color:var(--violet-dim);margin-top:6px;display:block}}

/* INSTANT LAUNCHER */
.launcher{{margin:30px 0 60px;padding:26px 28px;border-radius:18px;background:linear-gradient(135deg,rgba(155,127,212,.16),rgba(110,231,183,.06));border:1px solid rgba(213,198,224,.22);backdrop-filter:blur(14px)}}
.launcher h2{{font-size:18px;color:#fff;margin-bottom:14px;letter-spacing:-.01em}}
.launcher-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:12px}}
.l-btn{{display:flex;align-items:center;gap:12px;padding:14px 16px;border-radius:13px;background:var(--glass);border:1px solid var(--line);color:var(--violet);font-size:14px;cursor:pointer;transition:.22s cubic-bezier(.4,0,.2,1);text-decoration:none}}
.l-btn:hover{{background:var(--glass2);border-color:rgba(155,127,212,.35);transform:translateY(-2px);color:#fff}}
.l-btn .icon{{width:26px;height:26px;border-radius:8px;background:rgba(155,127,212,.14);display:flex;align-items:center;justify-content:center;font-size:15px}}
.l-btn.primary .icon{{background:rgba(110,231,183,.16)}}

/* NAV */
.navbar{{position:sticky;top:0;z-index:50;margin:30px 0 24px;padding:12px 0;background:rgba(8,7,12,.85);backdrop-filter:blur(20px);-webkit-backdrop-filter:blur(20px);border-bottom:1px solid var(--line);border-radius:12px;padding-left:18px;padding-right:18px}}
.nav-scroll{{display:flex;gap:8px;overflow-x:auto;scrollbar-width:none;padding-bottom:3px}}
.nav-scroll::-webkit-scrollbar{{display:none}}
.nav-btn{{flex-shrink:0;font:inherit;font-size:13px;cursor:pointer;color:var(--violet-dim);background:var(--glass);border:1px solid var(--line);border-radius:100px;padding:8px 15px;transition:.22s;white-space:nowrap}}
.nav-btn:hover{{color:#fff;background:var(--glass2);border-color:rgba(213,198,224,.3)}}

/* SEARCH */
.searchbox{{margin:0 0 30px;position:relative;max-width:480px}}
.searchbox input{{width:100%;font:inherit;font-size:15px;color:var(--violet);background:var(--glass);border:1px solid var(--line);border-radius:14px;padding:13px 17px 13px 44px;outline:none;transition:.25s}}
.searchbox input:focus{{border-color:rgba(155,127,212,.5);background:var(--glass2)}}
.searchbox input::placeholder{{color:rgba(168,146,184,.55)}}
.searchbox svg{{position:absolute;left:16px;top:50%;transform:translateY(-50%);opacity:.45}}

/* GROUPS */
.group{{margin-bottom:48px;scroll-margin-top:88px}}
.group-head{{display:flex;align-items:center;gap:13px;margin-bottom:18px;padding-bottom:12px;border-bottom:1px solid var(--line)}}
.group-icon{{font-size:18px;color:var(--accent)}}
.group-head h3{{font-size:19px;font-weight:700;color:#fff;letter-spacing:-.01em}}
.group-count{{margin-left:auto;font-size:12px;color:var(--violet-dim);background:var(--glass);padding:4px 11px;border-radius:100px;border:1px solid var(--line)}}
.skill-list{{display:grid;grid-template-columns:repeat(auto-fill,minmax(290px,1fr));gap:11px}}
.skill{{padding:15px 17px;border-radius:13px;background:var(--glass);border:1px solid var(--line);transition:.25s cubic-bezier(.4,0,.2,1);cursor:pointer;position:relative;overflow:hidden}}
.skill::after{{content:'';position:absolute;inset:0;border-radius:13px;opacity:0;transition:.35s;background:radial-gradient(circle at 50% 0%,rgba(155,127,212,.11),transparent 68%)}}
.skill:hover{{background:var(--glass2);border-color:rgba(155,127,212,.34);transform:translateX(3px)}}
.skill:hover::after{{opacity:1}}
.skill-name{{display:block;font-size:14.5px;font-weight:650;color:#fff;margin-bottom:5px;font-family:ui-monospace,'SF Mono',Menlo,monospace}}
.skill-desc{{display:block;font-size:12.5px;color:var(--violet-dim);line-height:1.5}}
.skill .skill-path{{display:block;font-size:10.5px;color:var(--violet-dim);margin-top:8px;opacity:.7;font-family:ui-monospace,monospace}}
.skill.hide{{display:none}}

/* INSTALL SECTION */
.install{{margin:40px 0 70px;padding:34px 30px;border-radius:18px;background:var(--glass);border:1px solid var(--line);backdrop-filter:blur(14px)}}
.install h2{{font-size:22px;color:#fff;margin-bottom:18px;letter-spacing:-.015em}}
.install .lede{{margin-bottom:22px}}
.step{{margin-bottom:20px;padding-left:14px;border-left:2px solid var(--accent)}}
.step h3{{font-size:14.5px;color:#fff;margin-bottom:7px;font-weight:700}}
.step p{{font-size:13.5px;color:var(--violet-dim);margin-bottom:8px}}
code{{font-family:ui-monospace,'SF Mono',Menlo,monospace;font-size:12.5px;background:rgba(155,127,212,.12);padding:2px 7px;border-radius:6px;color:var(--violet);border:1px solid rgba(155,127,212,.18)}}
pre{{background:#0b0a10;border:1px solid var(--line);border-radius:11px;padding:15px;overflow-x:auto;margin:10px 0 16px}}
pre code{{background:none;padding:0;border:none;color:var(--violet);font-size:12.5px;line-height:1.65}}
.kbd{{display:inline-block;padding:3px 8px;border-radius:6px;background:var(--glass2);border:1px solid var(--line);font-size:11.5px;font-family:ui-monospace,monospace}}

/* CTA */
.cta{{margin:30px 0 80px;padding:46px 36px;border-radius:24px;text-align:center;background:linear-gradient(150deg,rgba(155,127,212,.13),rgba(110,231,183,.05));border:1px solid rgba(213,198,224,.18);backdrop-filter:blur(14px)}}
.cta h2{{font-size:clamp(23px,4vw,34px);font-weight:800;color:#fff;margin-bottom:12px;letter-spacing:-.02em}}
.cta p{{color:var(--violet-dim);max-width:540px;margin:0 auto 26px;font-size:15.5px}}
.btn{{display:inline-block;font:inherit;font-size:15px;font-weight:650;cursor:pointer;padding:13px 32px;border-radius:100px;border:none;background:var(--violet);color:#0a0810;transition:.25s;text-decoration:none}}
.btn:hover{{background:#fff;transform:translateY(-2px);box-shadow:0 12px 34px rgba(213,198,224,.22)}}

footer{{padding:30px 0 46px;border-top:1px solid var(--line);text-align:center;font-size:12.5px;color:rgba(168,146,184,.6)}}
footer b{{color:var(--violet-dim}}

@media(max-width:760px){{.hero{{padding:60px 0 44px}}.stat-row{{gap:24px}}.install{{padding:24px 18px}}.cta{{padding:34px 20px}}.skill-list{{grid-template-columns:1fr}}}}
@media(prefers-reduced-motion:reduce){{*{{animation:none!important;transition:none!important}}}}
</style>
</head>
<body>
<div class="wrap">

  <section class="hero">
    <div class="badge"><span class="pulse"></span> Auto-generated · {len(skills)} สกิล · อัปเดตล่าสุด {datetime.now().strftime('%d/%m/%Y %H:%M')}</div>
    <h1>ฐานสกิลของสลี่<br><em>ครบทุกความสามารถในที่เดียว</em></h1>
    <p class="lede">
      สกัดจาก <code>SKILL.md</code> ครบทั้ง <strong>{len(skills)} ทักษะ</strong> ใน <code>~/cow/skills/</code> —<br>
      ค้นหา เรียกดู และกดปุ่มเพื่อเปิดดูรายละเอียดได้ทันที
    </p>
    <div class="stat-row">
      <div class="stat"><b>{len(skills)}+</b><span>สกิลพร้อมใช้</span></div>
      <div class="stat"><b>{len(groups)}</b><span>หมวดหมู่</span></div>
      <div class="stat"><b>{sum(len(g['items']) for g in groups)}</b><span>SKILL.md ที่สแกนแล้ว</span></div>
    </div>
  </section>

  <section class="launcher">
    <h2>🚀 เด้งด่วน — เปิดฐานสกิลในโหมดที่ต้องการ</h2>
    <div class="launcher-grid">
      <a class="l-btn primary" href="#groups"><span class="icon">⚡</span> เปิดดูทุกสกิล (ด้านล่าง)</a>
      <a class="l-btn" href="#install"><span class="icon">⬇</span> วิธีติดตั้ง & เรียกดู</a>
      <a class="l-btn" href="#" onclick="document.getElementById('q').focus();return false;"><span class="icon">🔎</span> ค้นหาสกิล</a>
      <a class="l-btn" href="../rootbase-skillhub/index.html"><span class="icon">◐</span> เวอร์ชันคลาสสิก</a>
    </div>
  </section>

  <nav class="navbar">
    <div class="nav-scroll">
{"".join(f'<button class="nav-btn" data-jump="g-{i}">{g["title"]}</button>' for i,g in enumerate(groups))}
    </div>
  </nav>

  <div class="searchbox">
    <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>
    <input type="text" id="q" placeholder="ค้นหาสกิล... เช่น เขียนโค้ด, เอกสาร, first principles">
  </div>

  <div id="groups">
{"".join(f'''
<section class="group" id="g-{i}">
  <header class="group-head"><span class="group-icon">{g["title"][:1]}</span><h3>{g["title"][2:]}</h3><span class="group-count">{len(g["items"])}</span></header>
  <div class="skill-list">
{"".join(f'''
<div class="skill" data-name="{s["name"].lower()} {s["desc"].lower()}" title="ดูไฟล์ SKILL.md">
  <span class="skill-name">{s["name"]}</span>
  <span class="skill-desc">{s["desc"] or "(ยังไม่มีคำอธิบาย)"}</span>
  <span class="skill-path">skills/{s["dir"]}/SKILL.md</span>
</div>''' for s in g['items'])}
  </div>
</section>''' for g in groups)}
  </div>

  <section class="install" id="install">
    <h2>📥 แนะนำการติดตั้งและเรียกดู</h2>
    <p class="lede">ฐานสกิลนี้เป็น static HTML — ไม่ต้องติดตั้งอะไรเลย เปิดผ่านเบราว์เซอร์ได้ทันที</p>

    <div class="step">
      <h3>วิธีที่ 1 — เปิดโดยตรง (ง่ายสุด)</h3>
      <p>กดปุ่ม <span class="kbd">⚡ เปิดดูทุกสกิล</span> ด้านบน หรือเปิดไฟล์นี้ในเบราว์เซอร์:</p>
      <pre><code>file:///data/data/com.termux/files/home/cow/websites/skillhub/index.html</code></pre>
    </div>

    <div class="step">
      <h3>วิธีที่ 2 — เปิดผ่านเว็บเซิร์ฟเวอร์ (แนะนำ)</h3>
      <p>เปิดด้วย HTTP server ธรรมดา เพื่อไม่ให้ browser บล็อกไฟล์ local:</p>
      <pre><code>cd ~/cow/websites/skillhub
python3 -m http.server 8088
# แล้วเปิด http://localhost:8088 ในเบราว์เซอร์</code></pre>
    </div>

    <div class="step">
      <h3>วิธีที่ 3 — เชื่อมจาก NovaAgent</h3>
      <p>ถ้า NovaAgent gateway รันอยู่ ให้วางไฟล์ไว้ใน <code>static/</code> แล้วเปิดผ่าน:</p>
      <pre><code>http://127.0.0.1:9899/skillhub/index.html</code></pre>
    </div>

    <div class="step">
      <h3>สร้าง Launcher บนหน้าจอ</h3>
      <p>สร้าง shortcut เปิดฐานสกิลด้วยคำสั่งเดียว (Android / Termux):</p>
      <pre><code># สร้างไฟล์ ~/cow/skillhub-launcher.sh
cat > ~/cow/skillhub-launcher.sh &lt;&lt;'EOF'
#!/data/data/com.termux/files/usr/bin/bash
xdg-open "file:///data/data/com.termux/files/home/cow/websites/skillhub/index.html" 2>/dev/null || \
am start -a android.intent.action.VIEW -d "file:///data/data/com.termux/files/home/cow/websites/skillhub/index.html" 2>/dev/null || \
echo "เปิดที่: ~/cow/websites/skillhub/index.html"
EOF
chmod +x ~/cow/skillhub-launcher.sh</code></pre>
    </div>

    <div class="step">
      <h3>🔄 สร้างใหม่เมื่อมีสกิลเพิ่ม</h3>
      <p>ทุกครั้งที่มี <code>SKILL.md</code> เพิ่ม ให้อัปเดต Skillhub ด้วยคำสั่งเดียว:</p>
      <pre><code>cd ~/cow/websites/skillhub && python3 build.py</code></pre>
      <p>หรือเพิ่ม alias ใน <code>.bashrc</code> / <code>config.fish</code>:</p>
      <pre><code>alias skillhub='cd ~/cow/websites/skillhub && python3 build.py && echo "✅ อัปเดตแล้ว ({len(skills)} สกิล)"'</code></pre>
    </div>
  </section>

  <section class="cta">
    <h2>พร้อมใช้สกิลไหนบอกสลี่ได้เลย</h2>
    <p>ไม่ต้องท่องจำ — เจอสกิลที่ชอบแล้วบอกชื่อมา หรือจะให้สลี่แนะนำตามงานที่ต้องการก็ได้ค่ะ</p>
    <button class="btn" onclick="document.getElementById('q').focus()">เริ่มค้นหาความสามารถ</button>
  </section>

  <footer>
    <b>Skillhub</b> · ฐานสกิลของสลี่ · Auto-generated จาก <code>~/cow/skills/*/SKILL.md</code> (รวม {len(skills)} สกิล)<br>
    บอส · สลี่ (CTO) · ไลรา (CEO) — พีน้องที่ทำงานด้วยกัน
  </footer>

</div>

<script>
const q = document.getElementById('q');
const skills = document.querySelectorAll('.skill');
const groups = document.querySelectorAll('.group');

q.addEventListener('input', () => {{
  const v = q.value.trim().toLowerCase();
  skills.forEach(s => {{
    const t = s.dataset.name;
    s.classList.toggle('hide', v && !t.includes(v));
  }});
  groups.forEach(g => {{
    const vis = [...g.querySelectorAll('.skill')].some(s => !s.classList.contains('hide'));
    g.style.display = vis ? '' : 'none';
  }});
}});

document.querySelectorAll('.nav-btn').forEach(b => {{
  b.addEventListener('click', () => {{
    const el = document.getElementById(b.dataset.jump);
    if (el) el.scrollIntoView({{behavior:'smooth', block:'start'}});
  }});
}});

// คลิกสกิลแล้วไฮไลต์ / เปิด path (สำหรับพัฒนา)
skills.forEach(s => {{
  s.addEventListener('dblclick', () => {{
    const path = s.querySelector('.skill-path').textContent;
    navigator.clipboard?.writeText(path);
    alert('คัดลอก path: ' + path);
  }});
}});
</script>
</body>
</html>
'''

open(OUT, 'w', encoding='utf-8').write(html)
print(f'✅ Generated {OUT}')
print(f'   {len(skills)} สกิล · {len(groups)} หมวดหมู่')
PY