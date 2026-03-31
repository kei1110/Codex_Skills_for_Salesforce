from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

from scripts import overlay_resolver


@unittest.skipUnless(overlay_resolver.yaml_available(), "PyYAML が未導入")
class ContextPruningTest(unittest.TestCase):
    WORKSPACE_ROOT = Path("tests/fixtures/workspace")

    def run_pruner(self, changed_file: str) -> dict[str, object]:
        result = subprocess.run(
            [
                sys.executable,
                "scripts/prune-context.py",
                "--overlay",
                "tests/fixtures/overlays/repos/child.yaml",
                "--changed-file",
                changed_file,
                "--workspace-root",
                str(self.WORKSPACE_ROOT),
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        return json.loads(result.stdout)

    def test_apex_change_adds_test_and_docs(self) -> None:
        result = self.run_pruner("force-app/child/main/default/classes/Foo.cls")
        self.assertIn("force-app/child/main/default/classes/Foo.cls", result["selected"]["source"])
        self.assertIn("force-app/child/main/default/classes/FooTest.cls", result["selected"]["tests"])
        self.assertIn("docs/specs/child-spec.md", result["selected"]["docs"])
        self.assertIn("force-app/child/main/default/classes/Bar.cls", result["selected"]["source"])
        self.assertIn("force-app/child", result["selected"]["metadata"])

    def test_lwc_change_adds_component_and_jest(self) -> None:
        result = self.run_pruner("force-app/child/main/default/lwc/foo/foo.js")
        self.assertIn("force-app/child/main/default/lwc/foo", result["selected"]["source"])
        self.assertIn("force-app/child/main/default/lwc/foo/__tests__", result["selected"]["tests"])
        self.assertIn("force-app/child/main/default/classes/FooController.cls", result["selected"]["source"])
        self.assertIn("force-app/child/main/default/lwc/bar", result["selected"]["source"])

    def test_metadata_change_adds_metadata_bucket(self) -> None:
        changed = "force-app/child/main/default/flows/OrderFlow.flow-meta.xml"
        result = self.run_pruner(changed)
        self.assertIn(changed, result["selected"]["metadata"])
        self.assertIn("docs/technical/child-technical.md", result["selected"]["docs"])
        self.assertIn("force-app/child", result["selected"]["metadata"])


if __name__ == "__main__":
    unittest.main()
