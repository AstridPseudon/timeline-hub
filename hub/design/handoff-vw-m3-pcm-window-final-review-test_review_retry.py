import pytest

from tests.packs.rendering.test_normal_audio_run import normal_run  # noqa: F401
from astrid.packs.rendering.rendering.renderers.remotion import run as remotion


def test_same_original_pair_retries_with_new_attempt_and_identical_pcm(normal_run):
    state = normal_run
    original = state.timeline_path.read_bytes(), state.registry.read_bytes()
    first_pcm = []

    def fail_first():
        first_pcm.extend(path.read_bytes() for path in state.paths)
        raise RuntimeError('first consumption cancelled')

    state.consume = fail_first
    with pytest.raises(RuntimeError, match='first consumption cancelled'):
        state.execute()
    first_paths = tuple(state.paths)
    assert all(not path.exists() for path in first_paths)
    state.paths.clear()

    def retry():
        assert all(path not in first_paths for path in state.paths)
        assert [path.read_bytes() for path in state.paths] == first_pcm

    state.consume = retry
    state.execute()
    assert all(not path.exists() for path in state.paths)
    assert (state.timeline_path.read_bytes(), state.registry.read_bytes()) == original
    assert state.events == ['server-enter', 'consume', 'server-exit'] * 2


@pytest.mark.parametrize('fail', [False, True], ids=['success', 'consumer-failure'])
def test_reused_managed_root_keeps_original_and_cleans_derived_attempt(normal_run, tmp_path, monkeypatch, fail):
    state = normal_run
    root = tmp_path / 'reused-runtime-root'
    root.mkdir()
    source = root / 'original.wav'
    payload = state.materialized_objects['object-sound']
    source.write_bytes(payload)
    state.materialized_objects['object-sound'] = source
    real_materializer = remotion.AssetMaterializer

    def reused(*args, **kwargs):
        kwargs.update(materialized_root=root, reuse_materialized_paths=True, allow_derived_files=True)
        return real_materializer(*args, **kwargs)

    monkeypatch.setattr(remotion, 'AssetMaterializer', reused)

    def consume():
        assert state.server.root == root
        for path in state.paths:
            path.relative_to(root)
            assert path.is_file()
        if fail:
            raise RuntimeError('reused root consumption failed')

    state.consume = consume
    if fail:
        with pytest.raises(RuntimeError, match='reused root consumption failed'):
            state.execute()
    else:
        state.execute()
    assert source.read_bytes() == payload
    assert list(root.iterdir()) == [source]
    assert all(not path.exists() for path in state.paths)
