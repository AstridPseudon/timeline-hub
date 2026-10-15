"""Offline speech fake through the real command host and Runtime HTTP task loop.

Run with the assigned Runtime worktree and its packages/python on PYTHONPATH.
No provider endpoint is contacted; all speech/network/media behavior is fake.
"""
from datetime import datetime, timedelta, timezone
import json
import sys
from pathlib import Path

import pytest

from banodoco_workspace_client import WorkspaceClient
from runtime_protocol.daemon import RuntimeDaemon
from runtime_protocol.store import RealmStore
from astrid.core.execution.generic_host import GenericPackHost, RuntimeProtocolClient
from astrid.core.execution.provider_failure import ProviderFailure


FAKE_SPEECH = '''
import argparse
from pathlib import Path
from types import SimpleNamespace
from astrid.packs.generation.actions.generate_speech import run

parser = argparse.ArgumentParser()
parser.add_argument('--out')
parser.add_argument('--state')
args = parser.parse_args()
state = Path(args.state)
class RateLimited(Exception):
    status = 429
    headers = {"Retry-After": "7"}
class Communicate:
    def __init__(self, *args, **kwargs): pass
    async def stream(self):
        count = int(state.read_text()) if state.exists() else 0
        state.write_text(str(count + 1))
        if count == 0:
            raise RateLimited("429 fake rejection")
        yield {"type": "audio", "data": b"ID3" + b"x" * 40}
        yield {"type": "WordBoundary", "text": "Hello", "offset": 0, "duration": 10000000}
run._load_edge_tts = lambda: SimpleNamespace(Communicate=Communicate)
run.shutil.which = lambda name: '/fake/' + name
def ffmpeg(argv, **kwargs):
    Path(argv[-1]).write_bytes(b'RIFF' + b'x' * 60)
run.subprocess.run = ffmpeg
run.ffprobe_metadata = lambda path: SimpleNamespace(duration_seconds=1.0)
run.time.sleep = lambda _: (_ for _ in ()).throw(AssertionError('executor local sleep'))
raise SystemExit(run.main(['--text', 'Hello', '--out', args.out]))
'''


def test_speech_fake_429_then_200_through_runtime_retry(tmp_path):
    pack = tmp_path / "fake-pack"
    pack.mkdir()
    script = pack / "fake_speech.py"
    script.write_text(FAKE_SPEECH)
    state = tmp_path / "provider-calls"
    (pack / "executor.yaml").write_text(json.dumps({
        "schema_version": 1, "id": "fixture.speech", "name": "Fake speech", "kind": "external",
        "version": "1.0", "command": {"argv": ["{python_exec}", str(script), "--out", "{out}", "--state", str(state)]},
        "outputs": [{"name": "speech", "type": "file", "path_template": "{out}/audio/speech.wav", "artifact_type": "audio/wav"},
                    {"name": "speech_manifest", "type": "file", "path_template": "{out}/speech-provenance.json", "artifact_type": "application/json"},
                    {"name": "speech_words", "type": "file", "path_template": "{out}/speech-words.json", "artifact_type": "application/json"}],
        "metadata": {"resource_keys": ["cpu"]},
    }))
    root = tmp_path / "realm"
    RealmStore.initialize(root).close()
    daemon = RuntimeDaemon(root, support_root=tmp_path / "support").start()
    try:
        clock = [datetime.now(timezone.utc)]
        daemon.service.store._provider_retry_now = lambda: clock[0]
        generated = WorkspaceClient(daemon.endpoint, daemon.token)
        generated.handshake("provider-retry-test", "0.1.0", ["projects:read", "worker:execute"])
        host = GenericPackHost(pack_roots=[pack], client=RuntimeProtocolClient(daemon.endpoint, daemon.token), executor_id="fake-host")
        host.register()
        record = host.capabilities["fixture.speech"]
        project = generated.create_project("Speech fake", slug="speech-fake", idempotency_key="speech-project")
        task = generated.admit_task(capability_id=record.id, capability_digest=record.capability_digest,
            input_object_ids=[], project_id=project.project_id, idempotency_key="speech-task")
        rejected = host.run(once=True)
        assert len(rejected) == 1 and rejected[0].state == "queued"
        waiting = generated.get_task(task.task_id)
        assert waiting.state == "queued"
        assert daemon.service.task(task.task_id)["task"]["waiting_reason"] == "provider_retry_after"
        assert state.read_text() == "1"
        assert host.run(once=True) == []
        assert state.read_text() == "1"
        clock[0] += timedelta(seconds=7)
        results = host.run(once=True)
        assert len(results) == 1 and results[0].state == "succeeded"
        assert state.read_text() == "2"
        final = generated.get_task(task.task_id)
        assert final.run_id == task.run_id and final.task_id == task.task_id
        assert final.capability_digest == record.capability_digest
        assert len(final.result["outputs"]) == 3
        assert daemon.service.store.conn.execute("SELECT COUNT(*) FROM tasks").fetchone()[0] == 1
        assert daemon.service.store.conn.execute("SELECT COUNT(*) FROM events WHERE kind='task.completed'").fetchone()[0] == 1
        assert host.run(once=True) == []
    finally:
        daemon.stop()
