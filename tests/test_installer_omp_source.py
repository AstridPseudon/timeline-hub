"""The bundled fork recipe is the only OMP staging route and fails closed."""

import hashlib
import io
import json
import subprocess
import zipfile
from pathlib import Path

import pytest

from astrid.installer import tools


def digest(value):
    return hashlib.sha256(value).hexdigest()


def tree_digest(files):
    output = hashlib.sha256(b"astrid-omp-source-tree-v1\0")
    for name, data in sorted(files.items()):
        name = name.encode("utf-8")
        output.update(len(name).to_bytes(8, "big"))
        output.update(name)
        output.update(hashlib.sha256(data).digest())
    return output.hexdigest()


def zipped(files):
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, "w") as archive:
        for path, value in files.items():
            archive.writestr(path, value)
    return stream.getvalue()


def fixture(tmp_path, monkeypatch):
    before, after, lock = b"first\nold\nlast\n", b"first\nnew\nlast\n", b"frozen lock\n"
    source = zipped({"source/bun.lock": lock, "source/main.ts": before})
    native = zipped({"package/native.node": b"native"})
    recipe = {"version": "17.4.0", "base_commit": "a" * 40,
              "source": {"url": "https://example.invalid/source.zip", "tree_sha256": tree_digest({"bun.lock": lock, "main.ts": before}),
                         "directory": "source"}, "bun_lock_sha256": digest(lock),
              "patch": {"sha256": "b" * 64, "files": [{"path": "main.ts",
                  "before_sha256": digest(before), "after_sha256": digest(after),
                  "edits": [{"start": 1, "old": ["old\n"], "new": ["new\n"]}]}]},
              "native": {"linux-x64": {"url": "https://example.invalid/native.zip",
                         "sha256": digest(native), "files": ["native.node"]}}}
    payloads = {recipe["source"]["url"]: source, recipe["native"]["linux-x64"]["url"]: native}
    requests, calls = [], []

    def response(url, timeout):
        requests.append(url)
        return io.BytesIO(payloads[url])

    def run(argv, *, extra_env=None, cwd=None, clean_bun_env=False):
        calls.append(([str(v) for v in argv], dict(extra_env or {}), cwd, clean_bun_env))
        if "link" in argv:
            folder = Path(extra_env["BUN_INSTALL_BIN"])
            folder.mkdir(parents=True, exist_ok=True)
            (folder / "omp").write_bytes(b"launcher")
        return ""

    env = {"ASTRID_BUN_EXECUTABLE": "/qualified/bun", "BUN_INSTALL": str(tmp_path / "omp"),
           "BUN_INSTALL_BIN": str(tmp_path / "omp/bin"), "PATH": "/qualified:/usr/bin:/bin"}
    monkeypatch.setattr(tools.urllib.request, "urlopen", response)
    return recipe, payloads, requests, calls, run, env


def test_source_recipe_freezes_graph_generates_only_views_and_links_real_cli(tmp_path, monkeypatch):
    recipe, _payloads, requests, calls, run, env = fixture(tmp_path, monkeypatch)
    build_env = {**env, "BUN_INSTALL_GLOBAL_DIR": str(tmp_path / "omp/install/global"),
                 "HOME": str(tmp_path / "omp/build-home"),
                 "USERPROFILE": str(tmp_path / "omp/build-home"),
                 "XDG_CONFIG_HOME": str(tmp_path / "omp/build-home/config")}
    if "BUN_INSTALL_CACHE_DIR" in tools.os.environ:
        build_env["BUN_INSTALL_CACHE_DIR"] = tools.os.environ["BUN_INSTALL_CACHE_DIR"]
    tools._install_omp_source(recipe, tmp_path / "omp", "linux-x64", run, env)
    source = tmp_path / "omp/source"
    assert requests == [recipe["source"]["url"], recipe["native"]["linux-x64"]["url"]]
    assert (source / "main.ts").read_bytes() == b"first\nnew\nlast\n"
    assert (source / "bun.lock").read_bytes() == b"frozen lock\n"
    assert (source / "packages/natives/native/native.node").read_bytes() == b"native"
    assert not (tmp_path / "omp/native-archive").exists()
    assert not (tmp_path / "omp/source-archive").exists()
    assert calls[0][0] == ["/qualified/bun", "install", "--frozen-lockfile", "--ignore-scripts", "--omit", "optional"]
    assert calls[0][2] == source
    assert calls[1][0] == ["/qualified/bun", "run", "gen:tool-views"]
    assert calls[1][2] == source
    assert calls[2][0][:2] == ["/qualified/bun", "-e"]
    assert "__piNativesV17_4_0" in calls[2][0][2]
    assert calls[3][0] == ["/qualified/bun", "link", "--frozen-lockfile", "--ignore-scripts", "--no-save"]
    assert calls[3][2] == source / "packages/coding-agent"
    assert all(row[1] == build_env for row in calls)
    assert all(row[3] is True for row in calls)
    assert env["ASTRID_INSTALL_OMP_SOURCE"] == "fork"
    assert env["ASTRID_INSTALL_OMP_VERSION"] == "17.4.0"
    assert env["ASTRID_INSTALL_OMP_BASE_COMMIT"] == recipe["base_commit"]
    assert env["ASTRID_INSTALL_OMP_PATCH_SHA256"] == recipe["patch"]["sha256"]
    provenance = json.loads((tmp_path / "omp/source-provenance.json").read_text())
    assert provenance["base_commit"] == recipe["base_commit"]
    assert provenance["patch_sha256"] == recipe["patch"]["sha256"]
    assert provenance["native_sha256"] == recipe["native"]["linux-x64"]["sha256"]
    assert provenance["version"] == "17.4.0"


