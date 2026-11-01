# Shared PWA Controls Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** Correct mismatched controls in all thirteen PWAs with one locally bundled control and SVG action set.

**Architecture:** Maintain canonical CSS and original SVG geometry in the central toolbox repository. Vendor identical upstream assets with explicit app adapters; retain existing renderers, event handlers, palettes and offline/release mechanisms.

**Tech Stack:** Static CSS, SVG, existing vanilla JavaScript/PHP, Python development-only sync and isolated browser checks.

**Spec:** `docs/superpowers/specs/2026-11-01-shared-controls-design.md` (approved in chat; user clarified flat SVG gear).

## Global Constraints

- 44 CSS-pixel base height and at least 44 CSS-pixel hit width; long labels may increase height.
- 2px control radius, 1px border, 4px/8px padding, 6–8px ordinary action gaps; align rows at the top.
- Safari 12 compatible required CSS/JS paths; local assets only, no runtime framework/CDN/toolbox requests.
- Flat outline SVG Settings gear, no Unicode/emoji/font gear; shared geometry and app-colored foreground.
- Preserve IDs, event handlers, translation/catalogue contracts, hidden/disabled/ARIA states and app themes.
- Preserve data, formats, domain controls, meaningful circles and print/fabrication geometry.
- Keep kit copies in offline/deploy inventories and linked release identifiers consistent; never deploy.
- Preserve existing uncommitted work, including current shared-baseline edits.

## Review Focus

- Hidden/busy controls must stay unavailable after CSS and dynamic re-renders; exercise `[hidden]`, disabled and busy variants.
- Long Portuguese labels at 320px and enlarged text must wrap without page overflow or clipped actions.
- Existing JS that replaces text/markup or identifies an event target must keep correct semantics after SVG adoption.
- Print and game-specific controls must retain dimensions/gesture behavior despite shared screen styles.
- A newly added kit asset must be both precached and published with the app's actual release contract.

---

### Task 1: Canonical controls and local gallery

**Files:** Create `shared/controls/controls.css`, `shared/controls/icons.svg`, `shared/controls/README.md`, `shared/controls/gallery.html`, `scripts/sync-controls.py`, `scripts/test-controls.py` in central `pwa/`.

**Interfaces:** CSS `.pwa-control` with primary/secondary/quiet/danger/icon modifiers; `.pwa-actions` for top-aligned wrapping rows; `.pwa-icon` for decorative inline SVG; `--pwa-control-*` palette tokens. Development-only `sync-controls.py --check [APP...]` reports drift; `--write` explicitly copies upstream files and never adapters. SVG geometry is referenced by stable action IDs documented in the spec.

- [x] Add a browser fixture asserting 44px ordinary controls, a wrapping long-label variant, hidden/disabled states, native select alignment and keyboard focus; run and confirm missing kit fails.
- [x] Implement the kit/gallery with the spec's values, explicit print exclusion, focus fallback and Safari-compatible spacing.
- [x] Implement explicit app inventory and byte comparison/copy tooling; test that checking is read-only and writing preserves adapters/unrelated files.
- [x] Run `python3 scripts/test-controls.py`; inspect gallery at 320px and desktop in both palette examples.

### Task 2: Festival reference integration

**Files:** `festival/styles.css`, `festival/index.html`, `festival/app.js`, `festival/assets/icons.svg`, `festival/icons.js`, `festival/scripts/build.cjs`, `festival/precache.js`, `festival/deploy-files.txt`, version markers and local kit/adapters/docs.

**Interfaces:** Consume Task 1 kit; preserve Festival icon lookup and IDs. Generate common icon geometry from the reviewed canonical source during development, retaining holiday artwork separately. Runtime build is unchanged.

- [x] Capture toolbar, Settings and dialog button bounds at 320px/desktop, including long EN/PT labels and selected country actions.
- [x] Integrate kit, remove superseded toolbar/control overrides and normalize gear/action geometry without changing holiday/calculation behavior.
- [x] Update build inventory and synchronized release markers; build prepared assets only with the documented local tooling.
- [x] Run `npm test`, focused browser geometry/action checks and `git diff --check`; verify offline reload and publication inventory.

### Task 3: Existing themed and bilingual apps

**Files:** Each app's entry HTML, screen CSS, existing icon renderers, local kit/adapter, docs and linked release inventories in `a4/`, `balance/`, `elementar/`, `flip/`, `fuel/`, `sopa_de_letras/pwa/`.

**Interfaces:** Task 1 classes/tokens and canonical SVG paths; each existing rendering entry point stays responsible for event wiring and localized names. Do not add custom-language-menu migrations or absent features.

- [x] Inspect each app's instructions, handover/code map and control selectors; record functional/domain exclusions before edits.
- [x] Adopt copied kit and explicit adapter, normalize ordinary controls and replace existing common-action glyphs, including every Unicode Settings gear.
- [x] Update required version markers, query strings, precache lists and deploy allowlists using the app's own mechanism.
- [x] Run FuelLog and Eternal Timer asset checks where relevant, Balance worker/panel tests, and each changed app's documented focused checks; verify clicks, dynamic re-renders, keyboard, 320px EN/PT layout and offline reload.
- [x] Confirm fabrication/print CSS and puzzle/game gestures retain their prior behavior; record device checks unavailable locally.

### Task 4: File processors and record apps

**Files:** Entry templates, control CSS/renderers, kit/adapters, docs and release inventories in `agenda/public/` plus `agenda/templates/`, `doctools/web/`, `eternytimer/`, `freezer/`, `govio/`, `oficina/`.

**Interfaces:** Same kit API. Existing private server paths, processor worker locks, timer state and workshop ownership remain application-owned.

- [x] Inspect app-local requirements and identify existing ordinary actions and protected task/print controls.
- [x] Apply common control treatment and SVG paths to existing controls only; preserve no-history/private-server boundaries.
- [x] Refresh linked release inventories/markers; Doctools uses `npm run release`, not hand-edited hashes. Add kit files only to each app's public inventory.
- [x] Run relevant documented suites and smoke existing action handlers with synthetic data. Verify hidden states, safe Settings/dialog closure, keyboard focus and narrow layouts.
- [x] Verify Freezer print/PDF dimensions and ordinary timer gestures are unchanged; report physical-device limitations.

### Task 5: Collection verification and documentation

**Files:** Central integration guide/check script and per-app adoption notes; update stale baseline references only where needed for this implementation, preserving current decisions.

**Interfaces:** `sync-controls.py --check` over all thirteen apps; app-owned adapters are intentionally different, upstream kit files are identical.

- [x] Run drift check, all changed asset/version checks and `git diff --check` per repository.
- [x] Inspect representative screens from every app, test gear geometry is SVG rather than text, compare action-row bounds and detect page-width overflow at 320px.
- [x] Record app-by-app checks, exclusions, runtime release IDs and remaining physical Safari/Home Screen verification.
- [x] Review the complete diffs for unexpected data/domain/print/server changes. Leave all work local for the user; do not push or deploy.

## Execution

Proposed execution method: native in this chat, with one independent final review,
because the kit interface is shared and app integration needs sequential visual
checks. Git commits are optional checkpoints after review; do not stage unrelated
user changes. Deployment consolidation has its own proposed design and will have
a separate implementation plan after its scope is approved.
