# Shared principles

## Purpose

Provide useful, focused applications that work primarily on the user's device, remain useful offline and need minimal ongoing server support.

## Local operation

- Store personal working data on the device by default.
- Perform normal calculations and processing locally.
- Make core functions usable offline after the application has been loaded and cached.
- Describe online-only features clearly, including their external dependencies.
- Treat accounts and synchronization as optional future decisions, not prerequisites.

## Small server footprint

- Prefer static hosting and small payloads.
- Introduce server-side components only for a concrete requirement and document why they are necessary.
- Keep optional online features separate from core local workflows.
- Avoid background requests unless they serve a documented purpose.

## Data ownership and portability

- Provide a practical way to export and restore user data.
- Explain that browser storage is specific to a device, browser and site origin, and can be cleared.
- Preserve data when updating the app; document migrations and recovery where needed.
- Do not add analytics, tracking or data uploads by default.

## Independent applications

- Each PWA has its own folder, repository, site and release lifecycle.
- The toolbox links to applications; it does not embed them or read their data.
- Each app manages its own storage, cache and service worker scope.
- Each app states its supported browsers and devices. Existing app compatibility requirements are not automatically requirements for every app.
- Share documented patterns first; extract common code only when repeated needs justify a dependency.

## Usability

- Keep interfaces focused, responsive and accessible.
- Use descriptive labels, visible keyboard focus and clear feedback.
- Prefer simple implementations with few dependencies and document any required build process.

These are development goals. Current behavior must be checked in each app's documentation and implementation.
