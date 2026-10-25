from __future__ import annotations

import copy
import json
from typing import Any, cast

import pytest

pytest_plugins = ["test_timeline_commit_acceptance"]

from test_timeline_commit_acceptance import context

from runtime_protocol.contract_metadata import SCHEMA_DIGEST
from runtime_protocol.errors import ConflictError, RuntimeErrorBase
from runtime_protocol.timeline_commit import CommitRejected
from runtime_protocol.timeline_commit_execution import _history_diagnostic_reason


class Provider:
    provider_id = "astrid-v1"
    interface_version = 1
    contract_digest = SCHEMA_DIGEST

    def __init__(self, action):
        self.action = action

    def commit(self, commit_context, port):
        return self.action(commit_context, port)


def _failure(message="history refusal"):
    return {
        "http_status": 409,
        "code": "conflict",
        "message": message,
        "details": {
            "status": "refused",
            "reason": "history_unavailable",
            "base": None,
            "current": None,
            "conflicts": [],
        },
    }


def _commit(service, project, request):
    return service.commit_timeline(
        project,
        "main",
        copy.deepcopy(request["request"]),
        idempotency_key=request["idempotency_key"],
        publisher=request["publisher"],
        invocation_path=request["invocation"]["path"],
        authorize=lambda: None,
    )


def _diagnostic(stderr):
    lines = stderr.splitlines()
    assert len(lines) == 1
    prefix, encoded = lines[0].split(" ", 1)
    assert prefix == "runtime.timeline_commit.error"
    return json.loads(encoded)


def test_provider_history_refusal_is_tagged_without_changing_public_reply(realm, capsys):
    service, _, project, head, _ = realm
    request = context(service, project, head, "history-diagnostic-provider")

    def refuse(*_args):
        raise CommitRejected(cast(Any, _failure()))

    service.register_timeline_commit_provider(Provider(refuse))

    with pytest.raises(RuntimeErrorBase) as caught:
        _commit(service, project, request)

    assert caught.value.status == 409
    expected = _failure()
    expected.pop("http_status")
    assert caught.value.as_dict() == expected
    diagnostic = _diagnostic(capsys.readouterr().err)
    assert diagnostic["reason"] == "history_provider_or_store_guard"
    assert diagnostic["exception_class_chain"] == []
    assert diagnostic["frames"] == []


def test_history_tags_are_stable_and_do_not_accept_arbitrary_reason_text():
    assert _history_diagnostic_reason({"details": {"reason": "head_changed"}}) is None
    assert _history_diagnostic_reason({
        "message": "history bounds disagree",
        "details": {"reason": "history_unavailable"},
    }) == "history_port_bounds"
    assert _history_diagnostic_reason({
        "details": {
            "reason": "history_unavailable",
            "integrity_reason": "source_publication_missing",
        },
    }) == "history_baseline_source_publication_missing"


def test_baseline_history_refusal_is_tagged_at_service_boundary(realm, monkeypatch, capsys):
    service, _, project, head, _ = realm
    request = context(service, project, head, "history-diagnostic-baseline")

    def refuse(*_args, **_kwargs):
        raise ConflictError("timeline publication history is unavailable", details={
            "status": "refused",
            "reason": "history_unavailable",
            "integrity_reason": "source_publication_missing",
        })

    monkeypatch.setattr(service, "_ensure_timeline_commit_baseline", refuse)
    service.register_timeline_commit_provider(Provider(lambda *_: None))
    with pytest.raises(ConflictError) as caught:
        _commit(service, project, request)

    assert caught.value.status == 409
    details = cast(dict[str, Any], caught.value.details)
    assert details["reason"] == "history_unavailable"
    diagnostic = _diagnostic(capsys.readouterr().err)
    assert diagnostic["reason"] == "history_baseline_source_publication_missing"

