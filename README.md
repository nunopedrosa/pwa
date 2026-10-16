# trekm PWA toolbox

Central working project for the trekm collection of local-first Progressive Web Apps. The public toolbox's new address is [basecentral.link](https://basecentral.link/). Hosting and live availability have not yet been verified.

Each application keeps its own development folder, Git repository and deployed site. This project holds shared goals, decisions and an app directory; it does not hold application data or provide a shared backend.

## Applications

| Application | Purpose | Site |
| --- | --- | --- |
| FuelLog | Vehicle fill-ups, fuel consumption and costs | [fuel.trekm.com](https://fuel.trekm.com/) |
| Eternal Timer | Multiple stopwatches and countdown timers | [timers.trekm.com](https://timers.trekm.com/) |

## Working documents

- [Agent development baseline](AGENTS.md) — reusable guidance adapted from FuelLog, with instructions for adoption by other PWAs.
- [Shared principles](docs/PRINCIPLES.md)
- [Application registry](docs/APPS.md)
- [Decisions and roadmap](docs/ROADMAP.md)
- [Toolbox design](docs/superpowers/specs/2026-10-08-toolbox-design.md)

## Project boundaries

Use this project for cross-app goals, the directory and toolbox page. Implement and test app-specific changes in the application's own folder. Shared principles express the collection's goals; the registry records current capabilities and differences rather than assuming all apps already satisfy every goal.

## Toolbox page

The toolbox is implemented as public `index.html`, `styles.css`, `favicon.svg` and `assets/BaseCentral.jpg`. It uses no runtime JavaScript, backend, build step, analytics or local data storage.

Each app's artwork is referenced directly from its own site:

- `https://fuel.trekm.com/icons/icon.svg`
- `https://timers.trekm.com/icons/icon.svg`

The artwork is not copied here. Fixed-size artwork frames keep the layout stable when images are unavailable, and app names and links remain usable. Image requests explicitly suppress referrers.

## Local preview

From the project folder, run:

```sh
python3 -m http.server 8000 --bind 127.0.0.1
```

Open http://127.0.0.1:8000/. The directory itself does not install a service worker or promise offline availability. Each linked PWA handles its own installation and offline behavior.

## Adding an application

1. Add an app entry in `index.html` with its public name, short description, HTTPS URL and artwork URL. Keep images decorative with empty alternative text and `referrerpolicy="no-referrer"`.
2. Add its folder, repository, storage, backup and offline details to `docs/APPS.md`.
3. Update the applications table in this README.
4. Check the page on a narrow screen and with the artwork request blocked. Check keyboard focus and the destination link.

## Deployment to basecentral.link

Configure the hostname and HTTPS with the hosting provider. The existing apps document DreamHost hosting; this toolbox also works on any static host.

Upload **only** these files to the domain's public web root:

```text
index.html
styles.css
favicon.svg
assets/BaseCentral.jpg
```

Keep `AGENTS.md`, this README, `docs/` and `.git/` outside the public web root. The public assets are ready for upload; this project has not been deployed by this chat. Hosting access and the actual web-root path must be confirmed before publication.

### Pull and publish on the host

After committing and pushing this project to GitHub, connect to the host by SSH. Keep the source checkout outside the public web directory. For a new checkout:

```sh
mkdir -p "$HOME/repos"
git clone https://github.com/nunopedrosa/pwa.git "$HOME/repos/pwa"
```

If your checkout already exists outside the public web directory, use its path instead. Run the deployment script on the host:

```sh
sh "$HOME/repos/pwa/scripts/deploy.sh" "$HOME/basecentral.link"
```

Replace the last argument with `basecentral.link`'s actual, existing web directory from your hosting settings. That directory must be writable by your SSH user. The same command performs the first publication and subsequent updates, and can be run from any current directory. Git must already be able to pull from the checkout's configured upstream; the script does not configure credentials, DNS or hosting.

The script:

- Requires a clean checkout on a branch that tracks a remote branch.
- Runs `git pull --ff-only` and refuses to deploy host-only commits.
- Requires the checkout and public directory to be separate, non-overlapping paths.
- Validates every published source file and destination entry before publication.
- Copies only `index.html`, `styles.css`, `favicon.svg` and `assets/BaseCentral.jpg`; other host files, including `.htaccess`, stay in place.
- Stages the files before replacing them, with readable permissions. Each file replacement is atomic, but the published set is not one atomic release.
- Prints the deployed commit and directory. It does not verify DNS, HTTPS or live site availability.

When a pull or validation fails, the published files are left unchanged. If a failure occurs during the final file replacements, publication may be partial; correct the reported problem and rerun the command. The script does not reset Git, discard local work or remove unrelated host files.

The deployment regression checks use temporary local repositories and no network:

```sh
python3 scripts/test-deploy.py
```

Python is needed only for these checks; the host deployment script uses a POSIX shell, Git and standard file utilities.

## Verification

Checked on 2026-10-08 in headless Chrome: desktop and 320 px layouts, enlarged text, keyboard focus, exact links, artwork failure behavior, request domains and referrer suppression. Both artwork URLs returned HTTP 200. Normal text and action contrast were checked. No page JavaScript errors occurred. No Safari 12 or physical iPhone verification was performed, and the toolbox domain's deployment has not been verified.
