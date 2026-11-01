# BaseCentral catalogue

The existing space artwork stays behind a dark translucent directory panel.
Each app is one ordinary accessible link containing its public name, app-owned
artwork and host. No app data, login/session, storage, tracking, embedded app or
JavaScript runtime is introduced. Missing artwork leaves the named link usable.

`apps.txt` is the single directory configuration: one sibling folder per line,
in display order. `scripts/build-directory.py` reads existing app manifests and
public deployment documentation. It generates the HTML using
`templates/directory.html` and updates `docs/APPS.md`. The server receives only
the existing four public assets; it does not need sibling checkouts or Python.
Regenerate locally before committing/publishing. Source-specific contracts remain
in the app repositories.

Validation covers folder-list changes/order, escaped metadata, invalid folders,
missing URLs, duplicates, no-JavaScript links, narrow/desktop layouts, keyboard
navigation and missing artwork. Configured URLs are checked separately before
publication; HTTP success does not establish full app functionality.

## Verification for this release

The independent review's URL-path and malformed-port findings were reproduced
and fixed; the browser test derives its expected count from the folder list.
Eight generator regressions cover list changes/order, empty selection, escaped
names, missing URLs, invalid folders, duplicates, URL paths and malformed ports.
Eight deployment regressions include refusing a changed list with stale HTML.
Browser checks cover all configured links with JavaScript disabled, widths
320/700/1280, focus navigation, enlarged text, artwork failure and referrer
suppression. Existing background artwork is preserved. The stylesheet URL carries
its content hash to avoid using an older cached stylesheet after publication.

All configured app URLs returned HTTP 200 before publication. FuelLog's current
app-owned deployment metadata points to `gas.basecentral.link`; the generated
catalogue follows that URL. No sibling app code, storage, settings or hosting was
changed by this directory work. Physical Safari 12 was not available for testing.
