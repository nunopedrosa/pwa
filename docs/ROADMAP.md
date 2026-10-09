# Decisions and roadmap

## Agreed decisions

### 2026-10-08: Central working project

Use `/Users/nfp/github/pwa/` and https://github.com/nunopedrosa/pwa for shared concepts, goals and an application registry. Keep application development in separate folders and sites.

### 2026-10-08: Public toolbox

Provide a simple page at https://pwa.trekm.com/ with references to the individual apps. Initially include FuelLog and Eternal Timer. The toolbox must not become a runtime dependency of either application.

### 2026-10-08: Local-first direction

Favor on-device operation, offline core workflows, user-controlled data and minimal server support across the collection. Record app-specific exceptions in the registry.

### 2026-10-08: Reuse application artwork

Use the applications' existing artwork as the public directory's visual anchors, referenced directly from their own sites. Do not copy app artwork into the central repository. Keep the directory usable when an image is unavailable.

## Next steps

The central `AGENTS.md` now provides shared development guidance adapted from FuelLog. Adoption by sibling app repositories requires an explicit reference or reviewed copy in their own agent instructions; their existing instructions have not been changed.

1. Point `basecentral.link` at its static web host, confirm the web-root path, and enable HTTPS.
2. Publish the three public assets to the new domain and verify the live page and artwork behavior.
3. Add further apps as their names and site URLs are supplied.

## Implementation status

The user approved the design and direct execution of the plan. On 2026-10-08, the static toolbox was implemented and checked in headless Chrome on desktop, at 320 px width, with enlarged text and with artwork blocked. Keyboard focus and referrer suppression passed, and both live artwork URLs returned HTTP 200. Shared agent instructions and the app registry are present. Publication remains pending; there is no claim of Safari 12 or physical-device verification.

## 2026-10-09: Toolbox address change

The original `pwa.trekm.com` target recorded above and in the first approved design was superseded by the user's request to move the toolbox to `https://basecentral.link/`. The canonical README, deployment instructions and host deploy-script usage now reflect the new domain. This changes the intended domain only; the toolbox page has not yet been published at the new address. DNS, the new web-root path, HTTPS and any handling of the former domain remain to be configured and verified.

## Future decisions

Consider an installable, offline toolbox only if there is a practical need. Consider shared code or optional synchronization only when a concrete requirement justifies them.
