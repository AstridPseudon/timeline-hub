"""Real admitted closure consumers; these checks do not launch render tasks."""
import json
import os
from pathlib import Path

import pytest

from astrid.core.execution import remotion_closure as closure


def test_retained_consumer_matches_canonical_patch_producer():
    source = Path(__file__).resolve().parents[3]
    manifest = json.loads((source / 'remotion/patches/renderer-4.0.509-retained-transport.json').read_text())
    expected = {entry['path'].removeprefix('dist/'): entry['after_sha256']
                for entry in manifest['files']}
    assert closure._RETAINED_TRANSPORT_PATCHES == expected


@pytest.mark.parametrize('generation', ['current', 'legacy'])
def test_real_admitted_closure_requires_current_retained_postimages(generation):
    key = 'ASTRID_TEST_REMOTION_ADMITTED_BINDING' if generation == 'current' else 'ASTRID_TEST_REMOTION_LEGACY_BINDING'
    raw = os.environ.get(key)
    if not raw:
        pytest.skip('requires explicitly admitted read-only renderer fixtures')
    record = json.loads(Path(raw).read_text())
    project = Path(record['derived_project'])
    binding = closure.RemotionClosureBinding.admit(
        project=project, installed_project=project,
        verification_receipt=record['path'], receipt_sha256=record['sha256'],
        manifest_sha256=record['manifest_sha256'], lock_sha256=record['lock_sha256'])
    assert binding.validate(project) == project / 'node_modules/@remotion/cli/remotion-cli.js'
    if generation == 'current':
        binding.require_retained_transport()
    else:
        # The previously admitted graph is still valid SRI input, but its old
        # BrowserRunner must not qualify as the current retained transport.
        with pytest.raises(ValueError, match='qualified retained transport postimages'):
            binding.require_retained_transport()
