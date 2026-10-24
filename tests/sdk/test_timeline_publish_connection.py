"""Checkout publication writes through the connection used to read its base.

Explicit connections must never ask the launcher for a different Runtime.
The existing Runtime fixture uses its real commit service without sockets.
"""
from __future__ import annotations

import contextlib
from types import SimpleNamespace

import pytest

from astrid.sdk import AstridClient, authoring_bundle, autobootstrap
from astrid.sdk.timeline import store
from astrid.sdk.timeline_checkout import Checkout
from tests.sdk import test_timeline_restructure

restructure_runtime = test_timeline_restructure.restructure_runtime
CANDIDATE = {"project_id": "p", "timeline_id": "t", "base_parent": {"revision_id": "rev-0"}}


class FakeTransport:
    def __init__(self) -> None:
        self.published: list[tuple[str, str, dict, str]] = []

    def publish_parent_composition(self, project_id, timeline_id, publication, *, idempotency_key):
        self.published.append((project_id, timeline_id, publication, idempotency_key))
        return {"data": {"new_head": "rev-1"}}


class FakeClient:
    def __init__(self) -> None:
        self.transport = FakeTransport()
        self._remote = SimpleNamespace(_transport=self.transport)
        self.timelines = SimpleNamespace(open_composition=lambda project, timeline: SimpleNamespace(ok=True, data={"summary": {"head_revision_id": "rev-0"}}))

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


@pytest.fixture(autouse=True)
def no_launcher_and_a_recording_publisher(monkeypatch):
    monkeypatch.setattr(autobootstrap, "ensure_runtime", lambda **kw: pytest.fail("the write asked the launcher for a Runtime"))

    def publish_authoring_candidate(candidate, writer, *, idempotency_key):
        return {"publication": writer.publish_parent_composition("p", "t", {"candidate": True}, idempotency_key=idempotency_key)}

    monkeypatch.setattr(authoring_bundle, "publish_authoring_candidate", publish_authoring_candidate)


def test_a_publish_with_no_client_writes_through_the_connection_it_opens(monkeypatch, restructure_runtime):
    env = restructure_runtime
    checkout = Checkout.open(env.project, "t", client=env.client)
    old_head = checkout.base_revision
    checkout.bundle["parent"]["opaque"]["connected"] = True
    opened = []

    @contextlib.contextmanager
    def connect(cls, **kwargs):
        opened.append(kwargs)
        yield env.client

    monkeypatch.setattr(AstridClient, "open_from_launcher", classmethod(connect))
    receipt = checkout._commit_document(checkout.stored_document(), "Connected edit", idempotency_key="key-1", client=None)
    assert receipt["new_head"] == env.document()["parent_revision"]["revision_id"] and receipt["old_head"] == old_head
    assert len(opened) == 1 and len(env.calls) == 1
    body, key = env.calls[0]
    assert (body["project_id"], body["timeline_id"], key) == (env.project, "t", "key-1")
    assert body["commands"][0]["op"] == "doc.patch"
    assert env.document()["parent_revision"]["payload"]["opaque"]["connected"] is True


def test_a_publish_with_a_client_writes_through_that_client(monkeypatch, restructure_runtime):
    env = restructure_runtime
    checkout = Checkout.open(env.project, "t", client=env.client)
    checkout.bundle["parent"]["opaque"]["connected"] = True
    monkeypatch.setattr(AstridClient, "open_from_launcher", classmethod(lambda cls, **kw: pytest.fail("a second connection was opened")))
    receipt = checkout._commit_document(checkout.stored_document(), "Connected edit", idempotency_key="key-2", client=env.client)
    assert receipt["new_head"] == env.document()["parent_revision"]["revision_id"]
    assert len(env.calls) == 1
    body, key = env.calls[0]
    assert (body["project_id"], body["timeline_id"], key) == (env.project, "t", "key-2")
    assert body["commands"][0]["op"] == "doc.patch"
    assert env.document()["parent_revision"]["payload"]["opaque"]["connected"] is True


def test_a_publish_with_no_client_writes_through_the_connection_it_opens_r4_original(monkeypatch):
    client = FakeClient()
    monkeypatch.setattr(AstridClient, "open_from_launcher", classmethod(lambda cls, **kw: client))
    receipt = store.publish_bundle(dict(CANDIDATE), "key-1")
    assert receipt["new_head"] == "rev-1" and receipt["old_head"] == "rev-0"
    assert client.transport.published == [("p", "t", {"candidate": True}, "key-1")]


def test_a_publish_with_a_client_writes_through_that_client_r4_original(monkeypatch):
    monkeypatch.setattr(AstridClient, "open_from_launcher", classmethod(lambda cls, **kw: pytest.fail("a second connection was opened")))
    client = FakeClient()
    receipt = store.publish_bundle(dict(CANDIDATE), "key-2", client=client)
    assert receipt["new_head"] == "rev-1"
    assert client.transport.published == [("p", "t", {"candidate": True}, "key-2")]
