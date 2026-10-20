import importlib.util
import json
import re
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
GENERATOR = ROOT / "scripts" / "gen_effect_registry.py"

_SPEC = importlib.util.spec_from_file_location("gen_effect_registry_elements_test", GENERATOR)
assert _SPEC is not None
gen_effect_registry = importlib.util.module_from_spec(_SPEC)
sys.modules[_SPEC.name] = gen_effect_registry
assert _SPEC.loader is not None
_SPEC.loader.exec_module(gen_effect_registry)


class RemotionElementGenerationTest(unittest.TestCase):
    def test_generated_registries_use_element_scope_aliases(self) -> None:
        for kind in ("effects", "animations", "transitions"):
            generated = gen_effect_registry.generate_element_registry(kind)
            self.assertIn("@banodoco/timeline-composition/theme-api", generated)
            self.assertNotIn("./effects.types", generated)
            self.assertNotIn("@workspace-", generated)
            self.assertNotIn("primitive-root", generated)
        self.assertIn("@pack-rendering-elements-effects/audio-reactive-colour/component", gen_effect_registry.generate_element_registry("effects"))

    def test_source_less_public_descriptor_yields_to_component_override(self) -> None:
        from astrid.core.element.registry import ElementRegistry
        from astrid.core.element.schema import ElementDefinition

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            override_root = root / "local" / "fade"
            override_root.mkdir(parents=True)
            component = override_root / "component.tsx"
            component.write_text("export default function FadeOverride() { return null; }\n", encoding="utf-8")
            public_root = root / "public" / "fade"
            public_root.mkdir(parents=True)

            public_descriptor = ElementDefinition(
                id="fade", kind="animations", root=public_root, source="pack:rendering",
                editable=False, priority=30, component=public_root / "component.tsx",
                schema={}, defaults={"durationFrames": 12},
                metadata={"pack_id": "rendering", "kind": "wrapper"},
                runtime={"adapter": "remotion"},
            )
            override = ElementDefinition(
                id="fade", kind="animations", root=override_root, source="pack:local",
                editable=True, priority=0, component=component, schema={},
                defaults={"durationFrames": 24}, metadata={"pack_id": "local"},
                runtime={"adapter": "remotion"},
            )
            old_registry = gen_effect_registry._element_registry
            gen_effect_registry._element_registry = lambda: ElementRegistry(
                (public_descriptor, override)
            )
            try:
                generated = gen_effect_registry.generate_element_registry("animations")
            finally:
                gen_effect_registry._element_registry = old_registry

        self.assertIn("'fade'", generated)
        self.assertIn("@pack-local-elements-animations/fade/component", generated)
        self.assertNotIn("@pack-rendering-elements-animations/fade/component", generated)

    def test_default_local_component_wins_source_less_public_descriptor(self) -> None:
        from astrid.core.element.registry import load_default_registry

        registry = load_default_registry(project_root=ROOT)
        winner = registry.get("effects", "text-card")
        self.assertEqual(winner.source, "pack:rendering")
        self.assertFalse(winner.component.is_file())
        self.assertEqual(winner.metadata["pack_id"], "rendering")

        generated = gen_effect_registry.generate_element_registry("effects")
        self.assertIn("@pack-local-elements-effects/text-card/component", generated)
        self.assertNotIn("@pack-rendering-elements-effects/text-card/component", generated)

    def test_missing_non_public_component_is_diagnostic(self) -> None:
        from astrid.core.element.registry import ElementRegistry
        from astrid.core.element.schema import ElementDefinition

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "custom" / "missing"
            root.mkdir(parents=True)
            missing = ElementDefinition(
                id="missing", kind="effects", root=root, source="pack:custom",
                editable=True, priority=0, component=root / "component.tsx",
                schema={}, defaults={}, metadata={"pack_id": "custom"},
                runtime={"adapter": "remotion"},
            )
            old_registry = gen_effect_registry._element_registry
            gen_effect_registry._element_registry = lambda: ElementRegistry((missing,))
            try:
                with self.assertRaisesRegex(ValueError, "broken custom component"):
                    gen_effect_registry.generate_element_registry("effects")
            finally:
                gen_effect_registry._element_registry = old_registry

    def test_remotion_alias_files_do_not_reference_workspace_element_aliases(self) -> None:
        checked = [
            ROOT / "scripts" / "gen_effect_registry.py",
            ROOT / "remotion" / "tsconfig.json",
        ]
        for path in checked:
            text = path.read_text(encoding="utf-8")
            self.assertNotIn("@workspace-", text)
            self.assertNotIn("workspace-effects", text)
            self.assertNotIn("workspace-animations", text)
            self.assertNotIn("workspace-transitions", text)

    def test_generated_effect_registry_hashes_manifest_component_support_and_assets(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            project = workspace / "project"
            local_pack = project / "astrid" / "packs" / "local"
            element_root = local_pack / "elements" / "effects" / "fingerprint-probe"
            assets_root = element_root / "assets"
            assets_root.mkdir(parents=True)
            (local_pack / "pack.yaml").write_text(
                "schema_version: 2\nid: local\nname: Local\nversion: 0.1.0\n"
                "capabilities: [elements]\n",
                encoding="utf-8",
            )
            component = element_root / "component.tsx"
            support_file = element_root / "support.css"
            asset = assets_root / "badge.txt"
            manifest = element_root / "element.yaml"

            component.write_text(
                "export default function FingerprintProbe() { return null; }\n",
                encoding="utf-8",
            )
            support_file.write_text(".fingerprint-probe { color: red; }\n", encoding="utf-8")
            asset.write_text("badge-v1\n", encoding="utf-8")
            manifest.write_text(
                json.dumps(
                    {
                        "id": "fingerprint-probe",
                        "kind": "effect",
                        "pack_id": "local",
                        "metadata": {"label": "Fingerprint Probe"},
                        "schema": {"type": "object"},
                        "defaults": {},
                        "assets": {"badge": "assets/badge.txt"},
                    },
                    sort_keys=True,
                )
                + "\n",
                encoding="utf-8",
            )

            from astrid.core.element import registry as element_registry
            from astrid.core.pack import discover_packs as real_discover_packs

            old_tools_dir = gen_effect_registry.TOOLS_DIR
            old_discover = element_registry.discover_packs

            def generated_fingerprint_and_import() -> tuple[str, str]:
                generated = gen_effect_registry.generate_element_registry("effects")
                fingerprint_match = re.search(
                    r"'fingerprint-probe': '([0-9a-f]{64})'",
                    generated,
                )
                self.assertIsNotNone(fingerprint_match)
                fingerprint = fingerprint_match.group(1)
                import_match = re.search(
                    r"import FingerprintProbe from '([^']+)';",
                    generated,
                )
                self.assertIsNotNone(import_match)
                import_path = import_match.group(1)
                self.assertEqual(
                    import_path,
                    "@pack-local-elements-effects/fingerprint-probe/component"
                    f"?astrid={fingerprint[:12]}",
                )
                self.assertIn(
                    "export const EFFECT_FINGERPRINTS: Record<EffectId, string> = {",
                    generated,
                )
                return fingerprint, import_path

            try:
                gen_effect_registry.TOOLS_DIR = project
                element_registry.discover_packs = (
                    lambda root=None: real_discover_packs(local_pack.parent)
                )

                original = generated_fingerprint_and_import()
                self.assertEqual(original, generated_fingerprint_and_import())

                component.write_text(
                    "export default function FingerprintProbe() { return 'component-v2'; }\n",
                    encoding="utf-8",
                )
                after_component = generated_fingerprint_and_import()
                self.assertNotEqual(original, after_component)

                component.write_text(
                    "export default function FingerprintProbe() { return null; }\n",
                    encoding="utf-8",
                )
                self.assertEqual(original, generated_fingerprint_and_import())

                support_file.write_text(
                    ".fingerprint-probe { color: blue; }\n",
                    encoding="utf-8",
                )
                after_support = generated_fingerprint_and_import()
                self.assertNotEqual(original, after_support)

                support_file.write_text(
                    ".fingerprint-probe { color: red; }\n",
                    encoding="utf-8",
                )
                self.assertEqual(original, generated_fingerprint_and_import())

                asset.write_text("badge-v2\n", encoding="utf-8")
                after_asset = generated_fingerprint_and_import()
                self.assertNotEqual(original, after_asset)

                asset.write_text("badge-v1\n", encoding="utf-8")
                self.assertEqual(original, generated_fingerprint_and_import())

                payload = json.loads(manifest.read_text(encoding="utf-8"))
                payload["metadata"]["label"] = "Fingerprint Probe v2"
                manifest.write_text(
                    json.dumps(payload, sort_keys=True) + "\n",
                    encoding="utf-8",
                )
                after_manifest = generated_fingerprint_and_import()
                self.assertNotEqual(original, after_manifest)
            finally:
                gen_effect_registry.TOOLS_DIR = old_tools_dir
                element_registry.discover_packs = old_discover


if __name__ == "__main__":
    unittest.main()
