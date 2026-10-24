# NovaAgent Security Remediation Plan

> Source: Read-only review by Lyra, 22 October 2026

## Priority order

1. Treat tracked `.preview_secret` as potentially compromised; rotate/revoke it before any history rewrite.
2. Consolidate duplicate `.env` migration code and use atomic writes with owner-only `0600` permissions.
3. Add a strict custom-header allowlist and reject reserved/auth/transport headers.
4. Add regression tests before changing startup or provider behavior.

## API keys written to `~/.cow/.env`

Affected paths:

- `bridge/agent_bridge.py:_migrate_config_to_env`
- `bridge/agent_initializer.py:_migrate_config_to_env`

Safest fix:

- Prefer resolving credentials in memory rather than copying config secrets into `.env` at startup.
- If migration remains necessary, centralize it behind one secure writer.
- Reject symlinks and non-regular files.
- Write atomically through a temporary file, fsync/replace, and enforce `0600` before and after replacement.
- Preserve unrelated environment entries and never log values.

Required tests:

- new and existing `.env` become `0600`
- interrupted writes preserve the old file
- unrelated entries remain intact
- mapped empty values remove only mapped keys
- symlinks are rejected
- logs and exceptions contain no key material
- both previous startup paths behave identically during migration

## Tracked `.preview_secret`

The exact value was intentionally not opened. Because it is tracked, file mode `0600` does not protect Git history, clones, backups, or forks.

Safe procedure:

1. Identify its purpose without exposing the value.
2. Rotate/revoke the external credential if it is live.
3. Add an ignore rule and replace it with a non-secret template.
4. Remove the artifact in a reviewed change.
5. Only after explicit owner approval, rewrite history and force-push if necessary.
6. Scan current tree and history and verify new clones do not contain active secrets.

## Custom provider headers

Current `models/custom_provider.py:get_provider_headers` permits arbitrary scalar header names and values. The downstream client merges extra headers after defaults, so reserved auth/content headers may be overridden.

Safe procedure:

- allowlist only documented provider-routing headers
- reject case-insensitive variants of `Authorization`, `Proxy-Authorization`, `api-key`, `Cookie`, `Set-Cookie`, `Host`, `Content-Length`, `Transfer-Encoding`, `Connection`, and uncontrolled `Content-Type`
- reject control characters, empty names/values, and oversized fields
- apply generated authentication and content headers after custom headers, or reject collisions
- separately validate `api_base` (HTTPS by default, explicit local HTTP opt-in, no credentials in query strings)

Required tests include case variants, CR/LF, oversized values, header collision, and ensuring headers reach only the selected provider endpoint.

## Current implementation boundary

The adapter work intentionally did not change these security paths. Security remediation should be a separate reviewed change after credential rotation/approval, not mixed into the provider-contract integration.

## Implementation status after remediation pass

- Added shared `common/secure_env.py` and routed both bridge migration paths through it.
- Secret migration now rejects symlinks/non-regular files, uses strict temp-file + fsync + replace without in-place fallback, and enforces directory `0700` / file `0600`.
- Added MCP custom-header validation with reserved-header, control-character, and size checks.
- Added dependency-free regression tests in `security_remediation_test.py`; local security tests and relevant syntax checks pass.
- Added `.preview_secret` to `.gitignore`, but the file remains tracked in Git history. No file deletion, history rewrite, rotation, or revocation was performed without explicit approval.
- Lyra's second read-only gate: code-path remediation passes, overall security gate remains blocked by the tracked preview secret.
