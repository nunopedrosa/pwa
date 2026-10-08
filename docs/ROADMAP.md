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

1. Configure HTTPS hosting for pwa.trekm.com and publish the three public assets after confirming deployment access and the web-root path.
2. Verify the published page and artwork behavior on the live toolbox domain.
3. Add further apps as their names and site URLs are supplied.

## Implementation status

The user approved the design and direct execution of the plan. On 2026-10-08, the static toolbox was implemented and checked in headless Chrome on desktop, at 320 px width, with enlarged text and with artwork blocked. Keyboard focus and referrer suppression passed, and both live artwork URLs returned HTTP 200. Shared agent instructions and the app registry are present. Publication remains pending; there is no claim of Safari 12 or physical-device verification.

## Future decisions

Consider an installable, offline toolbox only if there is a practical need. Consider shared code or optional synchronization only when a concrete requirement justifies them.
