"""Registry context keys collapse restatements of the default corpus, nothing else."""
import hashlib
import json
import os
from types import SimpleNamespace

import pytest

from astrid.core.foundation.paths import REPO_ROOT
from astrid.core.rendering import remotion_runtime as runtime


def _env(tmp_path, **extra):
    return {'HOME': str(tmp_path), 'PATH': '/usr/bin:/bin', **extra}


def _key(env):
    return runtime._registry_context(env, generator=False)


def test_pythonpath_naming_the_checkout_collapses_with_its_absence(tmp_path):
    base = _env(tmp_path)
    assert _key(_env(tmp_path, PYTHONPATH=str(REPO_ROOT))) == _key(base)
    assert 'PYTHONPATH' not in _key(_env(tmp_path, PYTHONPATH=str(REPO_ROOT)))


def test_a_different_pythonpath_entry_keeps_its_own_context(tmp_path):
    extra = tmp_path / 'deps'
    extra.mkdir()
    key = _key(_env(tmp_path, PYTHONPATH=os.pathsep.join((str(REPO_ROOT), str(extra)))))
    assert key['PYTHONPATH'] == str(extra)
    assert key != _key(_env(tmp_path))


def test_builtin_and_managed_pack_roots_collapse_but_an_external_root_does_not(tmp_path, monkeypatch):
    managed = tmp_path / 'managed-pack'
    managed.mkdir()
    external = tmp_path / 'external-pack'
    external.mkdir()
    from astrid.core.pack import source_setup

    class _Inventory:
        sources = [type('Source', (), {'pack_root': managed})()]
    monkeypatch.setattr(source_setup, 'active_source_inventory', lambda **_: _Inventory())
    builtin = str(REPO_ROOT / 'astrid' / 'packs')
    base = _key(_env(tmp_path))
    assert _key(_env(tmp_path, ASTRID_PACKS_PATH=builtin)) == base
    assert _key(_env(tmp_path, ASTRID_PACKS_PATH=os.pathsep.join((builtin, str(managed))))) == base
    different = _key(_env(tmp_path, ASTRID_PACKS_PATH=os.pathsep.join((builtin, str(external)))))
    assert different != base and different['ASTRID_PACKS_PATH'] == str(external)


def test_render_in_an_unvalidated_context_is_still_refused(tmp_path, monkeypatch):
    project = tmp_path / 'project'
    project.mkdir()
    external = tmp_path / 'external-pack'
    external.mkdir()
    reference = tmp_path / 'validation.json'
    raw = json.dumps({'schema': runtime._VALIDATION_SCHEMA, 'launch_id': 'l',
                      'probe_source_sha256': hashlib.sha256(runtime._schema_probe_source().encode()).hexdigest(),
                      'contexts': {'host': {'variants': []}}}).encode()
    reference.write_bytes(raw)
    reference.chmod(0o600)
    env = _env(tmp_path, ASTRID_PACKS_PATH=str(external))
    env.update(dict(zip(runtime._REF_ENV_KEYS, (str(reference), hashlib.sha256(raw).hexdigest(), 'l', 'host'))))
    with pytest.raises(runtime.RemotionValidationError, match='consumer context differs'):
        runtime._validated_runtime(project, environment=env, python_executable='/usr/bin/python3')
    env.pop(runtime._REF_ENV_KEYS[0])
    with pytest.raises(runtime.RemotionValidationError, match='missing or invalid launch validation'):
        runtime._validated_runtime(project, environment=env, python_executable='/usr/bin/python3')


def test_repeated_path_entries_do_not_make_a_different_context():
    # A shell that sourced its env twice (e.g. inside an otto-heavy job) repeats PATH
    # entries; lookup is unchanged, so the validated context must match.
    import os
    from astrid.core.rendering import remotion_runtime as rr
    base = {"HOME": "/h", "PATH": os.pathsep.join(["/v/bin", "/n/bin", "/usr/bin"]), "TMPDIR": "/t"}
    doubled = {**base, "PATH": os.pathsep.join(["/v/bin", "/n/bin", "/v/bin", "/n/bin", "/usr/bin"])}
    assert rr._dedupe_path(doubled["PATH"]) == base["PATH"]
    assert rr._registry_context(doubled, generator=False) == rr._registry_context(base, generator=False)
    import sys
    a = rr.probe_context(environment=doubled, python_executable=sys.executable)
    b = rr.probe_context(environment=base, python_executable=sys.executable)
    assert a["node_env"] == b["node_env"]
    # A genuinely different PATH order still differs.
    swapped = {**base, "PATH": os.pathsep.join(["/n/bin", "/v/bin", "/usr/bin"])}
    assert rr._registry_context(swapped, generator=False) != rr._registry_context(base, generator=False)


def test_windows_registry_context_keeps_windows_child_environment_only_on_windows(monkeypatch):
    windows = {name: f"value-{name}" for name in (
        "USERPROFILE", "HOMEDRIVE", "HOMEPATH", "APPDATA", "LOCALAPPDATA",
        "SYSTEMROOT", "TEMP", "TMP", "PATHEXT", "COMSPEC",
    )}
    monkeypatch.setattr(runtime, "probe_context", lambda **_: {})
    monkeypatch.setattr(runtime, "sys", SimpleNamespace(platform="win32", executable="python"))

    assert runtime._registry_context(windows, generator=True) == windows

    monkeypatch.setattr(runtime, "sys", SimpleNamespace(platform="linux", executable="python"))
    assert runtime._registry_context(windows, generator=True) == {}
