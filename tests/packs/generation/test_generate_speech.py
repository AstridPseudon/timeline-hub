from __future__ import annotations

import hashlib
import json
import os
import asyncio
import base64
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import pytest

os.environ.setdefault("ASTRID_INTERNAL_INVOCATION", "1")

from astrid.core.contracts.errors import AstridError  # noqa: E402
from astrid.packs.generation.actions.generate_speech import run  # noqa: E402
from astrid.core.execution import network_policy  # noqa: E402

WORD_EVENTS = [
    {"type": "WordBoundary", "offset": 892910, "duration": 1339160, "text": "One"},
    {"type": "WordBoundary", "offset": 2232080, "duration": 1562500, "text": "year"},
    {"type": "WordBoundary", "offset": 3794580, "duration": 3682910, "text": "ago"},
]


@pytest.fixture
def aiohttp_policy(monkeypatch):
    import aiohttp

    assert aiohttp.__version__ == '3.14.1'
    original = aiohttp.ClientSession._request
    redirects = []

    async def request(session, method, url, *, allow_redirects=True, **kwargs):
        redirects.append(allow_redirects)
        return await original(session, method, url, allow_redirects=allow_redirects, **kwargs)

    monkeypatch.setattr(aiohttp.ClientSession, '_request', request)
    monkeypatch.setattr(network_policy, '_AIOHTTP_REQUESTS', {})
    monkeypatch.setattr(network_policy, '_INSTALLED', True)
    monkeypatch.setattr(network_policy, '_POLICY', {'allow_redirects': False})
    network_policy.install_aiohttp_no_redirects(aiohttp)
    return aiohttp, redirects


def _memory_connector(aiohttp, *, status, location, requests, writes):
    from aiohttp.client_proto import ResponseHandler

    class MemoryTransport(asyncio.Transport):
        def __init__(self, protocol, request):
            self.protocol = protocol
            self.request = request
            self.responded = False
            self.closing = False

        def is_closing(self):
            return self.closing

        def get_extra_info(self, name, default=None):
            return default

        def write(self, data):
            writes.append(bytes(data))
            if self.responded:
                return
            self.responded = True
            if status == 101:
                challenge = self.request.headers['Sec-WebSocket-Key'].encode()
                accept = base64.b64encode(hashlib.sha1(
                    challenge + b'258EAFA5-E914-47DA-95CA-C5AB0DC85B11').digest()).decode()
                response = (f'HTTP/1.1 101 Switching Protocols\r\nUpgrade: websocket\r\n'
                    f'Connection: Upgrade\r\nSec-WebSocket-Accept: {accept}\r\n\r\n').encode()
                response += b'\x82\x05audio\x88\x02\x03\xe8'
            else:
                response = (f'HTTP/1.1 {status} Redirect\r\nLocation: {location}\r\n'
                    'Content-Length: 0\r\n\r\n').encode()
            self.protocol.data_received(response)

        def writelines(self, chunks):
            self.write(b''.join(chunks))

        def close(self):
            if not self.closing:
                self.closing = True
                self.protocol.connection_lost(None)

        def abort(self):
            self.close()

    class MemoryConnector(aiohttp.BaseConnector):
        async def _create_connection(self, request, traces, timeout):
            requests.append(str(request.url))
            assert len(requests) == 1, 'unexpected Location follow-on request'
            assert str(request.proxy) == 'http://127.0.0.1:43210'
            assert request.ssl is True
            assert request.proxy_auth is None
            protocol = ResponseHandler(loop=asyncio.get_running_loop())
            protocol.connection_made(MemoryTransport(protocol, request))
            return protocol

    return MemoryConnector(force_close=True)