@pytest.mark.parametrize("asset", ["source", "native"])
def test_archive_digest_failure_prevents_using_untrusted_bytes(tmp_path, monkeypatch, asset):
    recipe, payloads, _requests, calls, run, env = fixture(tmp_path, monkeypatch)
    selected = recipe["source"] if asset == "source" else recipe["native"]["linux-x64"]
    if asset == "source":
        payloads[selected["url"]] = zipped({"source/bun.lock": b"frozen lock\n", "source/main.ts": b"wrong source\n"})
    else:
        payloads[selected["url"]] += b"tampered"
    with pytest.raises(ValueError, match="checksum mismatch"):
        tools._install_omp_source(recipe, tmp_path / "omp", "linux-x64", run, env)
    assert not any("link" in argv for argv, *_ in calls)
    if asset == "source":
        assert not calls


@pytest.mark.parametrize("change,match", [
    ("directory", "source directory"), ("lock", "lock"),
    ("before", "preimage"), ("after", "postimage"), ("chunk", "chunk"),
    ("path", "Unsafe archive entry"), ("native", "native"),
])
def test_invalid_source_lock_patch_or_native_fails_before_link(tmp_path, monkeypatch, change, match):
    recipe, payloads, _requests, calls, run, env = fixture(tmp_path, monkeypatch)
    if change == "directory":
        recipe["source"]["directory"] = "absent"
    elif change == "lock":
        recipe["bun_lock_sha256"] = "0" * 64
    elif change in {"before", "after"}:
        recipe["patch"]["files"][0][change + "_sha256"] = "0" * 64
    elif change == "chunk":
        recipe["patch"]["files"][0]["edits"][0]["old"] = ["different\n"]
    elif change == "path":
        recipe["patch"]["files"][0]["path"] = "../outside"
    elif change == "native":
        recipe["native"]["linux-x64"]["files"] = ["missing.node"]
    with pytest.raises(ValueError, match=match):
        tools._install_omp_source(recipe, tmp_path / "omp", "linux-x64", run, env)
    assert not any("link" in argv for argv, *_ in calls)


@pytest.mark.parametrize("step", ["install", "generator", "link"])
def test_lock_changes_at_any_build_step_are_refused(tmp_path, monkeypatch, step):
    recipe, _payloads, _requests, _calls, run, env = fixture(tmp_path, monkeypatch)

    def mutate(argv, **kwargs):
        result = run(argv, **kwargs)
        selected = {"install": "install", "generator": "gen:tool-views", "link": "link"}[step]
        if selected in argv:
            (tmp_path / "omp/source/bun.lock").write_bytes(b"resolved again")
        return result

    with pytest.raises(ValueError, match="lock"):
        tools._install_omp_source(recipe, tmp_path / "omp", "linux-x64", mutate, env)
    assert not (tmp_path / "omp/source-provenance.json").exists()


def test_host_native_abi_failure_never_registers_the_launcher(tmp_path, monkeypatch):
    recipe, _payloads, _requests, calls, run, env = fixture(tmp_path, monkeypatch)

    def refuse(argv, **kwargs):
        if "-e" in argv:
            raise subprocess.CalledProcessError(1, argv, output="wrong native ABI")
        return run(argv, **kwargs)

    with pytest.raises(subprocess.CalledProcessError, match="non-zero"):
        tools._install_omp_source(recipe, tmp_path / "omp", "linux-x64", refuse, env)
    assert not any("link" in argv for argv, *_ in calls)


def test_unsupported_native_target_fails_before_source_download(tmp_path, monkeypatch):
    recipe, _payloads, requests, calls, run, env = fixture(tmp_path, monkeypatch)
    with pytest.raises(ValueError, match="native.*windows-arm64"):
        tools._install_omp_source(recipe, tmp_path / "omp", "windows-arm64", run, env)
    assert not requests and not calls


def test_staging_rejects_old_manifest_before_any_download(tmp_path, monkeypatch):
    requested = []
    monkeypatch.setattr(tools, "fetch_archive", lambda *a, **k: requested.append(a))
    with pytest.raises(ValueError, match="OMP.*17.4.0"):
        tools.install_tools({"tools": {"omp": {"version": "12.0.0"}}}, tmp_path, "linux-x64", lambda *_: None)
    assert not requested


