#!/usr/bin/env node
/**
 * index.js — Slilelo Browser MCP Server (stdio transport)
 *
 * Thin entry: registers tools, routes to BrowserActions, shapes MCP replies.
 * All real logic lives in actions.js / browser.js / snapshot.js.
 *
 * Design goals (first principles):
 *  - one persistent browser session per server lifetime (fast, stateful)
 *  - token-efficient snapshots with stable refs (agent-friendly)
 *  - graceful errors returned as text, never a crashed server
 */
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';
import { BrowserActions } from './actions.js';

const actions = new BrowserActions();

const TOOLS = [
  {
    name: 'navigate',
    description: 'Open a URL in the persistent browser and return a compact snapshot of interactive elements.',
    inputSchema: {
      type: 'object',
      properties: {
        url: { type: 'string', description: 'Absolute http(s) URL' },
        wait_until: { type: 'string', enum: ['domcontentloaded', 'load', 'networkidle'], default: 'domcontentloaded' },
      },
      required: ['url'],
    },
  },
  {
    name: 'snapshot',
    description: 'Re-read the current page and list interactive elements with refs (e1, e2, ...).',
    inputSchema: { type: 'object', properties: {} },
  },
  {
    name: 'click',
    description: 'Click an element by ref (e.g. "e3"), CSS selector, or visible text.',
    inputSchema: {
      type: 'object',
      properties: { target: { type: 'string' }, timeout: { type: 'number' } },
      required: ['target'],
    },
  },
  {
    name: 'fill',
    description: 'Type into an input/textarea by ref, CSS selector, or label text. Set submit=true to press Enter.',
    inputSchema: {
      type: 'object',
      properties: { target: { type: 'string' }, text: { type: 'string' }, submit: { type: 'boolean' } },
      required: ['target', 'text'],
    },
  },
  {
    name: 'select',
    description: 'Choose an option in a <select> dropdown by ref or selector.',
    inputSchema: {
      type: 'object',
      properties: { target: { type: 'string' }, value: { type: 'string' } },
      required: ['target', 'value'],
    },
  },
  {
    name: 'press',
    description: 'Press a keyboard key (e.g. Enter, Tab, Escape, ArrowDown).',
    inputSchema: { type: 'object', properties: { key: { type: 'string' } }, required: ['key'] },
  },
  {
    name: 'screenshot',
    description: 'Capture a PNG of the current page and return its local file path.',
    inputSchema: {
      type: 'object',
      properties: { name: { type: 'string' }, full_page: { type: 'boolean' } },
    },
  },
  {
    name: 'get_text',
    description: 'Return the visible text of the current page (truncated for context safety).',
    inputSchema: { type: 'object', properties: {} },
  },
  {
    name: 'evaluate',
    description: 'Run JavaScript in the page and return the JSON-serialized result.',
    inputSchema: { type: 'object', properties: { script: { type: 'string' } }, required: ['script'] },
  },
  {
    name: 'wait',
    description: 'Wait for a CSS selector to appear, or for the network to settle.',
    inputSchema: {
      type: 'object',
      properties: { selector: { type: 'string' }, timeout: { type: 'number' } },
    },
  },
  {
    name: 'scroll',
    description: 'Scroll the page up or down and return a fresh snapshot.',
    inputSchema: {
      type: 'object',
      properties: {
        direction: { type: 'string', enum: ['up', 'down'], default: 'down' },
        amount: { type: 'number', default: 600 },
      },
    },
  },
  {
    name: 'back',
    description: 'Go back in history and return a fresh snapshot.',
    inputSchema: { type: 'object', properties: {} },
  },
  {
    name: 'forward',
    description: 'Go forward in history and return a fresh snapshot.',
    inputSchema: { type: 'object', properties: {} },
  },
  {
    name: 'close',
    description: 'Close the browser session and free resources.',
    inputSchema: { type: 'object', properties: {} },
  },
];

const server = new Server(
  { name: 'slilelo-browser', version: '1.0.0' },
  { capabilities: { tools: {} } },
);

server.setRequestHandler(ListToolsRequestSchema, async () => ({ tools: TOOLS }));

// Tool name (snake_case, MCP-facing) → action method (camelCase, internal).
// Keep this explicit: a missing alias silently degrades to "unknown tool".
const ACTION_ALIASES = { get_text: 'getText' };

server.setRequestHandler(CallToolRequestSchema, async (req) => {
  const { name, arguments: args = {} } = req.params;
  const fn = actions[ACTION_ALIASES[name] ?? name];
  if (typeof fn !== 'function') {
    return { content: [{ type: 'text', text: `unknown tool: ${name}` }], isError: true };
  }
  try {
    const out = await fn.call(actions, args);
    const parts = [{ type: 'text', text: out.text ?? JSON.stringify(out) }];
    if (out.path) parts.push({ type: 'text', text: `ARTIFACT: ${out.path}` });
    return { content: parts };
  } catch (err) {
    const msg = err && err.message ? err.message : String(err);
    return { content: [{ type: 'text', text: `ERROR: ${msg}` }], isError: true };
  }
});

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  process.stderr.write('[slilelo-browser] ready on stdio\n');
}

process.on('SIGTERM', async () => { await actions.close({}); process.exit(0); });
process.on('SIGINT', async () => { await actions.close({}); process.exit(0); });

main().catch((e) => {
  process.stderr.write(`[slilelo-browser] fatal: ${e.stack || e.message}\n`);
  process.exit(1);
});