@pytest.mark.parametrize('status', [301, 302, 303, 307, 308])
@pytest.mark.parametrize('location', [
    'https://api.msedgeservices.com/redirect-target',
    'https://speech.platform.bing.com/redirect-target',
    'https://undeclared.invalid/redirect-target',
])
@pytest.mark.parametrize('entry', ['websocket', 'omitted', 'explicit-true'])
def test_pinned_aiohttp_never_follows_location(aiohttp_policy, status, location, entry):
    aiohttp, redirects = aiohttp_policy
    requests = []
    writes = []
    origin = ('wss' if entry == 'websocket' else 'https') + '://api.msedgeservices.com/original'

    async def exercise():
        connector = _memory_connector(aiohttp, status=status, location=location, requests=requests, writes=writes)
        async with aiohttp.ClientSession(connector=connector) as session:
            if entry == 'websocket':
                with pytest.raises(aiohttp.WSServerHandshakeError) as caught:
                    await session.ws_connect(origin, proxy='http://127.0.0.1:43210', ssl=True)
                assert caught.value.status == status
            else:
                options = {'allow_redirects': True} if entry == 'explicit-true' else {}
                async with session.request('GET', origin, proxy='http://127.0.0.1:43210', ssl=True, **options) as response:
                    assert response.status == status
                    assert response.headers['Location'] == location

    asyncio.run(exercise())
    assert requests == [origin]
    assert redirects == [False]
    assert writes and writes[0].startswith(b'GET /original HTTP/1.1\r\n')


def test_pinned_aiohttp_101_handshake_and_binary_stream_remain_usable(aiohttp_policy):
    aiohttp, redirects = aiohttp_policy
    requests = []
    writes = []
    origin = 'wss://api.msedgeservices.com/original'

    async def exercise():
        connector = _memory_connector(aiohttp, status=101, location='', requests=requests, writes=writes)
        async with aiohttp.ClientSession(connector=connector) as session:
            async with session.ws_connect(origin, proxy='http://127.0.0.1:43210', ssl=True) as websocket:
                await websocket.send_str('offline speech.config')
                message = await websocket.receive()
                assert message.type is aiohttp.WSMsgType.BINARY
                assert message.data == b'audio'

    asyncio.run(exercise())
    assert requests == [origin]
    assert redirects == [False]
    assert len(writes) >= 2


@pytest.mark.parametrize('failure', ['missing-helper', 'missing-policy', 'missing-flag', 'redirect-policy',
    'redirect-alias', 'unproven-installation', 'incompatible-request'])
def test_speech_no_redirect_enforcement_fails_before_communicate(monkeypatch, tmp_path, failure):
    import aiohttp
    import edge_tts

    monkeypatch.setattr(edge_tts, 'Communicate', lambda *args, **kwargs: pytest.fail('communication began'))
    monkeypatch.setattr(network_policy, '_AIOHTTP_REQUESTS', {})
    monkeypatch.setattr(network_policy, '_INSTALLED', failure != 'missing-policy')
    monkeypatch.setattr(network_policy, '_POLICY', {'allow_redirects': failure == 'redirect-policy'})
    if failure == 'missing-flag':
        monkeypatch.setattr(network_policy, '_POLICY', {})
    elif failure == 'redirect-alias':
        network_policy._POLICY['redirects'] = True
    elif failure == 'unproven-installation':
        monkeypatch.setattr(network_policy, '_INSTALLED', 1)
    if failure == 'missing-helper':
        monkeypatch.delattr(network_policy, 'install_aiohttp_no_redirects')
    elif failure == 'incompatible-request':
        async def incompatible(self, method, url):
            pytest.fail('incompatible request ran')
        monkeypatch.setattr(aiohttp.ClientSession, '_request', incompatible)
    with pytest.raises((ImportError, network_policy.NetworkPolicyError)):
        run.generate_core(['--text', 'offline', '--out', str(tmp_path/'outputs')])
    assert not (tmp_path/'outputs').exists()


def test_aiohttp_registration_is_idempotent_and_refuses_replacement(aiohttp_policy, monkeypatch):
    aiohttp, redirects = aiohttp_policy
    installed = aiohttp.ClientSession._request
    network_policy.install_aiohttp_no_redirects(aiohttp)
    assert aiohttp.ClientSession._request is installed

    async def replacement(self, method, url, *, allow_redirects=True):
        pytest.fail('replacement request ran')

    monkeypatch.setattr(aiohttp.ClientSession, '_request', replacement)
    with pytest.raises(network_policy.NetworkPolicyError, match='enforcement changed'):
        network_policy.install_aiohttp_no_redirects(aiohttp)
    assert redirects == []


