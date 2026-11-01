# BaseCentral controls 1.0.0

`controls.css` is the screen-only upstream stylesheet. `icons.svg` is the canonical original SVG action family, with matching inline geometry in `icons.json` for renderer integration. Never use Unicode/emoji gears or a runtime icon font. The SVG paths inherit currentColor and decorative SVGs have aria-hidden/focusable=false; buttons retain localized names.

Open `gallery.html` locally to compare variants, native selectors, focus and long labels. Copy styles/icons using `python3 scripts/sync-controls.py --write APP`; `--check` detects drift without writing. Each app owns its integration, palette, exclusions and release inventories. Never add a remote toolbox dependency. New apps use `.pwa-control`, the primary/secondary/quiet/danger/icon variants, `.pwa-icon` and `.pwa-actions`. Existing integrations preserve palettes through local adapters. Meaningful game/preview controls are excluded; print is untouched.

Run `node scripts/test-controls.cjs` for real-browser geometry/focus tests and `node scripts/smoke-controls.cjs` for existing local app screens. PLAYWRIGHT_PATH and CHROMIUM_PATH can select local developer tools. These checks do not establish physical iOS compatibility.
