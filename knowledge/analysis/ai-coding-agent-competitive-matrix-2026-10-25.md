# AI Coding Agent Competitive Matrix — 25 October 2026

> Scope: source-backed snapshot for positioning, not a benchmark or ranking. Vendor product pages describe vendor claims; feature availability and pricing can vary by plan, account, region, and release.

## Matrix

| Product | Interface / platform | Agent and integrations | Memory / context | Browser | Data / privacy | Pricing / models |
|---|---|---|---|---|---|---|
| Claude Code | Official docs list terminal, IDE extensions, desktop, and web surfaces. | Reads and edits code, runs commands, supports MCP, skills, hooks, and parallel agents. | Project instructions and auto memory are documented. | Official Chrome integration supports web testing, form tasks, extraction, and visible actions with permissions. | Data handling varies by consumer/commercial account and provider; consumer training choice and retention differ. Local transcript cache is documented. | Subscription/API/provider routes vary; see current official pricing and docs. |
| Cursor | Official docs describe Cursor as a coding agent and document editor/CLI/cloud workflows. | Repo work, planning, review, plugins, skills, subagents, hooks, and MCP are documented. | Do not infer absence/presence of persistent memory from this source set; scope not verified here. | Not verified from sources collected for this snapshot. | Security page says Privacy Mode prevents training when enabled; further data governance details are linked by vendor. | Model options and plan/usage information are documented; current rates are plan-dependent. |
| Windsurf / Devin Desktop | Provider says Devin Desktop is the new name of Windsurf; desktop IDE plus agent command center. Transition details can vary. | Devin Desktop docs describe Cascade modes and tools; not every legacy Windsurf detail is confirmed. | Current docs list Memories & Rules; verify availability by plan/version. | Not verified in this snapshot. | Not assessed from provider privacy docs in this snapshot. | Pricing page returned Devin-branded plans; re-check before publishing. |
| OpenCode | Official docs describe terminal UI, desktop app and IDE extension; OpenCode 2 docs are linked separately. | Official docs list configurable agents, tools, permissions and integrations. | Do not assert no cross-session memory without a current source. | Not established by this research snapshot. | Avoid broad claims about data handling without checking current product/provider-specific docs. | Docs say users configure LLM providers; verify current official pricing/model details before claims.
| NovaAgent (local source review) | Local web console; project source has SSE chat events. Public feature availability not assessed. | Source supports delegation/teammate responses when configured; not evidence of an always-on automatic group meeting. | Conversation persistence and an evolution-log mechanism exist in code; exact runtime settings/retention vary. | Browser tool can open pages and return snapshots; this is not proof of a continuous live-screen feed. | Prompts are passed to the configured model/provider. Conversation stores and logs exist; deletion/retention differ by data type. Provider training/retention cannot be generalized. | Provider and model choice are configured; “free” cannot be generalized to external API/provider costs. |

## Source-backed details

### OpenCode
- Intro: https://opencode.ai/docs/ — documents terminal UI, desktop app, IDE extension, provider setup and usage. Accessed 2026-10-25.
- Agents: https://opencode.ai/docs/agents/ — documents primary agents/subagents, configurable tools and permissions. Accessed 2026-10-25.

### Claude Code
- Overview: https://docs.anthropic.com/en/docs/claude-code/overview — terminal, IDE, desktop, web, code editing, commands, MCP and memory.
- Chrome integration: https://docs.anthropic.com/en/docs/claude-code/chrome — browser automation capabilities, permissions, visible browser actions, and plan/account prerequisites.
- Data usage: https://docs.anthropic.com/en/docs/claude-code/data-usage — consumer vs commercial training/retention, local transcript caching, telemetry and provider differences.
- Accessed: 2026-10-25.

### Cursor
- Docs: https://cursor.com/docs — coding-agent workflows and customization surfaces (agents, plugins, skills, subagents, hooks, MCP, Cloud Agents).
- Security: https://cursor.com/security — vendor states Privacy Mode, when enabled, means it will not train on user data; page says last updated 2026-08-25.
- Models and pricing: https://cursor.com/docs/models — model selection and pricing/usage information.
- Accessed: 2026-10-25.

### Windsurf / Devin Desktop
- Product page: https://windsurf.com/ — states Devin Desktop is the new name of Windsurf; IDE foundation remains and product adds an agent command center. Accessed 2026-10-25.
- Docs: https://docs.windsurf.com/windsurf/cascade/cascade — content is Devin Desktop docs describing Cascade modes, tools, memories/rules, simultaneous agents. Accessed 2026-10-25.
- Plans: https://windsurf.com/pricing — page returned Devin-branded plans on access date; use only with rebrand caveat and re-check before publication.
- Do not assume every legacy Windsurf feature or plan is unchanged; the provider says plans and settings carry over during update, but transition state can evolve.

### NovaAgent local source evidence (static inspection; not runtime verification)
- Prompt/model path: `agent/chat/service.py`, `agent/protocol/agent_stream.py`, `bridge/agent_bridge.py`.
- Conversation persistence/retention/deletion: `agent/chat/service.py`, `agent/memory/conversation_store.py`, `channel/web/api/sessions.py`, `agent/knowledge/service.py`.
- Teammate delegation: `agent/tools/agent_delegate/agent_delegate.py`, `agent/multiagent/transport.py`, `agent/chat/service.py`.
- Evolution records: `agent/evolution/executor.py`, `agent/evolution/record.py`.
- Browser and SSE: `agent/tools/browser/browser_tool.py`, `agent/tools/browser/browser_service.py`, `channel/web/api/chat.py`, `channel/web/core/channel.py`.
- These source paths were reviewed statically; this note does not attest to a specific live installation, provider configuration, or runtime behavior.

## Safe publication guidance

- Do not describe competitors as lacking memory, browser control, privacy, or agent capabilities unless a current primary source establishes the scope.
- Mark unsupported or inaccessible information as “not verified,” never as “does not have.”
- Describe NovaAgent as using the configured provider and disclose that data handling depends on provider and local settings.
- Count only explicitly defined, visible log rows if rendering a counter; do not imply it measures intelligence or learning quality.

## Related
- [OpenCode Competitive Analysis](opencode-competitive-analysis-2026-10-25.md) — earlier product-positioning analysis; detailed claims need source refresh before publication.
- [NovaAgent Multi-Agent Meeting Room](multi-agent-meeting-room.md) — local architecture and operational constraints.
