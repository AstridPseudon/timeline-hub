from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest

from astrid.core.execution.generic_host import GenericPackHost
from astrid.core.pack.discovery import discover_canonical_pack_metadata, discover_pack_metadata
from astrid.core.pack.source_setup import (
    DEFAULT_HIVEMIND_REPOSITORY,
    DEFAULT_HIVEMIND_REVISION,
    HIVEMIND_REPOSITORY_ENV,
    HIVEMIND_REVISION_ENV,
    SourceDeclaration,
    SourceSetupError,
    active_source_inventory,
    declarations_from_json,
    default_source_declarations,
    hivemind_pin_report,
    provision,
)
from astrid.sdk.discovery import _discover_pack_inventory
from astrid.sdk.discovery import _pack_record


def _git(root: Path, *args: str) -> str:
    return subprocess.check_output(["git", "-C", str(root), *args], text=True).strip()


def _fixture_repo(root: Path, *, schema_version: int = 2) -> str:
    root.mkdir()
    _git(root, "init", "-q", "-b", "main")
    _git(root, "config", "user.email", "fixture@example.test")
    _git(root, "config", "user.name", "Astrid fixture")
    pack = root
    executor = pack / "executors" / "echo"
    executor.mkdir(parents=True)
    (pack / "pack.yaml").write_text(
        f"schema_version: {schema_version}\nid: demo\nname: Demo Pack\nversion: 1.0.0\n"
        "capabilities: [testing]\n",
        encoding="utf-8",
    )
    (executor / "executor.yaml").write_text(
        json.dumps(
            {
                "id": "demo.echo",
                "name": "Demo Echo",
                "kind": "external",
                "version": "1.0",
                "command": {"argv": ["echo", "ok"]},
                "cache": {"mode": "none"},
            }
        ),
        encoding="utf-8",
    )
    _git(root, "add", ".")
    _git(root, "commit", "-q", "-m", "fixture")
    return _git(root, "rev-parse", "HEAD")


