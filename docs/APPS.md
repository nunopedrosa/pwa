# Application registry

Registry updated: 2026-10-08. Repository paths are development references, not public toolbox content. Site URLs are configured targets; this registry does not claim a live health check.

## FuelLog

- Purpose: log vehicle fill-ups and analyze fuel consumption and costs.
- Folder: `/Users/nfp/github/fuel/`
- Repository: https://github.com/nunopedrosa/fuel
- Site: https://fuel.trekm.com/
- Local storage: IndexedDB.
- Offline core: vehicle records, fuel logging and analysis, according to the app README.
- Portability: JSON backup and CSV export; several import formats.
- Optional online features: external fuel-price providers, maps and a same-origin PHP station proxy.
- Hosting: static assets on DreamHost, with optional PHP support for the station proxy.
- Compatibility: app documentation explicitly includes iPhone 6 / iOS 12.5.7 requirements.
- Source for these details: the application's README. Changes belong in its own repository.

## Eternal Timer

- Purpose: manage multiple stopwatches and countdown timers.
- Folder: `/Users/nfp/github/eternytimer/`
- Repository: https://github.com/nunopedrosa/eternytimer
- Site: https://timers.trekm.com/
- Local storage: browser localStorage.
- Offline core: PWA offline support, according to the app README.
- Portability: CSV export and import.
- Server requirements: static files; no application backend.
- Hosting: DreamHost, according to the app's deployment instructions.
- Source for these details: the application's README. The public app title is Eternal Timer; the development folder and repository are named eternytimer.

## Registering another app

Record its name, purpose, folder, repository, site, local storage, offline behavior, import/export support and any online dependencies. Add its public name, brief description and HTTPS link to the toolbox page when that page is implemented. Update this registry and the README at the same time.
