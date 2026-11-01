# Shared PWA controls

Status: proposed for review, 1 November 2026. Runtime changes have not started.

## Intent and authority

The user requested fixes for mismatched buttons across the applications and a
common set for all apps, identifying Festival as the newest app. Use the current
shared `AGENTS.md` as the requirements and Festival as the starting reference.
Festival itself needs normalization; copying its current stylesheet wholesale
would retain inconsistencies.

The user clarified that the Settings gear looks like a realistic Unicode glyph
on iOS and clashes with the cleaner apps. The shared Settings icon must therefore
be a simple flat outline SVG, with consistent rounded strokes and no shading,
emoji, Unicode gear, icon font or platform-provided rendering. Its shape is the
same in every app; its foreground color follows the app's button theme. Replacing
existing glyph gears is an explicit acceptance criterion.

Preserve each app's palette, body typography, artwork, task semantics, storage,
records, backup formats, permissions, server boundaries and physical outputs.
This work changes existing controls and their presentation. It does not implement
the separate functional compliance backlog from the preceding audit or deploy
any application.

## Common control contract

- Ordinary text buttons, icon buttons, button-like action links and selectors
  use a 44 CSS-pixel base height and at least 44 CSS-pixel hit width. Long labels
  wrap and increase height when needed; controls in a row align at the top.
- Controls have a 2px radius, 1px border, 4px vertical/8px horizontal padding and
  a shared 2/4/6/8/12/16/24px spacing scale. Use 6–8px action gaps, with margin
  fallbacks where Safari 12 cannot implement flex gap. Preserve larger controls
  when their task needs them.
- Provide primary, secondary, quiet, destructive, icon-only, selected/pressed,
  disabled and busy variants. App adapters provide accessible colors in each
  existing theme. Keep visible labels and native button/select semantics.
- Hover and press treatments do not move controls, change border thickness or
  alter text dimensions. Keyboard focus remains visible in Safari 12 as well as
  modern browsers; reduced-motion and forced-colors behavior remain usable.
- Use one original bundled inline-SVG action family: Settings, Check for updates,
  Update app, Import, Export, Close, Back, expand/collapse, Add, Remove, Previous,
  Next, Edit, Delete, Download, Print, Share, Play and Pause. Common geometry uses
  a 24-unit viewBox, 20px default display size and consistent rounded strokes.
  Icons inherit foreground color, are decorative beside labels, and never replace
  an accessible action name. Keep domain artwork and language flags distinct.
- Normalize native selectors to the same height and top edge, with one local SVG
  chevron and enough space for it. Retain native keyboard and touch selection.
  Existing native language selectors receive flag-only options and an accessible
  full language name. Converting custom language menus or adding absent language
  systems belongs to the broader compliance work unless separately requested.
- Keep `[hidden]`, disabled, validation, loading, selection and ARIA states
  authoritative. A shared display rule must never reveal hidden controls.
- Preserve meaningful circles (radio buttons, switches, avatars, game pieces),
  content previews, puzzle/canvas geometry, specialist gestures and print output.
  Controls embedded in games or dense task components need explicit adapters;
  do not blanket-restyle every link, SVG, label or child of a card.

## Packaging and ownership

Builder's proposed implementation: a small framework-free kit maintained under
`pwa/shared/controls/`, with a stylesheet, original SVG source, integration guide,
standalone control gallery and a development-only synchronization/check script.
Use local copied assets in each app, with identical upstream files plus a small
app-owned adapter. Each app remains independently deployable and usable offline;
there is no dependency on the toolbox URL, sibling filesystem paths, npm at
runtime, a CDN or a frontend framework.

Use explicit classes and deliberate mappings to existing selectors. Preserve
element IDs, event targets, accessible names, translated labels and data
attributes used by application code. Prefer inline icon geometry compatible
with the app's existing renderer over cross-document SVG references or automatic
DOM rewriting. Any runtime helper must use Safari 12 compatible syntax and add
no global mutation observer or unrelated event interception.

Document the kit version in each app. Make the synchronization tool report drift
by default and write only on an explicit invocation, with an application list
and clear file inventory. Never overwrite app-owned adapters.

## Adoption scope

Apply the same contract to all thirteen apps, starting with Festival to establish
the reference. Preserve these application boundaries:

| App | Specific integration constraints |
| --- | --- |
| Festival | Preserve calendar cells, holiday icons, civil dates, table scrolling and country picker; normalize toolbar, dialogs and Settings actions. |
| a4 | Preserve session-only images, per-page editing, corner handles and no-crop A4 export; fix the existing 40px editor-button override. |
| Agenda | Serve assets only from `public/`; include PHP templates and offline views without altering authorization or sync. |
| Balance | Preserve themed game controls, two-sided geometry, functional game indicators and fabrication output; ordinary controls get the shared treatment. |
| Doctools | Work inside `web/`; preserve workers, processing locks, previews, bounds and no document history. |
| Elementar | Preserve puzzle/person selectors, board artwork, in-memory progress and print/PDF geometry. |
| Eternal Timer | Preserve timer displays, wheel picker, touch gestures and timestamp behavior; ordinary actions and icon buttons adopt the kit. |
| Flip | Preserve movement choices, page previews and physical flipbook geometry; retain its established 44px control treatment where already correct. |
| Freezer | Preserve quantity semantics, editing and print/PDF layout; enlarge screen-only undersized quantity actions without changing paper output. |
| FuelLog | Preserve maps, bottom sheet, forms and calculations; integrate static and dynamically rendered actions. |
| Govio | Preserve local automatic conversion, slot selection, player constraints and PHP shell. |
| Oficina | Preserve workshop forms, financial meaning, editing ownership and private-sync controls. |
| Sopa de Letras | Work in the PWA runtime only; preserve saved progress, puzzle gestures, Python tools and print/PDF. |

The static toolbox can host the kit documentation/gallery but does not gain
application Settings, storage or a service worker.

## Release safety

Read each app's instructions and relevant release/deployment contract before
editing it. Keep existing uncommitted work. Include every added runtime asset in
the app's own offline inventory and publication allowlist. Update linked release
markers and content hashes using the project's existing mechanism. Never improve
appearance by clearing storage or changing data schemas. Do not change update
activation behavior as an incidental part of this visual work.

## Verification and acceptance

1. Review the gallery's variants, icon-only actions, native selects, long English
   and Portuguese labels, disabled/busy states and dark-theme example.
2. Inspect actual app controls at 320px, a short landscape viewport and desktop
   width. Check button bounds, top alignment, wrapping, page overflow and focus.
3. Exercise existing actions after migration: clicks, keyboard, dialogs, dynamic
   renders, hidden states and representative task-specific controls. Verify
   existing print styles and specialist outputs remain unchanged.
4. Run the projects' relevant asset/version/release checks and focused behavioral
   suites. Verify offline reload includes the local kit. Compare copied kit files
   against their canonical source and report untested apps/flows honestly.
5. Physical Safari 12/Home Screen testing remains separate from modern browser
   automation. No deployment or production claim follows from local checks.

Acceptance means a common usable set is present locally in all thirteen apps,
observed button mismatches are corrected, and the verification report identifies
remaining device or feature-specific limitations. The shared helper font is a
separate collection decision and is not selected by this button work.
