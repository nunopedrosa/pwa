# Shared controls and deployment — implementation report

Inspected working copies: 1 November 2026. All changes are local and uncommitted.
No production deployment, SSH publication, push, migration or account operation ran.

## Delivered

- Canonical screen-only control CSS and original SVG action family in `shared/controls/`, with a standalone `gallery.html`. Ordinary adopted controls have at least 44px targets, compact corners, consistent focus/disabled/busy treatment and top-aligned selectors. Each app retains its colors and domain controls.
- Existing Unicode Settings gears replaced with a common flat inline SVG, including Agenda's offline shell. Festival and Flip use that same geometry. The kit has a local selector-chevron asset to respect restrictive content-security policies.
- Local kit copies in all thirteen applications; no runtime request to the toolbox or a sibling checkout. App adapters handle narrow headers, larger action rows and Balance's update bar. Festival calendar-cell borders are explicitly excluded from ordinary button styling.
- One Bash 3-compatible deployment engine, vendored in the toolbox and the twelve applicable app repositories. Tiny wrappers load app-owned public inventories and hooks. Agenda retains its PHP/private-server deployment boundary.
- Common command: `bash scripts/deploy.sh [--dry-run] [--verify] [DESTINATION]`. Normal deployment requires a clean tracked Git branch and fail-closed fast-forward update. Dry runs never fetch or write. Staging, locking, path validation, local byte verification and update-metadata-last publication are shared. No broad pruning, automatic clone or SSH wrapper remains.
- Doctools retains hash-verified immutable releases and its owned `current` link. Its existing release generator now also regenerates deployment hashes and the public inventory.
- Oficina retains staged query rewriting, managed Apache/public PHP files and its private-data exclusions. Balance retains build checks and a required successful private public-site backup. Festival preserves existing host headers or installs its template only when absent.
- `scripts/sync-controls.py` and `scripts/sync-deploy.py` check drift by default and write only with `--write`; app-owned adapters/profiles are preserved.

## Independent review and corrections

A fresh reviewer inspected the uncommitted changes across the repositories. All five actionable findings were corrected:

1. Doctools release directories now become 0755 before activation.
2. The existing `BALANCE_DRY_RUN=1` safety flag is honored.
3. User-controlled root ancestors, including backup/release roots, are checked for symlinks before canonicalization. Standard macOS `/tmp` and `/var` aliases remain usable.
4. Doctools deployment checksums/inventory are regenerated through `npm run release` and exact coverage is checked.
5. Agenda's client builders and Doctools' dynamic format/preview/download controls adopt the shared set.

The first three findings and stale-sidecar behavior were reproduced by failing regressions before fixes. Dynamic-control browser assertions likewise failed before adoption. An additional visual check caught ordinary control borders on Festival calendar cells; its regression now enforces the domain-specific borderless cells.

## Verification

- Shared control fixture: real browser checks for 44px geometry, selector alignment, long-label wrapping, hidden/disabled states, focus and print isolation.
- Local browser smoke: eleven static entry screens at 320px and desktop width; existing Settings actions and dynamic controls. Agenda's actual client button/select builders were exercised in an isolated DOM. No Unicode gear or horizontal page overflow on the inspected screens.
- Shared engine: 17 isolated Git/filesystem tests, including Bash 3, dirty/divergent/failed upstreams, dry run, nested symlinks, backup paths, failed staging, source changes, release permissions and preservation of the previous release link.
- Actual profiles: 13 disposable-repository checks, including expected refusal for Govio's incomplete vendor inventory. Private boundaries, Oficina's staged URLs, Balance's backup and Doctools' release mode were checked.
- Legacy deployment regressions: toolbox 7, a4 5 and Festival 17 passing checks. Fixtures now vendor the local core/profile and model the clean-Git contract. Festival fixture clones use upload-pack rather than fragile local hardlinks.
- Festival: `npm test` and `npm run build` passed; catalogue/engine bytes were retained. Only the root app package version changed in the lockfile.
- Doctools: 171 unit tests plus browser processing, offline/cache repair, busy-window update locking, release transitions and format-help checks passed. Independent Pillow/jpegtran oracle passed 12 images using the installed Pillow decoder with a temporary flat-sample API compatibility adapter; product/oracle source was unchanged.
- FuelLog: asset/release, translation, update and backup checks passed. Eternal Timer: asset/release checks passed.
- Balance: worker resilience, panel/artwork, checkpoint and two-sided geometry suites passed. Elementar: language, portraits, targets and evidence/generation suites passed. Oficina: syntax, compatibility, 63 workshop rules and two worker checks passed.
- Modified browser JS and PHP parsed; repository diffs passed whitespace checks. Generated tracked screenshots/documents from tests were restored so the change set contains source and intended assets only.

## Deliberate scope and remaining checks

This implements controls and deployment consolidation, not the earlier full PWA-compliance backlog. It does not add absent Settings/language/backup systems, change update activation, migrate data, choose the shared helper font, or change game/print/fabrication semantics.

Physical iPhone 6/Safari 12 and installed-PWA behavior remain unverified. Agenda's authenticated/database workflows were not run. Govio's documented Mediabunny runtime files are absent locally; PHP rendering/syntax and incomplete-release refusal were checked, not video conversion. Host headers, current server paths and actual publication must be verified during a separately authorized deployment. New profiles/wrappers/core assets must be committed and published to the relevant source remotes before the host's normal deployment command can accept them.

## Rulings made

- Reused existing checkouts and left changes uncommitted to preserve user work and the current approved baseline; the user can review each repository's diff.
- Used real-browser checks for reversible CSS and isolated Git/filesystem tests for deployment safety; neither establishes physical-device support.
- Used existing renderer APIs and generated inline SVG geometry rather than a shared runtime or DOM observer; integration remains app-owned.
- Kept app-specific release/private boundaries, with no broad stale-file cleanup. Previously broad deletion is superseded explicitly in the deployment notes; managed cleanup would need its own reviewed policy.

No independent-review findings remain deferred.