def test_real_speech_loader_keeps_no_follow_installed_across_declared_fallback(aiohttp_policy, monkeypatch, tmp_path):
    import edge_tts

    aiohttp, redirects = aiohttp_policy
    installed = aiohttp.ClientSession._request
    calls = []
    original_endpoint = edge_tts.communicate.WSS_URL
    monkeypatch.setattr(edge_tts.communicate, 'WSS_URL', original_endpoint)

    class Communicate:
        def __init__(self, text, voice, **kwargs):
            assert aiohttp.ClientSession._request is installed
            assert network_policy._AIOHTTP_REQUESTS[aiohttp.ClientSession] is installed
            calls.append(edge_tts.communicate.WSS_URL)

        async def stream(self):
            if len(calls) == 1:
                raise RuntimeError('offline first-endpoint refusal')
            yield {'type': 'audio', 'data': b'offline'}
            for event in WORD_EVENTS:
                yield dict(event)

    monkeypatch.setattr(edge_tts, 'Communicate', Communicate)
    monkeypatch.setattr(run.shutil, 'which', lambda name: '/fake/'+name)
    monkeypatch.setattr(run.subprocess, 'run', _fake_ffmpeg([]))
    monkeypatch.setattr(run, 'ffprobe_metadata', lambda path: SimpleNamespace(duration_seconds=2.375))
    result = run.generate_core(['--text', 'offline', '--out', str(tmp_path/'outputs')])
    assert result.image_paths
    assert len(calls) == 2
    assert calls[0].startswith('wss://api.msedgeservices.com/')
    assert calls[1] == original_endpoint
    assert redirects == []


def _fake_edge_tts(calls: list[dict], events: list[dict] | None = None):
    class Communicate:
        def __init__(self, text, voice, **kwargs):
            calls.append({"text": text, "voice": voice, **kwargs})

        async def stream(self):
            yield {"type": "audio", "data": b"ID3" + b"x" * 40}
            for event in WORD_EVENTS if events is None else events:
                yield dict(event)

    return SimpleNamespace(Communicate=Communicate)


def _fake_ffmpeg(calls: list[list[str]], *, fail: bool = False):
    def fake_run(argv, **kwargs):
        calls.append(argv)
        if fail:
            raise RuntimeError("stubbed ffmpeg failure")
        Path(argv[-1]).write_bytes(b"RIFF" + b"x" * 60)
        return SimpleNamespace(returncode=0, stdout="", stderr="")

    return fake_run


