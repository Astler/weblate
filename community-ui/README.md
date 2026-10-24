# Weblate Community UI — 0.1.0

Non-SPA, minimally invasive UI overlay on Weblate. **Work in progress; not production certified.**

## Implemented

- Community landing page for guests with real Weblate project records and announcements.
- Projects as responsive cards with native statistics and progress; a local filter applies **only to currently paginated projects**.
- Original detailed, permission-aware project listing remains under expandable details.
- Light/dark/system CSS tokens; refined cards, forms and existing editor styling.
- Derived official Weblate Docker image, pinned Compose dependencies, persistent volumes, health checks and smoke probe.

## Not yet implemented or verified

- Full three-panel editor rewrite, standalone reviewer UI and profile redesign.
- Guest suggestion submission and reviewer acceptance/rejection: remain handled by Weblate and need E2E testing.
- Docker build, screenshot regression, browser accessibility audit and API/Git integration test.

## Source / installation

Templates audited against upstream tag `weblate-2026.10.1` and image `weblate/weblate:2026.10.1.2`. The Dockerfile copies the template/style overlay **inside the derived image** and preserves all upstream Python, Django models, Git actions, form handlers and entrypoint. Do not change tags to `latest` without compatibility review.

Files overridden in derived Docker package:

- `weblate/templates/snippets/meta-css.html`
- `weblate/templates/dashboard/anonymous.html`
- `weblate/templates/projects.html`
- `weblate/templates/list-projects.html`

New assets: `weblate/static/community-ui/theme.css` and `projects.js`.

### Coolify staging setup

1. Choose the repository `Astler/weblate`, select the feature branch and directory `/community-ui` as the Compose build directory. Compose file: `compose.yaml`.
2. Set values from `.env.example` via Coolify environment/secrets. Use an actual randomly generated `POSTGRES_PASSWORD`, correct hostname and configured SMTP address.
3. Point the Coolify HTTPS reverse proxy to Weblate port **8080**, with correct trusted proxy headers.
4. Deploy into **new** database and Weblate volumes. This Compose is for a fresh staging environment only, not existing production data.
5. Verify health, guests, languages, suggestions, forms, role permissions, translations and Git sync before any public rollout.

### CLI on staging

```sh
cd community-ui
cp .env.example .env
# Set secure secrets, hostnames and proxy-related settings first.
docker compose --env-file .env -f compose.yaml build
docker compose --env-file .env -f compose.yaml up -d
docker compose --env-file .env -f compose.yaml ps
python -m unittest discover -s tests -v
WEBLATE_URL=https://translate.example.com bash scripts/check_live.sh
```

The Weblate image may apply migrations during startup; **do not connect a production database** without full backup and staging compatibility review.

## Backups and rollback

Back up PostgreSQL and /app/data separately; a database dump alone does not contain the Git repositories or files. Quiesce writes before taking a consistent file snapshot. Keep off-server encrypted backups and test restoration.

Example DB dump:

```sh
docker compose -f compose.yaml exec -T database pg_dump -U weblate -d weblate -Fc > weblate-db.dump
```

To revert only UI, deploy upstream Weblate at the **same application version** without this overlay. Database schema downgrades are not guaranteed; for downgrades restore matching-version database plus file snapshots into fresh volumes.

## Maintenance

When upgrading Weblate, diff the four overridden templates against the new upstream sources before building. Re-test auth/CSRF, anonymous suggestions, plural forms, reviewer operations and responsive editor. All contribution remains subject to GPL-3.0-or-later and upstream copyright notices.

This feature directory intentionally does **not** patch Weblate source on the repository branch until the overlay is validated on staging.