def test_bundled_recipe_matches_reviewed_patch_and_immutable_native_assets():
    recipe = tools.load_omp_recipe()
    assert recipe["version"] == "17.4.0"
    assert recipe["base_commit"] == "9962a46db1e8340320a0f2fb276964f957985505"
    assert recipe["patch"]["sha256"] == "4f5524ea9c687cea741fbaee1069e0d6789b7c85ea68c6a25fc4cdb18b0dbb33"
    assert {row["path"] for row in recipe["patch"]["files"]} == {
        "packages/coding-agent/src/main.ts", "packages/coding-agent/src/modes/acp/acp-agent.ts",
        "packages/coding-agent/src/modes/acp/acp-mode.ts"}
    assert set(recipe["native"]) == {"linux-x64", "linux-arm64", "macos-x64", "macos-arm64", "windows-x64"}
    assert recipe["source"]["url"].startswith("https://codeload.github.com/peteromallet/oh-my-pi/")
    assert len(recipe["source"]["tree_sha256"]) == 64
    for asset in recipe["native"].values():
        assert tools.asset_downloads(asset) == [(asset["url"], asset["sha256"])]


def test_local_qualification_override_uses_only_recipe_commit_and_same_tree_pin(tmp_path, monkeypatch):
    recipe, _payloads, requests, calls, run, env = fixture(tmp_path, monkeypatch)
    archived = []

    def local(repo, commit, archive):
        archived.append((repo, commit))
        archive.write_bytes(zipped({"bun.lock": b"frozen lock\n", "main.ts": b"first\nold\nlast\n"}))

    monkeypatch.setattr(tools, "local_source", local)
    tools._install_omp_source(recipe, tmp_path / "omp", "linux-x64", run, env, repo="/own/producer")
    assert archived == [("/own/producer", recipe["base_commit"])]
    assert requests == [recipe["native"]["linux-x64"]["url"]]
    assert calls[0][2] == tmp_path / "omp/source"
    assert json.loads((tmp_path / "omp/source-provenance.json").read_text())["source_mode"] == "local-repo"
    assert not (tmp_path / "omp/source.download").exists()


def test_source_tree_pin_rejects_added_files_before_commands(tmp_path, monkeypatch):
    recipe, payloads, _requests, calls, run, env = fixture(tmp_path, monkeypatch)
    payloads[recipe["source"]["url"]] = zipped({"source/bun.lock": b"frozen lock\n",
        "source/main.ts": b"first\nold\nlast\n", "source/extra.ts": b"unapproved"})
    with pytest.raises(ValueError, match="source tree checksum"):
        tools._install_omp_source(recipe, tmp_path / "omp", "linux-x64", run, env)
    assert not calls


def test_patch_preflights_all_files_before_writing_any(tmp_path):
    first, last = tmp_path / "first.ts", tmp_path / "last.ts"
    first.write_bytes(b"old\n")
    last.write_bytes(b"wrong\n")
    patch = {"files": [{"path": name, "before_sha256": digest(b"old\n"),
        "after_sha256": digest(b"new\n"), "edits": [{"start": 0, "old": ["old\n"], "new": ["new\n"]}]}
        for name in ("first.ts", "last.ts")]}
    with pytest.raises(ValueError, match="preimage.*last.ts"):
        tools._apply_omp_patch(tmp_path, patch)
    assert first.read_bytes() == b"old\n"
    assert last.read_bytes() == b"wrong\n"


def test_bundled_patch_corruption_is_refused(tmp_path, monkeypatch):
    folder = tmp_path / "omp"
    folder.mkdir()
    recipe = tools.load_omp_recipe()
    (folder / "recipe.json").write_text(json.dumps(recipe))
    (folder / "source.patch").write_bytes(b"different correction")
    monkeypatch.setattr(tools, "__file__", str(tmp_path / "tools.py"))
    with pytest.raises(ValueError, match="patch checksum"):
        tools.load_omp_recipe()


def test_inherited_bun_registration_paths_are_overridden_only_during_build(tmp_path, monkeypatch):
    recipe, _payloads, _requests, calls, run, env = fixture(tmp_path, monkeypatch)
    outside = tmp_path / "unrelated-global"
    monkeypatch.setenv("BUN_INSTALL_GLOBAL_DIR", str(outside))
    user_home = tmp_path / "user-home"
    user_home.mkdir()
    monkeypatch.setenv("HOME", str(user_home))
    user_config = user_home / ".bunfig.toml"
    user_config.write_text('[install]\nglobalDir="outside-global"\nglobalBinDir="outside-bin"\n')
    before = (user_config.read_bytes(), user_config.stat().st_mtime_ns)
    tools._install_omp_source(recipe, tmp_path / "omp", "linux-x64", run, env)
    assert all(row[1]["BUN_INSTALL_GLOBAL_DIR"] == str(tmp_path / "omp/install/global") for row in calls)
    assert all(row[1]["BUN_INSTALL_BIN"] == str(tmp_path / "omp/bin") for row in calls)
    assert "BUN_INSTALL_GLOBAL_DIR" not in env
    assert not outside.exists()
    assert (user_config.read_bytes(), user_config.stat().st_mtime_ns) == before