def test_speech_writes_wav_provenance_and_word_timing(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("ASTRID_BROKER_PROXY", "http://127.0.0.1:43210")
    text = "One year ago, I invited testers into a Discord."
    out = tmp_path / "attempt"
    tts_calls: list[dict] = []
    ffmpeg_calls: list[list[str]] = []
    with patch.object(run, "_load_edge_tts", return_value=_fake_edge_tts(tts_calls)), \
         patch.object(run.shutil, "which", side_effect=lambda name: f"/fake/{name}"), \
         patch.object(run.subprocess, "run", side_effect=_fake_ffmpeg(ffmpeg_calls)), \
         patch.object(run, "ffprobe_metadata", return_value=SimpleNamespace(duration_seconds=2.375)):
        result = run.generate_core([
            "--text", text, "--voice", "en-US-AndrewMultilingualNeural",
            "--rate=+12%", "--volume=-2%", "--pitch=+2Hz", "--out", str(out),
        ])

    assert result.image_paths == [out.resolve() / "audio" / "speech.wav"]
    assert not (out / "audio" / "speech.mp3").exists()
    assert tts_calls == [{
        "text": text, "voice": "en-US-AndrewMultilingualNeural", "rate": "+12%",
        "volume": "-2%", "pitch": "+2Hz", "boundary": "WordBoundary",
        "proxy": "http://127.0.0.1:43210",
    }]

    words = json.loads((out / "speech-words.json").read_text())
    assert words["boundary"] == "WordBoundary"
    assert words["duration_seconds"] == 2.375
    assert words["words"] == [
        {"word": "One", "start_s": 0.089291, "end_s": 0.223207},
        {"word": "year", "start_s": 0.223208, "end_s": 0.379458},
        {"word": "ago", "start_s": 0.379458, "end_s": 0.747749},
    ]

    manifest = json.loads((out / "manifest.json").read_text())
    assert manifest["text"] == text
    assert manifest["text_sha256"] == hashlib.sha256(text.encode()).hexdigest()
    assert manifest["settings"] == {
        "provider": "edge-tts", "voice": "en-US-AndrewMultilingualNeural",
        "rate": "+12%", "volume": "-2%", "pitch": "+2Hz",
    }
    assert manifest["word_count"] == 3
    assert [row["name"] for row in manifest["outputs"]] == ["speech", "speech_manifest", "speech_words"]
    assert manifest["outputs"][2]["path"] == "speech-words.json"
    provenance = json.loads((out / "speech-provenance.json").read_text())
    assert provenance["audio_sha256"] == manifest["audio_sha256"]


def test_missing_word_timing_fails_and_removes_audio(tmp_path: Path) -> None:
    out = tmp_path / "attempt"
    with patch.object(run, "_load_edge_tts", return_value=_fake_edge_tts([], events=[])), \
         patch.object(run.shutil, "which", side_effect=lambda name: f"/fake/{name}"), \
         patch.object(run.subprocess, "run", side_effect=_fake_ffmpeg([])):
        with pytest.raises(AstridError, match="WordBoundary"):
            run.generate_core(["--text", "Hello there.", "--out", str(out)])

    assert not (out / "audio" / "speech.wav").exists()
    assert not (out / "audio" / "speech.mp3").exists()
    assert not (out / "speech-words.json").exists()
    assert not (out / "manifest.json").exists()


def test_decode_failure_removes_false_success_artifacts(tmp_path: Path) -> None:
    out = tmp_path / "attempt"
    with patch.object(run, "_load_edge_tts", return_value=_fake_edge_tts([])), \
         patch.object(run.shutil, "which", side_effect=lambda name: f"/fake/{name}"), \
         patch.object(run.subprocess, "run", side_effect=_fake_ffmpeg([], fail=True)):
        result = run.run_sdk(["--text", "Hello", "--out", str(out)])

    assert result["returncode"] == 1
    assert not (out / "audio" / "speech.wav").exists()
    assert not (out / "speech-words.json").exists()
    assert not (out / "manifest.json").exists()


def test_missing_edge_tts_package_is_a_recoverable_error(tmp_path: Path) -> None:
    missing = AstridError(
        "edge-tts is not installed in this Astrid environment",
        recovery_command="pip install 'astrid[speech]'",
    )
    with patch.object(run, "_load_edge_tts", side_effect=missing):
        result = run.run_sdk(["--text", "Hello", "--out", str(tmp_path / "attempt")])
    assert result["returncode"] == 1
    assert "astrid[speech]" in result["error"]["recovery_command"]


def test_provider_is_explicitly_validated(tmp_path: Path) -> None:
    result = run.run_sdk(["--text", "Hello", "--provider", "other", "--out", str(tmp_path)])
    assert result["returncode"] == 1
    assert list(result["error"]["valid_options"]) == ["edge-tts"]


def test_speech_moves_to_the_next_edge_endpoint_when_one_refuses(tmp_path: Path) -> None:
    calls: list[str] = []
    communicate = SimpleNamespace(WSS_URL="wss://speech.platform.bing.com/legacy?TrustedClientToken=T")

    class Communicate:
        def __init__(self, text, voice, **kwargs):
            pass

        async def stream(self):
            calls.append(communicate.WSS_URL)
            if "msedgeservices" in communicate.WSS_URL:
                raise RuntimeError("403, message='Invalid response status'")
            yield {"type": "audio", "data": b"ID3" + b"x" * 40}
            for event in WORD_EVENTS:
                yield dict(event)

    edge = SimpleNamespace(Communicate=Communicate, communicate=communicate,
                           constants=SimpleNamespace(TRUSTED_CLIENT_TOKEN="T"))
    out = tmp_path / "attempt"
    with patch.object(run, "_load_edge_tts", return_value=edge), \
         patch.object(run.shutil, "which", side_effect=lambda name: f"/fake/{name}"), \
         patch.object(run.subprocess, "run", side_effect=_fake_ffmpeg([])), \
         patch.object(run, "ffprobe_metadata", return_value=SimpleNamespace(duration_seconds=2.375)):
        run.generate_core(["--text", "One year ago", "--out", str(out)])

    assert calls == [
        "wss://api.msedgeservices.com/tts/cognitiveservices/websocket/v1?Ocp-Apim-Subscription-Key=T",
        "wss://speech.platform.bing.com/legacy?TrustedClientToken=T",
    ]
    manifest = json.loads((out / "manifest.json").read_text())
    assert any("api.msedgeservices.com failed" in w for w in manifest["warnings"])


def test_speech_names_every_endpoint_that_failed(tmp_path: Path) -> None:
    communicate = SimpleNamespace(WSS_URL="wss://speech.platform.bing.com/legacy?TrustedClientToken=T")

    class Communicate:
        def __init__(self, text, voice, **kwargs):
            pass

        async def stream(self):
            if "msedgeservices" in communicate.WSS_URL:
                raise RuntimeError("Cannot connect to host api.msedgeservices.com:443")
            raise RuntimeError("403, message='Invalid response status'")
            yield {}

    edge = SimpleNamespace(Communicate=Communicate, communicate=communicate,
                           constants=SimpleNamespace(TRUSTED_CLIENT_TOKEN="T"))
    with patch.object(run, "_load_edge_tts", return_value=edge), \
         patch.object(run.shutil, "which", side_effect=lambda name: f"/fake/{name}"):
        with pytest.raises(AstridError) as caught:
            run.generate_core(["--text", "One year ago", "--out", str(tmp_path / "attempt")])

    message = str(caught.value)
    assert "403" in message
    assert "api.msedgeservices.com failed (RuntimeError: Cannot connect to host" in message


def test_speech_reports_429_once_without_sleep_or_endpoint_fallback(tmp_path: Path) -> None:
    from astrid.core.execution.provider_failure import ProviderFailure, PROVIDER_FAILURE_FILE
    calls = []
    edge = _fake_edge_tts([])
    edge.communicate = SimpleNamespace(WSS_URL="wss://legacy.example/tts")
    edge.constants = SimpleNamespace(TRUSTED_CLIENT_TOKEN="T")

    class RateLimited(Exception):
        status = 429
        headers = {"Retry-After": "7"}

    async def reject(*args, **kwargs):
        calls.append(edge.communicate.WSS_URL)
        raise RateLimited("429")

    out = tmp_path / "attempt"
    with patch.object(run, "_load_edge_tts", return_value=edge), \
         patch.object(run.shutil, "which", return_value="/fake/ffmpeg"), \
         patch.object(run, "_stream_speech", side_effect=reject), \
         patch.object(run.time, "sleep", side_effect=AssertionError("executor slept")):
        result = run.run_sdk(["--text", "One year ago", "--out", str(out)])
        assert result["returncode"] == 1
        assert result["error"]["provider_id"] == "edge-tts"
        assert result["error"]["retryable"] is True
        assert result["error"]["retry_after_seconds"] == 7
        assert len(calls) == 1
        assert run.main(["--text", "One year ago", "--out", str(out)]) == 1
    assert len(calls) == 2
    assert all("msedgeservices" in url for url in calls)
    assert json.loads((out / PROVIDER_FAILURE_FILE).read_text())["retry_after_seconds"] == 7
    assert not (out / "audio/speech.wav").exists()
    assert not (out / "audio/speech.mp3").exists()
    assert not (out / "manifest.json").exists()