def test_default_source_policy_uses_full_delivery_hivemind_pin(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("ASTRID_SOURCE_DECLARATIONS", raising=False)
    monkeypatch.delenv(HIVEMIND_REVISION_ENV, raising=False)
    monkeypatch.delenv(HIVEMIND_REPOSITORY_ENV, raising=False)
    declarations = default_source_declarations()
    assert declarations[0].revision == DEFAULT_HIVEMIND_REVISION
    assert declarations[0].repository == DEFAULT_HIVEMIND_REPOSITORY
    assert hivemind_pin_report(declarations)["status"] == "configured"


def test_default_source_policy_accepts_only_a_configured_full_immutable_pin(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    revision = "a" * 40
    monkeypatch.setenv(HIVEMIND_REVISION_ENV, revision)
    declarations = default_source_declarations()
    assert declarations == (
        SourceDeclaration(
            pack_id="hivemind",
            repository=DEFAULT_HIVEMIND_REPOSITORY,
            revision=revision,
        ),
    )
    assert hivemind_pin_report(declarations)["status"] == "configured"

    monkeypatch.setenv(HIVEMIND_REVISION_ENV, "deadbeef")
    with pytest.raises(SourceSetupError, match="full immutable Hivemind Git object id"):
        default_source_declarations()


def test_local_git_v2_source_is_staged_once_and_shared(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    repository = tmp_path / "repository"
    revision = _fixture_repo(repository)
    state_path = tmp_path / "state" / "pack-sources.json"
    data_root = tmp_path / "data"
    declaration = SourceDeclaration.from_mapping(
        {"pack_id": "demo", "repository": str(repository), "revision": revision}
    )
    monkeypatch.setenv("ASTRID_SOURCE_STATE", str(state_path))

    result = provision((declaration,), state_path=state_path, data_root=data_root)
    assert result["ok"] is True
    inventory = active_source_inventory(state_path=state_path)
    assert inventory.sources[0].pack_root.is_dir()
    assert inventory.sources[0].revision == revision

    discovered = discover_pack_metadata(discover_packs_fn=lambda *args: ())
    managed = next(item for item in discovered if item.id == "demo")
    assert managed.source_kind == "managed"
    assert managed.source_inventory_identity == inventory.identity
    assert managed.source_revision == revision
    canonical = next(item for item in discover_canonical_pack_metadata() if item.id == "demo")
    assert canonical.source_kind == "managed"
    assert canonical.source_inventory_identity == inventory.identity
    sdk_record = _pack_record(next(item for item in _discover_pack_inventory() if item.id == "demo"))
    assert sdk_record["source_kind"] == "managed"
    assert sdk_record["source_inventory_identity"] == inventory.identity

    host = GenericPackHost(
        pack_roots=[*map(str, inventory.roots)],
        source_inventory_identity=inventory.identity,
    )
    record = next(item for item in host.discover() if item.id == "demo.echo")
    assert Path(record.definition.metadata["pack_root"]) == inventory.sources[0].pack_root
    assert host.source_inventory_identity == inventory.identity
    assert host.source_epoch != "uninitialized"

    before = state_path.read_bytes()
    checked = provision((declaration,), check=True, state_path=state_path, data_root=data_root)
    assert checked["changed"] is False
    assert state_path.read_bytes() == before

    offline = provision((declaration,), offline=True, state_path=state_path, data_root=data_root)
    assert offline["ok"] is True
    disabled = provision((), disable_pack="demo", state_path=state_path, data_root=data_root)
    assert disabled["active"] == []
    assert active_source_inventory(state_path=state_path).sources == ()
    restored = provision(
        (declaration,), offline=True, restore_pack="demo", state_path=state_path, data_root=data_root
    )
    assert restored["ok"] is True
    assert active_source_inventory(state_path=state_path).sources[0].revision == revision


def test_managed_source_requires_strict_v2_manifest(tmp_path: Path) -> None:
    repository = tmp_path / "repository"
    revision = _fixture_repo(repository, schema_version=1)
    state_path = tmp_path / "state" / "pack-sources.json"
    data_root = tmp_path / "data"
    declaration = SourceDeclaration.from_mapping(
        {"pack_id": "demo", "repository": str(repository), "revision": revision}
    )

    with pytest.raises(SourceSetupError, match="canonical v2/v3 admission.*schema_version must be integer 2 or 3"):
        provision((declaration,), state_path=state_path, data_root=data_root)
    assert not state_path.exists()


def test_invalid_update_keeps_prior_active_state(tmp_path: Path) -> None:
    repository = tmp_path / "repository"
    revision = _fixture_repo(repository)
    state_path = tmp_path / "state" / "pack-sources.json"
    data_root = tmp_path / "data"
    first = SourceDeclaration.from_mapping(
        {"pack_id": "demo", "repository": str(repository), "revision": revision}
    )
    provision((first,), state_path=state_path, data_root=data_root)
    prior_state = state_path.read_bytes()

    (repository / "pack.yaml").write_text(
        "schema_version: 1\nid: demo\nname: Broken\nversion: 1.0.0\n", encoding="utf-8"
    )
    _git(repository, "add", "pack.yaml")
    _git(repository, "commit", "-q", "-m", "invalid-update")
    bad_revision = _git(repository, "rev-parse", "HEAD")
    bad = SourceDeclaration.from_mapping(
        {"pack_id": "demo", "repository": str(repository), "revision": bad_revision}
    )

    with pytest.raises(SourceSetupError, match="canonical v2/v3 admission.*schema_version must be integer 2 or 3"):
        provision((bad,), state_path=state_path, data_root=data_root)
    assert state_path.read_bytes() == prior_state
    assert active_source_inventory(state_path=state_path).sources[0].revision == revision


def test_active_checkout_tamper_fails_closed(tmp_path: Path) -> None:
    repository = tmp_path / "repository"
    revision = _fixture_repo(repository)
    state_path = tmp_path / "state" / "pack-sources.json"
    data_root = tmp_path / "data"
    declaration = SourceDeclaration.from_mapping(
        {"pack_id": "demo", "repository": str(repository), "revision": revision}
    )
    provision((declaration,), state_path=state_path, data_root=data_root)
    active_root = active_source_inventory(state_path=state_path).sources[0].pack_root
    # Interpreter caches are ignored generated files and must not invalidate
    # the immutable tracked-tree digest of an installed source.
    (active_root / ".git" / "info" / "exclude").write_text("__pycache__/\n*.pyc\n", encoding="utf-8")
    cache = active_root / "__pycache__" / "generated.pyc"
    cache.parent.mkdir()
    cache.write_bytes(b"generated bytecode")
    assert active_source_inventory(state_path=state_path).sources[0].revision == revision
    (active_root / "pack.yaml").write_text(
        (active_root / "pack.yaml").read_text(encoding="utf-8") + "\n# tampered\n",
        encoding="utf-8",
    )
    with pytest.raises(SourceSetupError, match="dirty|digest mismatch"):
        active_source_inventory(state_path=state_path)


def test_failed_stage_removes_temporary_checkout_and_keeps_state_absent(tmp_path: Path) -> None:
    repository = tmp_path / "repository"
    _fixture_repo(repository)
    state_path = tmp_path / "state" / "pack-sources.json"
    data_root = tmp_path / "data"
    declaration = SourceDeclaration.from_mapping(
        {
            "pack_id": "demo",
            "repository": str(repository),
            "revision": "0" * 40,
        }
    )
    with pytest.raises(SourceSetupError):
        provision((declaration,), state_path=state_path, data_root=data_root)
    if (data_root / "demo").exists():
        assert not list((data_root / "demo").glob("stage-*"))
    assert not state_path.exists()


def test_offline_missing_cache_and_tamper_fail_closed(tmp_path: Path) -> None:
    repository = tmp_path / "repository"
    revision = _fixture_repo(repository)
    state_path = tmp_path / "state" / "pack-sources.json"
    data_root = tmp_path / "data"
    declaration = SourceDeclaration.from_mapping(
        {"pack_id": "demo", "repository": str(repository), "revision": revision}
    )

    missing = provision(
        (declaration,), offline=True, check=True, state_path=state_path, data_root=data_root
    )
    assert missing["ok"] is False
    assert "cached revision is missing" in missing["errors"][0]

    provision((declaration,), state_path=state_path, data_root=data_root)
    active = active_source_inventory(state_path=state_path)
    (active.sources[0].pack_root / "pack.yaml").write_text(
        (active.sources[0].pack_root / "pack.yaml").read_text(encoding="utf-8")
        + "\n# tampered\n",
        encoding="utf-8",
    )
    with pytest.raises(SourceSetupError, match="dirty"):
        active_source_inventory(state_path=state_path)


@pytest.mark.parametrize("failure", ["auth", "generation", "disconnect", "overflow", "cleanup"])
def test_inventory_custody_failure_cannot_enter_tree_digest_fallback(tmp_path, monkeypatch, failure):
    from astrid.core.execution import custody_broker as cb
    from astrid.core.pack import source_setup as sources
    root=tmp_path / "checkout";root.mkdir();(root / "tracked").write_text("file")
    def rejected(*args,**kwargs):raise cb.CustodyError("controlled " + failure)
    monkeypatch.setattr(cb,"command_inventory_git",rejected)
    with pytest.raises(cb.CustodyError):sources._tree_digest(root)


def test_real_outer_command_inventory_route_retains_sibling_creator_waits_and_graph(tmp_path, monkeypatch):
    import os,sys
    from astrid.core.execution import process_group as pg
    from astrid.core.pack import source_setup as sources
    repository=tmp_path / "repository";revision=_fixture_repo(repository)
    state=tmp_path / "sources.json";data=tmp_path / "sources"
    declaration=SourceDeclaration("demo",str(repository),revision)
    assert provision((declaration,),state_path=state,data_root=data)["ok"]
    before=state.read_bytes();environment=dict(os.environ,ASTRID_SOURCE_STATE=str(state),PYTHONDONTWRITEBYTECODE="1")
    script=tmp_path / "public_inventory.py"
    source_root=Path(sources.__file__).resolve().parents[3]
    script.write_text("import sys,json\nsys.path.insert(0,"+repr(str(source_root))+ ")\nfrom astrid.core.pack.source_setup import active_source_inventory\nresult=active_source_inventory()\nassert len(result.sources)==1\nprint(json.dumps({'identity':result.identity}))\n")
    process=pg.popen_owned_process([sys.executable,"-I",str(script)],cwd=str(tmp_path),env=environment,
                                  stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    try:
        stdout,stderr=process.communicate(timeout=30)
        assert process.wait(timeout=0)==0,stderr.decode()
        pg.verify_tree_absent(process)
        owner=process._astrid_custody._inventory_owner
        if sys.platform=="darwin":
            assert owner is not None and len(owner.helpers)==4
            assert owner.pending is None and owner.error is None and not owner.accepting
            assert all(helper.wait(timeout=0)==0 for helper in owner.helpers.values())
            assert all(helper.pid != process.pid for helper in owner.helpers.values())
            journal=[json.loads(line) for line in (process._astrid_custody.root / "custody.journal.jsonl").read_text().splitlines()]
            pending=[r for r in journal if r.get("event")=="command_inventory_pending"]
            completed=[r for r in journal if r.get("event")=="command_inventory_completed"]
            assert [r["operation_id"] for r in pending]==[1,2,3,4]
            assert [r["operation_id"] for r in completed]==[1,2,3,4]
            assert all(r["helper_graph"]=="VERIFIED" and r["original_wait"]==0 for r in completed)
            assert all("environment" not in r for r in pending+completed)
        else:assert owner is None
        assert state.read_bytes()==before and "identity" in json.loads(stdout)
    finally:
        if process.poll() is None:pg.terminate_tree(process)
        process.wait(timeout=5)


def test_darwin_cf_projection_preserves_only_exact_owner_pin_and_other_keys(monkeypatch):
    from astrid.core import subprocess_env as policy
    monkeypatch.setattr(policy.sys, 'platform', 'darwin')
    pin = '0x1F5:0:0'
    parent = {'HOME': '/owner', 'PATH': '/bin', 'LANG': 'C.UTF-8', '__CF_USER_TEXT_ENCODING': pin}
    before = policy.build_child_subprocess_env(base={k: v for k, v in parent.items() if k != '__CF_USER_TEXT_ENCODING'}, parent={k: v for k, v in parent.items() if k != '__CF_USER_TEXT_ENCODING'})
    result = policy.build_child_subprocess_env(base={'HOME': '/owner', 'PATH': '/bin', 'LANG': 'C.UTF-8'}, parent=parent)
    assert result == {**before, '__CF_USER_TEXT_ENCODING': pin}
    assert policy.build_child_subprocess_env(base=parent, parent=parent,
        explicit_env={'__CF_USER_TEXT_ENCODING': pin}) == result


@pytest.mark.parametrize('source', ['base', 'explicit'])
@pytest.mark.parametrize('owner_present', [False, True])
def test_darwin_cf_projection_rejects_unpinned_or_conflicting_inputs(monkeypatch, source, owner_present):
    from astrid.core import subprocess_env as policy
    monkeypatch.setattr(policy.sys, 'platform', 'darwin')
    parent = {'__CF_USER_TEXT_ENCODING': '0x1F5:0:0'} if owner_present else {}
    base = {'HOME': '/owner'}
    explicit = {}
    (base if source == 'base' else explicit)['__CF_USER_TEXT_ENCODING'] = 'different-caller-value'
    with pytest.raises(policy.SubprocessEnvPolicyError, match='inherited owner pin'):
        policy.build_child_subprocess_env(base=base, parent=parent, explicit_env=explicit)


@pytest.mark.parametrize('value', ['', None, 501, 'bad\0value'])
def test_darwin_cf_projection_refuses_malformed_owner_pin(monkeypatch, value):
    from astrid.core import subprocess_env as policy
    monkeypatch.setattr(policy.sys, 'platform', 'darwin')
    with pytest.raises(policy.SubprocessEnvPolicyError):
        policy.build_child_subprocess_env(base={'__CF_USER_TEXT_ENCODING': value},
            parent={'__CF_USER_TEXT_ENCODING': value})


def test_darwin_cf_projection_never_manufactures_absent_owner_pin(monkeypatch):
    from astrid.core import subprocess_env as policy
    monkeypatch.setattr(policy.sys, 'platform', 'darwin')
    assert '__CF_USER_TEXT_ENCODING' not in policy.build_child_subprocess_env(base={'HOME': '/owner'}, parent={})


def test_non_darwin_cf_projection_retains_prior_filter_and_explicit_behavior(monkeypatch):
    from astrid.core import subprocess_env as policy
    monkeypatch.setattr(policy.sys, 'platform', 'linux')
    assert '__CF_USER_TEXT_ENCODING' not in policy.build_child_subprocess_env(
        base={'__CF_USER_TEXT_ENCODING': 'base'}, parent={'__CF_USER_TEXT_ENCODING': 'parent'})
    assert policy.build_child_subprocess_env(base={}, parent={},
        explicit_env={'__CF_USER_TEXT_ENCODING': 'explicit'})['__CF_USER_TEXT_ENCODING'] == 'explicit'


def test_real_filtered_command_root_cf_pin_preserves_all_four_inventory_operations(tmp_path):
    import os, sys, hashlib
    from astrid.core.execution import process_group as pg
    from astrid.core.pack import source_setup as sources
    from astrid.core.subprocess_env import build_child_subprocess_env
    repository = tmp_path / 'repository'
    revision = _fixture_repo(repository)
    state = tmp_path / 'sources.json'
    assert provision((SourceDeclaration('demo', str(repository), revision),),
        state_path=state, data_root=tmp_path / 'sources')['ok']
    before = state.read_bytes()
    parent = dict(os.environ, ASTRID_SOURCE_STATE=str(state), PYTHONDONTWRITEBYTECODE='1')
    environment = build_child_subprocess_env(parent=parent, passthrough=('ASTRID_SOURCE_STATE',),
        declared_passthrough=('ASTRID_SOURCE_STATE',))
    key = '__CF_USER_TEXT_ENCODING'
    if sys.platform == 'darwin':
        assert key in parent and environment[key] == parent[key]
    script = tmp_path / 'public_inventory.py'
    source_root = Path(sources.__file__).resolve().parents[3]
    script.write_text("import sys,os,json,hashlib\nsys.path.insert(0," + repr(str(source_root)) + ")\n"
        "from astrid.core.pack.source_setup import active_source_inventory\n"
        "result=active_source_inventory()\nassert len(result.sources)==1\n"
        "value=os.environ.get('__CF_USER_TEXT_ENCODING')\n"
        "print(json.dumps({'identity':result.identity,'cf_present':value is not None,"
        "'cf_sha256':None if value is None else hashlib.sha256(value.encode()).hexdigest()}))\n")
    process = pg.popen_owned_process([sys.executable, '-I', str(script)], cwd=str(tmp_path), env=environment,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        stdout, stderr = process.communicate(timeout=30)
        assert process.wait(timeout=0) == 0, stderr.decode()
        pg.verify_tree_absent(process)
        result = json.loads(stdout)
        assert state.read_bytes() == before and result['identity']
        if sys.platform == 'darwin':
            assert result['cf_present'] and result['cf_sha256'] == hashlib.sha256(parent[key].encode()).hexdigest()
            owner = process._astrid_custody._inventory_owner
            assert owner is not None and owner.error is None and owner.pending is None and len(owner.helpers) == 4
            assert all(helper.wait(timeout=0) == 0 for helper in owner.helpers.values())
            journal = [json.loads(line) for line in (process._astrid_custody.root / 'custody.journal.jsonl').read_text().splitlines()]
            pending = [r for r in journal if r.get('event') == 'command_inventory_pending']
            completed = [r for r in journal if r.get('event') == 'command_inventory_completed']
            assert [r['operation'] for r in pending] == ['revision', 'clean_status', 'repository_root', 'tracked_files']
            assert [r['operation_id'] for r in completed] == [1, 2, 3, 4]
            assert all(r['helper_graph'] == 'VERIFIED' and r['original_wait'] == 0 for r in completed)
            assert not any(r.get('event') == 'command_inventory_first_failure' for r in journal)
    finally:
        if process.poll() is None:
            pg.terminate_tree(process)
        process.wait(timeout=5)


@pytest.mark.parametrize('where', ['base', 'explicit_env'])
@pytest.mark.parametrize('value', ['/foreign/state.json', ''])
def test_source_selector_rejects_command_conflict(where, value, tmp_path):
    from astrid.core.subprocess_env import SubprocessEnvPolicyError, build_child_subprocess_env
    parent = {'ASTRID_SOURCE_STATE': str(tmp_path / 'state.json')}
    with pytest.raises(SubprocessEnvPolicyError, match='parent-owned'):
        build_child_subprocess_env(parent=parent, **{'base': {}, where: {'ASTRID_SOURCE_STATE': value}})


@pytest.mark.parametrize('value', ['', 'relative.json', ' /absolute.json', '/bad\0state'])
def test_source_selector_rejects_invalid_parent(value):
    from astrid.core.subprocess_env import SubprocessEnvPolicyError, build_child_subprocess_env
    with pytest.raises(SubprocessEnvPolicyError, match='parent-owned'):
        build_child_subprocess_env(base={}, parent={'ASTRID_SOURCE_STATE': value})


def test_source_selector_absent_and_unowned_selection():
    from astrid.core.subprocess_env import SubprocessEnvPolicyError, build_child_subprocess_env
    assert build_child_subprocess_env(base={'HOME': '/owner', 'XDG_STATE_HOME': '/foreign',
        'UNRELATED': 'value', 'API_TOKEN': 'secret', 'PYTHONSTARTUP': '/startup'}, parent={}) == {'HOME': '/owner'}
    for channel in ('base', 'explicit_env'):
        with pytest.raises(SubprocessEnvPolicyError, match='parent-owned'):
            build_child_subprocess_env(parent={}, **{'base': {}, channel: {'ASTRID_SOURCE_STATE': '/task/state.json'}})


def test_selected_source_real_registry_projections_and_fresh_refusals(tmp_path):
    """Real verified fixture inventory and registry discovery; no native issuer."""
    import hashlib
    import os
    import sys
    import time

    import banodoco_timeline_schema

    from astrid.core.rendering import remotion_runtime as runtime
    from astrid.core.subprocess_env import build_child_subprocess_env

    repository = tmp_path / 'repository'
    revision = _fixture_repo(repository)
    state = tmp_path / 'selected.json'
    assert provision((SourceDeclaration('demo', str(repository), revision),),
        state_path=state, data_root=tmp_path / 'data')['ok']
    original = state.read_bytes()
    (tmp_path / 'qualified-state.json').write_bytes(original)
    inventory = active_source_inventory(state_path=state)
    root = Path(__file__).resolve().parents[3]
    packs = root / 'tests/fixtures/renderer_packs/discovery/source'
    parent = {'HOME': str(tmp_path), 'PATH': os.environ['PATH'], 'TMPDIR': str(tmp_path),
              'ASTRID_SOURCE_STATE': str(state), 'ASTRID_PACKS_PATH': str(packs),
              'ASTRID_TIMELINE_SCHEMA_PYTHONPATH': str(Path(banodoco_timeline_schema.__file__).resolve().parent.parent),
              'XDG_STATE_HOME': str(tmp_path / 'foreign'), 'API_TOKEN': 'secret',
              'PYTHONSTARTUP': '/unqualified', 'UNRELATED': 'value'}
    child = build_child_subprocess_env(base=parent, parent=parent)
    repeated = build_child_subprocess_env(base=child, parent=child,
        explicit_env={'ASTRID_SOURCE_STATE': str(state)})
    assert child == repeated
    assert not {'XDG_STATE_HOME', 'API_TOKEN', 'PYTHONSTARTUP', 'UNRELATED'} & child.keys()
    script = ('import sys,json; sys.path[0]=sys.argv[2]; sys.path.insert(0,sys.argv[1]); '
              'sys.path.insert(0,sys.argv[3]); '
              'from astrid.core.rendering.remotion_runtime import _registry_observation; '
              'print(json.dumps(_registry_observation(),sort_keys=True))')

    commands = []

    def observe(environment, generator):
        directory = root / ('scripts' if generator else 'astrid/packs/rendering/rendering')
        argv = [sys.executable, '-B', '-I', '-c', script, str(root),
                str(directory), parent['ASTRID_TIMELINE_SCHEMA_PYTHONPATH']]
        started = time.monotonic()
        with subprocess.Popen(argv, env=environment, cwd=directory,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) as process:
            stdout, stderr = process.communicate()
        result = subprocess.CompletedProcess(argv, process.returncode, stdout, stderr)
        prefix = f'probe-{len(commands):02d}'
        (tmp_path / (prefix + '.stdout')).write_text(stdout)
        (tmp_path / (prefix + '.stderr')).write_text(stderr)
        commands.append({'argv': argv, 'cwd': str(directory), 'environment': environment,
            'generator': generator, 'pid': process.pid, 'exit_code': result.returncode,
            'seconds': time.monotonic() - started,
            'state_sha256': hashlib.sha256(state.read_bytes()).hexdigest(),
            'stdout_sha256': hashlib.sha256(stdout.encode()).hexdigest(),
            'stderr_sha256': hashlib.sha256(stderr.encode()).hexdigest()})
        (tmp_path / 'probe-commands.json').write_text(json.dumps(commands, indent=2))
        return result

    observations = []
    for label, environment in [('parent', {k: v for k, v in parent.items()
            if k not in {'PYTHONSTARTUP', 'XDG_STATE_HOME'}}), ('child', child), ('repeated', repeated)]:
        for generator in (False, True):
            context = runtime._registry_context(environment, generator=generator)
            assert context['ASTRID_SOURCE_STATE'] == str(state)
            assert context['ASTRID_PACKS_PATH'] == str(packs)
            result = observe(context, generator)
            assert result.returncode == 0, result.stderr
            observation = json.loads(result.stdout)
            assert observation['managed_inventory_identity'] == inventory.identity
            assert observation['selected_source_state']['path'] == str(state)
            assert observation['selected_source_state']['sha256'] == hashlib.sha256(original).hexdigest()
            assert str(inventory.roots[0]) in observation['roots']
            assert str(packs) in observation['roots']
            assert observation['runtime_origin'] == str(Path(runtime.__file__).resolve())
            runtime._registry_inputs(observation)
            (tmp_path / f'{label}-{generator}.json').write_text(json.dumps(observation, indent=2))
            observations.append(observation)
    assert all(item['state'] == observations[0]['state'] for item in observations)
    assert state.read_bytes() == original
    print('SOURCE_PROJECTION=' + json.dumps({'state_path': str(state),
        'state_sha256': hashlib.sha256(original).hexdigest(), 'revision': revision,
        'inventory': [item.to_dict() for item in inventory.sources],
        'identity': inventory.identity, 'registry': observations[0]['state'],
        'origins': {key: observations[0][key] for key in ('astrid_origin', 'runtime_origin', 'generator_origin')}}))

    # Actual verifier failures under both retained contexts, with a valid
    # default inventory present to detect accidental selected-state fallback.
    default = tmp_path / '.local/state/astrid/default/pack-sources.json'
    default.parent.mkdir(parents=True)
    default.write_bytes(original)
    negatives = {}
    for defect in ('version', 'key', 'revision', 'digest', 'foreign_root', 'pack_changed'):
        changed = json.loads(original)
        record = changed['active']['demo']
        if defect == 'version':
            changed['version'] = 999
        elif defect == 'key':
            changed['active']['foreign'] = changed['active'].pop('demo')
        elif defect == 'revision':
            record['revision'] = 'f' * 40
        elif defect == 'digest':
            record['tree_sha256'] = 'f' * 64
        elif defect == 'foreign_root':
            record['pack_root'] = str(tmp_path / 'foreign-root')
        else:
            (inventory.roots[0] / 'pack.yaml').write_text('changed pack')
        state.write_text(json.dumps(changed))
        for generator in (False, True):
            # Use the already-qualified projections; observe must freshly
            # validate actual state and source rather than reuse discovery.
            result = observe(runtime._registry_context(repeated, generator=generator), generator) if defect not in {'version'} else observe(repeated, generator)
            assert result.returncode != 0, (defect, result.stdout)
            negatives[f'{defect}-{generator}'] = {'exit': result.returncode,
                'stderr_sha256': hashlib.sha256(result.stderr.encode()).hexdigest()}
        state.write_bytes(original)
    (tmp_path / 'negative-results.json').write_text(json.dumps(negatives, indent=2))
    assert runtime._selected_source_state_binding(repeated) == observations[0]['selected_source_state']
    state.write_bytes(original + b'\n')
    with pytest.raises(runtime.RemotionValidationError, match='changed after'):
        runtime._registry_inputs(observations[0])
