"""Public command recovery after a partial program removal."""

from unittest.mock import Mock

from astrid.installer import cli
from astrid.installer.core import write_json
from astrid.installer.service import LABEL


def test_partial_uninstall_can_finish_after_version_metadata_was_removed(tmp_path, monkeypatch):
    from runtime_protocol import platform

    monkeypatch.setenv('HOME', str(tmp_path / 'home'))
    monkeypatch.setenv('XDG_DATA_HOME', str(tmp_path / 'xdg-data'))
    monkeypatch.setattr(platform, 'log_dir', lambda: tmp_path / 'logs')
    root, data = tmp_path / 'program', tmp_path / 'workspace'
    write_json(root / 'install.json', {'owner': LABEL, 'data_root': str(data)})
    (root / 'current').write_text('removed-version\n')
    backend = Mock()
    backend.service.recorded.return_value = {'owner': LABEL, 'program_root': str(root),
                                             'data_root': str(data), 'uninstalled': True}
    backend.existing.return_value = None
    backend.remove.return_value = []
    monkeypatch.setattr(cli, 'Backend', Mock(return_value=backend))

    assert cli.main(['--root', str(root), '--uninstall']) == 0
    backend.stop.assert_called_once_with(None, data)
    backend.unregister.assert_called_once_with()
    backend.remove.assert_called_once_with(root, data, delete_data=False)
