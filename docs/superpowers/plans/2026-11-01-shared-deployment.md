# Shared Deployment Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans in this chat. No production actions.

**Goal:** one local common engine, reviewed app-owned profiles and a consistent command.
**Spec:** ../specs/2026-11-01-shared-deployment-design.md
**Architecture:** Bash 3 core vendored independently; copy strategy for static apps, verified release-link strategy for Doctools, documentation/preflight boundary for Agenda.

- [x] Add isolated failing Git/filesystem tests before implementation.
- [x] Implement clean tracked upstream preflight, read-only dry run, fail-closed pull, locks, explicit inventory/path checks, full staging and metadata-last copy.
- [x] Integrate app profiles and preserve Oficina transformations/private allowlist, Festival headers, Balance backup and Doctools immutable hashes.
- [x] Add local synchronization/check tooling and documented compatibility entry points; remove broad deletion and implicit SSH/clone.
- [x] Extend failure/permissions tests and run app-specific legacy fixtures with the new local core/profile files.
- [x] Independently review all changes, fix important findings and record verification/remaining device checks.
