# trekm toolbox design

Date: 2026-10-08

## Intent and scope

The user wants a central working folder for the shared concepts and goals of several local-first PWAs, while each app retains its own development folder and site. The original approved design targeted https://pwa.trekm.com/ and initially included FuelLog and Eternal Timer. A later user request changes the toolbox's canonical address to https://basecentral.link/; the original target is retained here as design history.

This design covers the documentation structure and a static directory page. It does not alter either existing app or add a shared backend.

## Approach

Use a plain HTML page, local CSS and a small local SVG favicon. This supports ordinary static hosting, works without JavaScript and needs no build step. A generated catalogue would introduce a build step for only two entries; a dynamic catalogue would introduce runtime behavior without a current need. Keep the two public entries in HTML and record maintenance instructions for updating the registry at the same time.

## Public page

Show the title “trekm toolbox” and a brief introduction: “Small tools for everyday use. Open an app to get started.”

Show two clearly separated entries:

- FuelLog: “Track fill-ups, fuel consumption and costs.” Link text: “Open FuelLog”. Target: https://fuel.trekm.com/.
- Eternal Timer: “Keep multiple stopwatches and countdowns.” Link text: “Open Eternal Timer”. Target: https://timers.trekm.com/.

Display the destination hostname with each entry. Use normal links in the same tab so browser back navigation returns to the toolbox. Do not show development paths, technical implementation details or unverified availability badges on the public page.

## Visual direction

Use a compact, left-aligned tool directory on a cool light background, with a deep blue header and restrained blue accents. Base palette: white #ffffff, mist #f2f6fa, ink #172d43, blue #175da8 and slate #526579. Use local system sans-serif fonts so rendering introduces no font download. Keep the title, app names and actions legible. Use each application's existing artwork, loaded directly from its own site, as the visual anchor; do not copy that artwork into this repository or create replacement app symbols. Avoid animation and decorative imagery.

The existing source projects reference these artwork paths:

- FuelLog: `https://fuel.trekm.com/icons/icon.svg`.
- Eternal Timer: `https://timers.trekm.com/icons/icon.svg`.

Verify the deployed paths and image responses before implementation claims that they work live. Render artwork as ordinary images, with fixed display dimensions and preserved aspect ratios. The adjacent app name provides its accessible identity, so artwork may use empty alternative text. Keep the app name, description and link usable when artwork cannot load; artwork is optional and must not require a successful network request to navigate. Suppress the referrer on image requests. Each image request goes to the corresponding app's host; no other image service is needed. Changes to app artwork will follow the app host's caching policy without a separate copied asset to update here.

Implementation note, 2026-10-08: artwork uses ordinary images with explicit `referrerpolicy="no-referrer"` inside fixed 72 px frames. Image heights remain intrinsic, capped by the frame; blocked images leave blank space without broken-image boxes in the verified browser. The live artwork URLs returned HTTP 200 during Chrome verification.

Use a two-column app list on larger screens and a single column on phones, including 320 px screens. Provide semantic landmarks, one h1, descriptive link labels, visible keyboard focus and comfortable touch targets. Check contrast for all text and focus indicators.

## Files and maintenance

- `index.html`: public content and links.
- `styles.css`: responsive styling.
- `favicon.svg`: local toolbox identity.
- `README.md`: purpose, local preview, maintenance and deployment instructions.
- `docs/PRINCIPLES.md`: shared goals.
- `docs/APPS.md`: application registry.
- `docs/ROADMAP.md`: decisions and cross-app next steps.

Public assets should be independently uploadable so the documentation and .git directory need not be exposed on the web host. No package manager, application server or runtime JavaScript is required. The only remote visual assets are the two apps' own artwork; fonts, styling and the toolbox favicon stay local.

## Data and offline behavior

The toolbox stores no personal data and reads no application storage. Browser origin isolation keeps each application's data separate. Each app handles its own PWA installation and offline caching. The initial toolbox is an ordinary static page and does not promise offline availability; making the directory installable is a separate future decision.

## Hosting

Both existing projects document DreamHost hosting. Use the same static hosting model for this directory unless the user chooses otherwise. The initial target in this approved design was pwa.trekm.com. The user subsequently changed the canonical target to basecentral.link. Configure the new hostname, enable HTTPS and upload the public assets to its web root. The actual hosting account, DNS state, web-root path and deployment access have not been supplied, so the domain change is documented locally but publication requires host configuration.

## Verification

Check HTML structure, local asset references and the exact two HTTPS app links. Render the page at desktop and narrow mobile sizes; check for overflow, readable text and visible keyboard focus. Check that artwork requests are limited to the two app sites and that each image renders correctly. Block the artwork requests and confirm that app names and links remain legible and usable, without broken-image clutter or layout shifts. Confirm there are no unrelated third-party requests or JavaScript errors. Verify the two sites' availability separately before claiming deployment or link health; current web-tool attempts could not access either site.
