from __future__ import annotations

import io
import wave
from pathlib import Path

import pytest

from test_timeline_commit_port import prepared

from runtime_protocol.contract_metadata import SCHEMA_DIGEST
from runtime_protocol.errors import ConflictError, NotFoundError
from runtime_protocol.service import RuntimeService
from runtime_protocol.store import RealmStore
from runtime_protocol.timeline_commit import CommitRejected
from runtime_protocol.timeline_commit_port import MediaReads, RequestCommitPort, route_path


class NoopProvider:
    provider_id = "astrid-v1"
    interface_version = 1
    contract_digest = SCHEMA_DIGEST

    def commit(self, _context, _port):
        raise AssertionError("the raw media port test does not commit")


class RawReadProvider:
    provider_id = "astrid-v1"
    interface_version = 1
    contract_digest = SCHEMA_DIGEST

    def __init__(self, service: RuntimeService, *, tamper: bool = False):
        self.service = service
        self.tamper = tamper
        self.calls = 0

    def commit(self, context, port):
        self.calls += 1
        candidate = prepared(context, port)
        pin = candidate["canonical_document"]["dependency_manifest"]["media"][0]
        info = port.media_info(pin)
        assert info["duration_seconds"] == 1.0
        record = candidate["records"]["commands"][0]
        record["dependencies"] = [{"key": "media:raw", "kind": "media", "pin": pin, "policy": "exact"}]
        record["reads"] = [{"ref": "media:" + pin["media_id"], "path": ["duration_seconds"],
                             "state": {"state": "present", "value": info["duration_seconds"]}}]
        if self.tamper:
            path = self.service.cas.path_for(pin["media_id"][7:])
            original = path.read_bytes()
            path.write_bytes(b"tampered")
            try:
                return port.accept(candidate)
            finally:
                path.write_bytes(original)
        return port.accept(candidate)


