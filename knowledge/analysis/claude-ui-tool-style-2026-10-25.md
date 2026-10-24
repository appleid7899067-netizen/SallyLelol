# Claude-like Tool UI override — summary

Created: 2026-10-25

Goal: Provide a non-destructive CSS override that makes the Tool UI resemble "Claude" (Anthropic) styling without changing existing theme-tools.css directly. The override is scoped under .claude-theme and uses Anthropic brand colors and typography per skills/brand-guidelines/SKILL.md.

Files created:
- NovaAgent-Brandable/channel/web/static/css/theme-tools-claude.css — CSS override file scoped under .claude-theme

How to apply:
- Add class="claude-theme" to the <body> element or wrap the chat container with a div that has that class. This keeps the change non-destructive and toggleable.
- Example: <body class="claude-theme"> or <div class="claude-theme">...chat...</div>
- Ensure chat.html or the app loads the CSS file (add a <link rel="stylesheet" href="/assets/css/theme-tools-claude.css"> near other theme files).

Design notes:
- Uses Anthropic colors: dark background (#141413), light text (#faf9f5), and accents (orange/blue/green).
- Applies Poppins for headings and Lora for body as preferred (falls back to Arial/Georgia).
- Gentle running-state pulse uses Anthropic blue; failures use red-ish tint; success uses green accent.
- Respects prefers-reduced-motion and provides light-mode adjustments.

Testing checklist:
1. Load chat UI with the CSS linked and body class set; verify Agent Steps panel visually changes to dark Claude-like theme.
2. Check running/failed/success states for icons and pulses.
3. Verify mobile responsive behavior (max-width:640px) and reduced-motion.
4. Ensure no layout regressions on other pages that don't have .claude-theme class.

Risks & notes:
- This is a visual override only. It doesn't alter JS behavior; if send.js expects certain DOM or classes, confirm compatibility.
- If multiple theme override files are present (theme-tools.css, theme-tools-grouped.css), load order matters — the claude file should be loaded after them to apply overrides.

Next steps (optional):
- Add a small toggle in UI settings to switch themes by adding/removing .claude-theme on body.
- Create a test page/screenshot set to capture before/after for QA.

Recorded by: Sally (สลี่)
