from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


class DiscoverOverlayTest(unittest.TestCase):
    WORKSPACE_ROOT = Path("tests/fixtures/workspace")

    def test_discover_overlay_candidates(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                "scripts/discover-overlay.py",
                "--workspace-root",
                str(self.WORKSPACE_ROOT),
                "--name",
                "Fixture Repo",
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        payload = json.loads(result.stdout)
        self.assertEqual("Fixture Repo", payload["name"])
        self.assertIn("force-app/child", payload["packaging"]["package_dirs"])
        self.assertIn("force-app/child/main/default/classes", payload["source"]["apex"])
        self.assertIn("docs/specs/order-spec.md", payload["docs"]["specs"])
        self.assertIn("docs/design/solution.md", payload["docs"]["technical"])
        self.assertIn(
            "force-app/child/main/default/permissionsets/Fixture_User.permissionset-meta.xml",
            payload["security"]["permission_sets"]["user"],
        )
        self.assertIn("npm run lint", payload["quality_gates"]["lint"])
        self.assertTrue(payload["quality_gates"]["static_analysis"]["commands"])


if __name__ == "__main__":
    unittest.main()
