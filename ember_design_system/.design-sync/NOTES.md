# design-sync notes — Ember Design System

## Shape: hand-authored (off-script)

This repo is **not** a converter-shaped design system:
- No `package.json`, no lockfile, no Storybook, no `dist/` build.
- It is authored directly in Claude Design's "Design System" upload shape.
- Component preview cards (`components/<group>/<group>.card.html`) carry `@dsCard`
  headers and mount `_ds_bundle.js`, which **Claude Design compiles at runtime**
  when the project type is `DESIGN_SYSTEM`. There is nothing to bundle locally.
- `styles.css` is an `@import` manifest of `tokens/*.css`.

Because of this, the standard converter pipeline (`package-build.mjs`, render
verification, `_ds_sync.json` anchor) does not apply. Syncing = upload the repo
files as-is; the app does the rest. There is no anchor, so each sync re-uploads
the full file set (idempotent) as source-of-truth.

## Files NOT uploaded
- `Shared link-handoff.zip` — local handoff artifact, not part of the system.
- `.design-sync/` — sync metadata, local only.

## Projects in Claude Design
- `c67f2f07-7b40-4513-8cbf-30fa45e53ad3` — "Ember Design System" (original, left untouched).
- `8a927d0a-7bbd-422e-8664-faa878215640` — "Ember Design System (copy)" — this run's target (pinned in config.json).
