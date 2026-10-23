"""Bounded retained/renamed/deleted payload controls for the corrected oracle."""
import importlib.util
import os
from pathlib import Path
import tempfile
import unittest

PATH = Path(__file__).with_name('handoff-runtime-OPS-bench-store-core-test-sol-1928-test-core.py')
spec = importlib.util.spec_from_file_location('fixture', PATH)
fixture = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fixture)


class OracleControls(unittest.TestCase):
    def test_retained_renamed_and_deleted_before_build(self):
        root = Path(tempfile.mkdtemp(prefix='oracle-', dir=os.environ['TMPDIR']))
        old = root / 'old-payload'
        payload = b'evicted-only1928' * 4096
        old.write_bytes(payload)
        def before_build():
            fixture.assert_payload_reclaimed(root, payload)
        with self.assertRaisesRegex(AssertionError, 'old payload retained'):
            before_build()
        quarantine = root / 'quarantine'
        quarantine.mkdir()
        old.rename(quarantine / 'renamed')
        self.assertFalse(old.exists())
        with self.assertRaisesRegex(AssertionError, 'old payload retained'):
            before_build()
        (quarantine / 'renamed').unlink()
        before_build()
        # Arbitrary new bytes are allowed even if the OS reuses an old inode.
        (root / 'new-metadata').write_bytes(b'new metadata')
        before_build()
        print('PASS retained rejected; quarantine rename rejected; real unlink accepted; new metadata accepted')


if __name__ == '__main__':
    unittest.main(verbosity=2)
