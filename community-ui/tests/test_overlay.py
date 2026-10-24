"""Structural tests for the Weblate Community UI override."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / "overlay" / "templates"
STATIC = ROOT / "overlay" / "static" / "community-ui"

class TemplateContract(unittest.TestCase):
    def test_templates_exist(self):
        for name in ("snippets/meta-css.html", "dashboard/anonymous.html", "projects.html", "list-projects.html"):
            self.assertTrue((TEMPLATES / name).is_file(), name)

    def test_upstream_dynamic_workflows_remain_in_place(self):
        meta = (TEMPLATES / "snippets/meta-css.html").read_text()
        for value in ("styles/main.css", "style-dark.css", "css-custom", "bootstrap5_rtl.css"):
            self.assertIn(value, meta)
        self.assertIn("{% announcements %}", (TEMPLATES / "dashboard/anonymous.html").read_text())
        self.assertIn("top_projects", (TEMPLATES / "dashboard/anonymous.html").read_text())
        projects = (TEMPLATES / "list-projects.html").read_text()
        for value in ("project.stats.translated_percent", 'include "snippets/list-objects.html"', "project.get_absolute_url"):
            self.assertIn(value, projects)

    def test_no_secrets_or_admin_api_tokens_in_frontend(self):
        joined = "\n".join(p.read_text() for p in STATIC.iterdir())
        for value in ("POSTGRES_PASSWORD", "Authorization: Bearer", "API_TOKEN", "csrf_exempt"):
            self.assertNotIn(value, joined)

    def test_client_filter_does_not_fetch_external_data(self):
        script = (STATIC / "projects.js").read_text()
        for fragment in ("DOMContentLoaded", "card.hidden"):
            self.assertIn(fragment, script)
        self.assertNotIn("fetch(", script)

    def test_dockerfile_has_fixed_base(self):
        content = (ROOT / "Dockerfile").read_text()
        self.assertIn("weblate/weblate:2026.10.1.2", content)
        self.assertNotIn("weblate/weblate:latest", content)
        self.assertIn("USER 1000", content)

if __name__ == "__main__":
    unittest.main()
