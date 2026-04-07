from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class BootstrapSmokeTest(unittest.TestCase):
    def test_bootstrap_installs_links_and_runs_doctor(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            env = os.environ.copy()
            env["CODEX_HOME"] = tmp
            existing_pythonpath = env.get("PYTHONPATH")
            extra_path = "/tmp/codex-skills-pydeps"
            env["PYTHONPATH"] = extra_path if not existing_pythonpath else f"{extra_path}:{existing_pythonpath}"
            result = subprocess.run(
                ["/bin/bash", "scripts/bootstrap-kit.sh"],
                capture_output=True,
                text=True,
                check=False,
                env=env,
            )
            self.assertEqual(0, result.returncode, msg=result.stdout + result.stderr)
            self.assertTrue((Path(tmp) / "salesforce-kit").is_symlink())
            self.assertTrue((Path(tmp) / "skills").is_dir())
            self.assertIn("Salesforce Codex kit doctor", result.stdout)


if __name__ == "__main__":
    unittest.main()
