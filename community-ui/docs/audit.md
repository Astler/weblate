# Weblate 2026.10.1 UI audit

Inspected upstream GitHub tag `weblate-2026.10.1`. Weblate serves Django templates with Bootstrap 5, Weblate template tags, CSS custom properties and editor scripts. Source locations:

- `weblate/templates/base.html` includes `snippets/meta-css.html`.
- `weblate/templates/dashboard/anonymous.html` renders `top_projects`.
- `weblate/templates/projects.html` includes `list-projects.html`.
- `weblate/templates/list-projects.html` includes a native permission-aware `snippets/list-objects.html` table.
- `weblate/templates/project.html` provides project-language statistics and tabs.
- `weblate/templates/translate.html` uses existing native Django forms and permissions including `unit.edit`, `suggestion.add`, `suggestion.accept`, alongside `editor/base.js` and `editor/full.js`.
- `weblate/templates/zen.html` uses `editor/zen.js`.

## Choice

Isolated four template overlays plus CSS and a client-only project filter in a derivative official image. Do not change models, API, Git sync, routing, Weblate JS handlers, form serialization or permission checks. Runtime `/app/data` remains unmodified.

## Risks

- Internal template and JS entrypoint changes may break the overlay during upstream upgrades.
- Changes to `project.stats` or template filters require auditing.
- Dark theme, RTL, admin custom CSS and upstream Bootstrap variants may interact with design tokens.
- Weblate Docker startup may apply schema migrations. Production volumes require backup, schema/version validation and staging test.
- Docker/Playwright/browser execution was unavailable during this slice. The version-pinned image has **not** been validated running with these overrides.

## Next milestones

1. Run Docker image and Playwright browser checks on populated staging.
2. Verify real guest suggestion flow and anti-abuse settings, not anonymous API token bypasses.
3. Improve project language selection.
4. Recompose editor layout carefully while preserving plural handling, hotkeys, CSRF, and reviews.
5. Add review dashboard and authenticated E2E suite.
