# BaseCentral

The app catalogue at [basecentral.link](https://basecentral.link/), with the
existing BaseCentral artwork behind a responsive list of app links.

The website is static HTML/CSS. It has no JavaScript runtime, accounts, tracking,
shared app storage or installation requirement. Each app opens on its own site.

## One configuration file

Edit **[apps.txt](apps.txt)** to add, remove or reorder apps. It contains sibling
folder names, one per line; `#` comments and blank lines are allowed:

```text
festival
fuel
eternytimer
```

Then regenerate locally:

```sh
python3 scripts/build-directory.py
python3 scripts/build-directory.py --check
```

The generator reads each selected app's existing manifest and public deployment
URL, then updates `index.html` and [the application registry](docs/APPS.md).
There is no directory-specific metadata mapping to maintain. An empty list
produces an empty catalogue. Missing folders, invalid metadata and missing URLs
stop generation before replacing the previous page.

Keep the app checkouts beside this repository. A new app needs its own valid
manifest and documented public HTTPS URL, normally `DEPLOY_URL` in its deployment
profile. Names and icons come from its manifest. Documentation fallbacks preserve
hosting subdirectories. The generator reads public metadata only, never executes
shell profiles, contacts app services or changes sibling repositories.

Commit the list and generated output together. Deploy refuses a changed folder
list with stale HTML. `--root /path/to/apps-parent` can select another local
checkout layout. Python is only a local maintenance tool; the server needs no
Python, Node, database or frontend build system.

## Presentation

The artwork remains the full-page background, with the catalogue in translucent
panels. App artwork is referenced directly from each app's own site, with
referrers suppressed. Names and links remain usable if artwork cannot load.
Edit `templates/directory.html` or `styles.css` for presentation changes, then
regenerate; do not hand-edit generated app links in `index.html`.

## Publish on the existing DreamHost host

The source checkout is `~/pwa`; the public web directory is
`~/basecentral.link`. Run under the hosting account:

```sh
bash "$HOME/pwa/scripts/deploy.sh" --dry-run "$HOME/basecentral.link"
bash "$HOME/pwa/scripts/deploy.sh" --verify "$HOME/basecentral.link"
```

A normal deployment requires a clean tracked branch, fetches and pulls with
`--ff-only`, validates the generated directory and stages the complete public
set. Assets publish before HTML. The four-file public allowlist is unchanged:

```text
index.html
styles.css
favicon.svg
assets/BaseCentral.jpg
```

Configuration, templates, Git history and development tools stay outside the
public directory. Unrelated host files are preserved. Publication is atomic per
file, not for the whole release. If new deployment code/profile arrives during
a pull, review it and rerun. No app migrations, credentials, DNS or hosting
settings are changed by this command.

`--dry-run` checks the currently checked-out files without fetching, writing,
creating locks or making HTTP requests. To preview the latest source, manually
pull first. `--verify` deploys and then runs the configured public HTTP check;
that check alone does not prove every linked app's functionality.

See [the shared deployment contract](docs/SHARED_DEPLOYMENT.md).

## Checks

```sh
python3 tests/test_directory.py
python3 scripts/build-directory.py --check
python3 scripts/test-deploy.py
node tests/directory-browser.cjs
git diff --check
```

The Python tests use synthetic apps and disposable local Git repositories.
Browser checks use optional local Playwright/Chromium development tooling;
`PLAYWRIGHT_PATH` and `CHROMIUM_PATH` can select installed tools. They cover
no-JavaScript links, narrow/desktop widths, keyboard navigation, enlarged text,
image failure and referrer suppression. See [catalogue notes](docs/DIRECTORY.md).

## Shared collection resources

- [Agent development baseline](AGENTS.md)
- [Shared principles](docs/PRINCIPLES.md)
- [Application registry](docs/APPS.md)
- [Control gallery](shared/controls/gallery.html) and [integration guide](shared/controls/README.md)
- [Shared controls/deployment implementation report](docs/SHARED_IMPLEMENTATION_REPORT.md)

Common controls and deployment code are maintained here and copied locally into
each app. `scripts/sync-controls.py --check` and `scripts/sync-deploy.py --check`
detect drift. The directory does not create a runtime dependency for the apps.
