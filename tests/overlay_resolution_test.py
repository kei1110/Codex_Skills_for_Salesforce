from __future__ import annotations

import unittest
from pathlib import Path

from scripts import overlay_resolver


class OverlayResolverUnitTest(unittest.TestCase):
    def test_merge_overlay_prefers_child_scalar(self) -> None:
        parent = overlay_resolver.normalize_overlay(
            {
                "kind": "workflow",
                "name": "parent",
                "quality_gates": {"api_version_check": "check-a"},
            }
        )
        child = {
            "kind": "repo",
            "name": "child",
            "quality_gates": {"api_version_check": "check-b"},
        }
        merged = overlay_resolver.merge_overlay(parent, child)
        self.assertEqual("check-b", merged["quality_gates"]["api_version_check"])
        self.assertEqual("repo", merged["kind"])
        self.assertEqual("child", merged["name"])

    def test_merge_overlay_dedupes_lists(self) -> None:
        parent = overlay_resolver.normalize_overlay(
            {
                "kind": "workflow",
                "name": "parent",
                "notes": ["a", "b"],
                "source": {"apex": ["force-app/base"]},
            }
        )
        child = {
            "kind": "repo",
            "name": "child",
            "notes": ["b", "c"],
            "source": {"apex": ["force-app/base", "force-app/child"]},
        }
        merged = overlay_resolver.merge_overlay(parent, child)
        self.assertEqual(["a", "b", "c"], merged["notes"])
        self.assertEqual(["force-app/base", "force-app/child"], merged["source"]["apex"])

    def test_merge_overlay_list_replace(self) -> None:
        parent = overlay_resolver.normalize_overlay(
            {
                "kind": "workflow",
                "name": "parent",
                "source": {"apex": ["force-app/base", "force-app/common"]},
            }
        )
        child = {
            "kind": "repo",
            "name": "child",
            "source": {
                "apex": {
                    "replace": True,
                    "values": ["force-app/custom"],
                }
            },
        }
        merged = overlay_resolver.merge_overlay(parent, child)
        self.assertEqual(["force-app/custom"], merged["source"]["apex"])

    def test_merge_overlay_list_remove(self) -> None:
        parent = overlay_resolver.normalize_overlay(
            {
                "kind": "workflow",
                "name": "parent",
                "quality_gates": {"smoke_tests": ["a", "b", "c"]},
            }
        )
        child = {
            "kind": "repo",
            "name": "child",
            "quality_gates": {"smoke_tests": {"remove": ["b"]}},
        }
        merged = overlay_resolver.merge_overlay(parent, child)
        self.assertEqual(["a", "c"], merged["quality_gates"]["smoke_tests"])


@unittest.skipUnless(overlay_resolver.yaml_available(), "PyYAML が未導入")
class OverlayResolverIntegrationTest(unittest.TestCase):
    def fixture(self, relative: str) -> Path:
        return overlay_resolver.REPO_ROOT / relative

    def test_resolve_overlay_merges_parent_and_child(self) -> None:
        resolved, chain = overlay_resolver.resolve_overlay(
            self.fixture("tests/fixtures/overlays/repos/child.yaml")
        )
        self.assertEqual(
            [
                "tests/fixtures/overlays/workflows/base.yaml",
                "tests/fixtures/overlays/repos/child.yaml",
            ],
            chain,
        )
        self.assertEqual(
            [
                "force-app/base/main/default/classes",
                "force-app/child/main/default/classes",
            ],
            resolved["source"]["apex"],
        )
        self.assertEqual(["force-app/base", "force-app/child"], resolved["packaging"]["package_dirs"])
        self.assertEqual(
            ["sf apex run test --target-org child-org"],
            resolved["quality_gates"]["unit_tests"],
        )
        self.assertEqual(3, resolved["schema_version"])
        self.assertEqual(
            ["source.apex", "source.objects"],
            resolved["context_pruning"]["roots"]["source"],
        )
        self.assertEqual(
            ["pmd-json", "sfdx-scanner-json"],
            [item["parser"] for item in resolved["quality_gates"]["static_analysis"]["commands"]],
        )

    def test_invalid_key_is_reported(self) -> None:
        with self.assertRaises(overlay_resolver.OverlayError):
            overlay_resolver.resolve_overlay(
                self.fixture("tests/fixtures/overlays/repos/invalid-key.yaml")
            )

    def test_inheritance_cycle_is_reported(self) -> None:
        with self.assertRaises(overlay_resolver.OverlayError):
            overlay_resolver.resolve_overlay(
                self.fixture("tests/fixtures/overlays/repos/cycle-a.yaml")
            )

    def test_resolve_overlay_applies_list_patch(self) -> None:
        resolved, _ = overlay_resolver.resolve_overlay(
            self.fixture("tests/fixtures/overlays/repos/child-patch.yaml")
        )
        self.assertEqual(["force-app/override/main/default/classes"], resolved["source"]["apex"])
        self.assertEqual(["workflow rule", "repo rule"], resolved["quality_gates"]["blocking_rules"])
        self.assertEqual([], resolved["quality_gates"]["static_analysis"]["commands"])


if __name__ == "__main__":
    unittest.main()
