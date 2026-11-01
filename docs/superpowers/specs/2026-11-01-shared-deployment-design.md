# Shared deployment tools

Status: proposed for review, 1 November 2026. No deployment changes or production
actions have been performed. Separate from the approved shared-controls design.

## User intent

The user observed that deployment scripts have too many variants despite doing
mostly the same job. Consolidate the repeated machinery and operator interface
while retaining genuine application contracts. Local implementation and tests
do not authorize SSH, production writes, credentials, database migrations, user
provisioning, pushes or publication.

## Findings from current source

- The toolbox, Festival and Elementar fetch/pull and publish allowlisted assets.
- a4 and Freezer copy files; the operator is expected to pull separately.
- Flip can clone automatically, then pulls and copies its hardcoded list.
- Eternal Timer's `manual_deploy.sh` is a one-line SSH/git-pull command.
- Sopa de Letras uses recursive rsync deletion and continues if its pull fails.
- Balance adds backups, stale-file deletion, build contracts and HTTP checks.
- Oficina adds managed Apache/PHP files, staged version-query rewriting,
  cleanup and optional security-header checks. Private sync state is excluded.
- Doctools already requires hashed immutable releases and an atomic `current`
  symlink switch; do not substitute per-file copies.
- Agenda is a PHP/MariaDB application with private code, Composer dependencies,
  reviewed migrations and workers, not a static-file deployment.
- FuelLog and Govio document hosting procedures but do not have an equivalent
  general host-side publication script in the inspected checkout.

Proposed scope includes new local wrappers/profiles for FuelLog and Govio, as
well as consolidation of the existing static scripts. Their current documented
public PHP endpoints and vendor assets remain included; no server configuration
or dependency download is performed implicitly. This is a builder's proposal,
not an assertion that the user has approved replacing their hosting procedures.
Agenda receives documentation/preflight alignment only in this work; a new
server-release automation is a separate project.

## Common command and implementation

Builder's proposed choice: canonical Bash 3-compatible deployment code maintained
in `pwa/shared/deploy/`, copied into each participating app. A tiny app wrapper
loads that local copy and the app's reviewed profile. The server never downloads
executable deployment code from the toolbox and needs no Node/Python runtime.

Use the common interface `scripts/deploy.sh [--dry-run] [--verify] [DESTINATION]`.
Existing entry points and documented environment overrides remain compatibility
wrappers. `--help` exits successfully. Destinations must already exist, be
absolute and writable. Keep configured app defaults; require an explicit target
where the app has none. Do not guess a production path.

The shared engine owns argument parsing, path validation, locking, clean/upstream
checks, fast-forward-only pulls, public manifests, staging, permissions, compare
verification, cleanup, logging and honest failure status. Profiles own source
roots, public-file lists, publication order, destination defaults, header policy,
backup policy and narrowly defined validation/verification hooks.

`--dry-run` is read-only: no fetch/pull, locks, directory creation, backups,
public writes, HTTP requests or pruning. It reports the local commit and pending
checks rather than claiming it previews an unfetched remote release. Normal runs
fail closed on a failed fetch/pull, dirty/untracked checkout, detached HEAD,
missing upstream, local-only/divergent commits or changed sources during staging.
No reset, clean, stash, push or implicit clone.

Validate every path component, not just the final file. Reject traversal,
duplicates, symlinks in source/target paths, overlapping checkout/public roots,
non-regular public files and malformed manifests. Only reviewed public allowlists
are publishable; a developer file cannot become public merely by being added to
an inventory. Preserve unrelated files and private state.

Stage the entire validated set on the destination filesystem before publication.
Use 0644 regular files and 0755 created directories, then compare staged bytes.
Publish ordinary assets first, HTML next and worker/update metadata last.
Document per-file atomicity honestly. Keep all code that executes around a pull
loaded before that pull; profile/inventory changes from upstream require renewed
validation before publication. Abort if the checked commit or sources change.

## Explicit differences that remain

- Static copy mode: central toolbox and ordinary static apps share the same core.
- Release-link mode: Doctools keeps complete inventory/hash verification,
  immutable releases, existing path layout and rollback before switching only
  the owned `current` link. This is an explicit strategy, not permission for the
  static engine to follow arbitrary symlink destinations.
- Server app boundary: Agenda may share read-only preflight and command naming;
  its PHP release/private-path process stays separate. Do not invent a static
  deployment that publishes only `public/` while omitting its matching private
  application code. Migrations, SMTP and cron remain explicit operator actions.
- Oficina retains its public PHP allowlist, security headers and cache-query
  preparation; no private configuration, SQLite or operator backup is copied.
- Balance retains release consistency checks, backups and optional live checks.
  A required backup failure blocks publication rather than continuing silently.
- Header policy is explicit per profile: preserve existing host-owned files,
  install a reviewed template only when absent, or manage an app-owned config.
  Never replace an existing `.htaccess` with a generic shared template.
- Delete nothing by default. Apps that need obsolete public assets removed use
  an explicit reviewed managed-file policy based on the previous successful
  deployment inventory. Never sweep unrelated directory contents or use broad
  `rsync --delete`. Record the policy change in the app's deployment guide.
- HTTP verification runs only with `--verify`, using the profile's URL and
  app-specific status/header expectations. No automatic requests during tests.

## Packaging and tests

Maintain shared source, version and sync/check tooling centrally; vendor local
copies and app configuration so every checkout deploys independently. Keep
operational code outside public-file inventories. Update app instructions and
old entry points to point to the common command and describe real exceptions.

Test only temporary local repositories, fake upstreams and temporary web roots.
Pin successful publication and preservation, pull failures, divergent/dirty
checkouts, source/target overlap, nested symlinks, traversal, incomplete/stale
manifests, lock ownership, staging failure, publication order and cleanup. Prove
dry-run leaves Git and both filesystem trees unchanged. Test app hooks and
Doctools release-switch rollback separately. No production hosts or credentials.

Acceptance: duplicated deployment mechanics are removed for the static apps,
the operator command is consistent, existing security/release contracts remain
explicit, and local isolated regressions demonstrate the common safeguards.