def _wav_bytes(seconds: int = 1) -> bytes:
    output = io.BytesIO()
    with wave.open(output, "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(8000)
        wav.writeframes(b"\0\0" * 8000 * seconds)
    return output.getvalue()


def _seed(tmp_path: Path, *, include_invalid: bool = False):
    root = tmp_path / "realm"
    RealmStore.initialize(root).close()
    service = RuntimeService(root)
    project = service.create_project({"slug": "raw-audio", "name": "Raw audio"})["id"]
    wav = service.ingest(project, _wav_bytes(), media_type="audio/wav", original_name="music.wav",
                         idempotency_key="wav")["data"]
    objects = [wav]
    if include_invalid:
        objects.append(service.ingest(project, b"not a wav", media_type="audio/wav", original_name="unknown.wav",
                                       idempotency_key="unknown")["data"])
    service.publish_parent_composition(
        project,
        "main",
        {"project_id": project, "timeline_id": "main", "expected_head": None,
         "parent_composition": {},
         "dependency_manifest": {"media": [item["object_id"] for item in objects]}},
        idempotency_key="legacy-seed",
    )
    service.register_timeline_commit_provider(NoopProvider())
    head = service.get_project_timeline(project, "main")
    request = {"api_version": 1, "project_id": project, "timeline_id": "main",
               "base_revision_id": head["head_revision_id"], "base_publication_id": head["head_publication_id"],
               "commands": [{"schema_version": 1, "op": "clip.move", "version": "1",
                              "select": "parent/clip:clip-1", "args": {"on": 2}}]}
    return service, project, objects, request


def _port(service, request):
    commits, _ = service._timeline_commits()
    context = {"request": request,
               "invocation": {"operation": "commitTimeline",
                              "path": route_path(request["project_id"], request["timeline_id"]),
                              "body": request},
               "idempotency_key": "raw-port-read", "request_hash": "raw-port-read-hash",
               "publisher": "test", "realm_id": service.realm["id"]}
    return RequestCommitPort(service, commits, context, lambda: None)


def test_raw_media_info_reads_exact_base_pin_and_wav_header(tmp_path):
    service, _project, objects, request = _seed(tmp_path, include_invalid=True)
    try:
        port = _port(service, request)
        try:
            closure = port.revision_closure(request["base_revision_id"])
            pins = closure["dependency_manifest"]["media"]
            wav_pin = next(pin for pin in pins if pin["media_id"] == objects[0]["object_id"])
            info = port.media_info(wav_pin)
            assert info == {"object_id": objects[0]["object_id"], "media_type": "audio/wav",
                            "size": len(_wav_bytes()), "duration_seconds": 1.0}
            unknown = next(pin for pin in pins if pin != wav_pin)
            assert port.media_info(unknown) == {"object_id": unknown["media_id"], "media_type": "audio/wav",
                                                "size": len(b"not a wav")}
        finally:
            port.close()
    finally:
        service.close()


def test_raw_media_info_refuses_pin_outside_base_closure(tmp_path):
    service, _project, _objects, request = _seed(tmp_path)
    try:
        port = _port(service, request)
        try:
            with pytest.raises(CommitRejected) as error:
                port.media_info({"media_id": "sha256:" + "0" * 64, "content_digest": "sha256:" + "0" * 64})
            assert error.value.failure["details"]["reason"] == "dependency_unavailable"
        finally:
            port.close()
    finally:
        service.close()


def test_raw_media_info_refuses_object_owned_by_another_project(tmp_path):
    service, project, _objects, _request = _seed(tmp_path)
    try:
        foreign = service.create_project({"slug": "foreign", "name": "Foreign"})["id"]
        object_id = service.ingest(foreign, b"foreign-only", media_type="audio/wav", original_name="foreign.wav",
                                    idempotency_key="foreign-wav")["data"]["object_id"]
        with pytest.raises(NotFoundError):
            MediaReads(service).media_info(project, {"media_id": object_id, "content_digest": object_id})
    finally:
        service.close()


@pytest.mark.parametrize("race", ["rename", "inplace"])
def test_raw_media_info_uses_verified_descriptor_under_storage_race(tmp_path, monkeypatch, race):
    service, project, objects, _request = _seed(tmp_path)
    object_id = objects[0]["object_id"]
    path = service.cas.path_for(object_id[7:])
    replacement = tmp_path / "replacement.wav"
    original_path = tmp_path / "original.wav"
    original_verify = RuntimeService._verify_open_file

    def verify_then_race(file_fd, digest, expected_size, *, label):
        result = original_verify(file_fd, digest, expected_size, label=label)
        if race == "rename":
            replacement.write_bytes(_wav_bytes(2))
            path.replace(original_path)
            replacement.replace(path)
        else:
            corrupted = bytearray(_wav_bytes())
            corrupted[:4] = b"XXXX"
            path.write_bytes(corrupted)
        return result

    monkeypatch.setattr(RuntimeService, "_verify_open_file", staticmethod(verify_then_race))
    try:
        pin = {"media_id": object_id, "content_digest": object_id}
        if race == "rename":
            assert MediaReads(service).media_info(project, pin)["duration_seconds"] == 1.0
        else:
            with pytest.raises(ConflictError, match="size does not match|hash or size"):
                MediaReads(service).media_info(project, pin)
    finally:
        if race == "rename":
            path.unlink(missing_ok=True)
            original_path.replace(path)
        else:
            path.write_bytes(_wav_bytes())
        service.close()


def test_raw_media_info_rechecks_tampered_bytes_before_acceptance(tmp_path):
    service, project, _objects, request = _seed(tmp_path)
    provider = RawReadProvider(service, tamper=True)
    service._timeline_commit_provider = provider
    try:
        with pytest.raises(ConflictError):
            service.commit_timeline(project, "main", request, idempotency_key="tamper",
                                    publisher="test", invocation_path=route_path(project, "main"),
                                    authorize=lambda: None)
        assert provider.calls == 1
        assert service.get_project_timeline(project, "main")["head_revision_id"] == request["base_revision_id"]
    finally:
        service.close()


def test_accepted_retry_checks_ledger_before_raw_media_read(tmp_path, monkeypatch):
    service, project, _objects, request = _seed(tmp_path)
    provider = RawReadProvider(service)
    service._timeline_commit_provider = provider
    try:
        accepted = service.commit_timeline(project, "main", request, idempotency_key="retry",
                                            publisher="test", invocation_path=route_path(project, "main"),
                                            authorize=lambda: None)

        def forbidden(*_args, **_kwargs):
            raise AssertionError("accepted retry must not reread raw media")

        monkeypatch.setattr(RequestCommitPort, "media_info", forbidden)
        assert service.commit_timeline(project, "main", request, idempotency_key="retry",
                                       publisher="test", invocation_path=route_path(project, "main"),
                                       authorize=lambda: None) == accepted
        assert provider.calls == 1
    finally:
        service.close()
