from __future__ import annotations

import json

import pytest
from email.message import Message
from io import BytesIO
from pathlib import Path
from types import MethodType

from astrid.packs.training.actions.dataset_build.state import make_initial_state, read_review_state, write_review_state
from astrid.packs.editorial.actions.human_review.run import make_handler_class


def _handler(tmp_path: Path, *, data: object, state: dict | None = None) -> tuple[type, str, Path, Path]:
    html = tmp_path / "index.html"
    data_path = tmp_path / "data.json"
    state_path = tmp_path / "review_state.json"
    out_path = tmp_path / "submit.json"
    media_dir = tmp_path / "media"
    html.write_text("<html>review</html>", encoding="utf-8")
    data_path.write_text(json.dumps(data), encoding="utf-8")
    media_dir.mkdir()
    (media_dir / "clip.mp4").write_bytes(b"0123456789")
    if state is not None:
        write_review_state(state_path, state, now="2026-05-21T00:00:01Z")
    token = "test-token"
    return (
        make_handler_class(
            html_path=html,
            data_path=data_path,
            state_path=state_path if state is not None else None,
            out_path=out_path,
            schema_path=None,
            mounts={"/media": media_dir},
            token=token,
            shutdown_event=_EventStub(),
        ),
        token,
        state_path,
        out_path,
    )


class _EventStub:
    def __init__(self) -> None:
        self.was_set = False

    def set(self) -> None:
        self.was_set = True


def _request(handler_cls: type, method: str, path: str, *, body: object | bytes | None = None, token: str | None = None, headers: dict[str, str] | None = None) -> tuple[int, dict[str, str], bytes]:
    request_headers = dict(headers or {})
    if body is None:
        payload = b""
    elif isinstance(body, bytes):
        payload = body
    else:
        payload = json.dumps(body).encode("utf-8")
        request_headers.setdefault("Content-Type", "application/json")
    if token is not None:
        request_headers["X-Session-Token"] = token
    request_headers["Content-Length"] = str(len(payload))
    request = handler_cls.__new__(handler_cls)
    request.path = path
    request.headers = Message()
    for key, value in request_headers.items():
        request.headers[key] = value
    request.rfile = BytesIO(payload)
    request.wfile = BytesIO()
    request.status = None
    request.response_headers = []

    def send_response(self, status: int) -> None:
        self.status = status

    def send_header(self, key: str, value: str) -> None:
        self.response_headers.append((key, value))

    def end_headers(self) -> None:
        return None

    request.send_response = MethodType(send_response, request)
    request.send_header = MethodType(send_header, request)
    request.end_headers = MethodType(end_headers, request)
    if method == "GET":
        request.do_GET()
    elif method == "POST":
        request.do_POST()
    else:
        raise AssertionError(f"unsupported method: {method}")
    assert request.status is not None
    return request.status, dict(request.response_headers), request.wfile.getvalue()


def _state() -> dict:
    return make_initial_state(
        run_id="run-1",
        writer_id="writer-1",
        buckets={"bucket": 1},
        now="2026-05-21T00:00:00Z",
    )


def test_data_json_without_query_preserves_legacy_full_payload(tmp_path: Path) -> None:
    payload = {"items": [{"item_id": "a"}], "legacy": True}
    handler, token, _, _ = _handler(tmp_path, data=payload)
    status, _, body = _request(handler, "GET", "/data.json", token=token)

    assert status == 200
    assert json.loads(body) == payload


def test_data_json_paginates_and_filters_by_review_status(tmp_path: Path) -> None:
    payload = {
        "items": [
            {"item_id": "a", "review_status": "pending"},
            {"item_id": "b", "review_status": "accepted"},
            {"item_id": "c", "review_status": "accepted"},
        ]
    }
    handler, token, _, _ = _handler(tmp_path, data=payload)
    status, _, body = _request(handler, "GET", "/data.json?status=accepted&offset=1&limit=1", token=token)

    assert status == 200
    page = json.loads(body)
    assert page == {
        "items": [{"item_id": "c", "review_status": "accepted"}],
        "total": 2,
        "offset": 1,
        "limit": 1,
        "status": "accepted",
        "sampled": None,
    }


def test_data_json_filters_by_review_sampled_metadata(tmp_path: Path) -> None:
    payload = {
        "items": [
            {"item_id": "sampled-a", "review_status": "pending", "review_sampled": {"sampled": True}},
            {"item_id": "unsampled-a", "review_status": "pending", "review_sampled": {"sampled": False}},
            {"item_id": "legacy-a", "review_status": "pending"},
        ]
    }
    handler, token, _, _ = _handler(tmp_path, data=payload)
    sampled_status, _, sampled_body = _request(handler, "GET", "/data.json?sampled=true", token=token)
    unsampled_status, _, unsampled_body = _request(handler, "GET", "/data.json?sampled=false", token=token)

    assert sampled_status == 200
    assert unsampled_status == 200
    sampled_page = json.loads(sampled_body)
    unsampled_page = json.loads(unsampled_body)
    assert [item["item_id"] for item in sampled_page["items"]] == ["sampled-a", "legacy-a"]
    assert [item["item_id"] for item in unsampled_page["items"]] == ["unsampled-a"]
    assert sampled_page["sampled"] == "true"
    assert unsampled_page["sampled"] == "false"


def test_data_json_paging_bounds_large_metadata_payloads(tmp_path: Path) -> None:
    payload = {
        "items": [
            {
                "item_id": f"item-{index:03d}",
                "review_status": "pending" if index % 2 else "accepted",
                "source_metadata": {"blob": "x" * 5000, "index": index},
            }
            for index in range(120)
        ]
    }
    handler, token, _, _ = _handler(tmp_path, data=payload)
    status, _, body = _request(handler, "GET", "/data.json?status=pending&offset=10&limit=7", token=token)

    assert status == 200
    page = json.loads(body)
    assert page["total"] == 60
    assert page["offset"] == 10
    assert page["limit"] == 7
    assert [item["item_id"] for item in page["items"]] == [
        "item-021",
        "item-023",
        "item-025",
        "item-027",
        "item-029",
        "item-031",
        "item-033",
    ]
    assert len(page["items"]) == 7
    assert b"item-119" not in body


def test_save_rejects_non_diff_payload_without_overwriting_state(tmp_path: Path) -> None:
    legacy_state = {"seinfeld": True, "items": [{"id": "legacy"}]}
    initial = _state()
    handler, token, state_path, _ = _handler(tmp_path, data=[], state=initial)
    status, _, body = _request(handler, "POST", "/save", body=legacy_state, token=token)

    assert status == 400
    response = json.loads(body)
    assert response["error"] == "diff_required"
    assert read_review_state(state_path)["run_id"] == initial["run_id"]


def test_save_dataset_diff_merges_revision_and_increments_state_version(tmp_path: Path) -> None:
    handler, token, state_path, _ = _handler(tmp_path, data=[], state=_state())
    status, _, body = _request(
        handler,
        "POST",
        "/save",
        token=token,
        body={
            "base_state_version": 1,
            "revisions": [
                {
                    "item_id": "item-1",
                    "decision": "accepted",
                    "edited_caption": "caption edit",
                    "reviewed_at": "2026-05-21T00:00:02Z",
                }
            ],
        },
    )

    assert status == 200
    response = json.loads(body)
    assert response["state_version"] == 2
    state = read_review_state(state_path)
    assert state["state_version"] == 2
    assert state["review_decisions"]["item-1"]["decision"] == "accept"
    assert state["review_decisions"]["item-1"]["edited_caption"] == "caption edit"


def test_save_dataset_diff_returns_409_on_stale_state_without_mutation(tmp_path: Path) -> None:
    handler, token, state_path, _ = _handler(tmp_path, data=[], state=_state())
    initial = read_review_state(state_path)

    status, _, body = _request(
        handler,
        "POST",
        "/save",
        token=token,
        body={
            "base_state_version": initial["state_version"] - 1,
            "revisions": [{"item_id": "item-1", "decision": "accepted"}],
        },
    )

    assert status == 409
    response = json.loads(body)
    assert response["error"] == "stale_state"
    state = read_review_state(state_path)
    assert state["state_version"] == initial["state_version"]
    assert state["review_decisions"] == {}


def test_save_error_statuses_distinguish_stale_from_non_diff_without_mutation(tmp_path: Path) -> None:
    handler, token, state_path, _ = _handler(tmp_path, data=[], state=_state())
    initial = read_review_state(state_path)

    stale_status, _, stale_body = _request(
        handler,
        "POST",
        "/save",
        token=token,
        body={
            "base_state_version": initial["state_version"] - 1,
            "revisions": [{"item_id": "item-1", "decision": "accepted"}],
        },
    )
    non_diff_status, _, non_diff_body = _request(
        handler,
        "POST",
        "/save",
        token=token,
        body={"items": [{"item_id": "legacy-full-state"}]},
    )

    assert stale_status == 409
    assert json.loads(stale_body)["error"] == "stale_state"
    assert non_diff_status == 400
    assert json.loads(non_diff_body)["error"] == "diff_required"
    state = read_review_state(state_path)
    assert state["state_version"] == initial["state_version"]
    assert state["review_decisions"] == {}


def test_save_dataset_diff_normalizes_multiple_revision_statuses_and_updates_timestamp_once(tmp_path: Path) -> None:
    handler, token, state_path, _ = _handler(tmp_path, data=[], state=_state())
    initial = read_review_state(state_path)

    status, _, body = _request(
        handler,
        "POST",
        "/save",
        token=token,
        body={
            "base_state_version": initial["state_version"],
            "revisions": [
                {
                    "item_id": "accepted-item",
                    "decision": "accepted",
                    "edited_caption": "approved edit",
                    "reviewed_at": "2026-05-21T00:01:00Z",
                },
                {
                    "item_id": "rejected-item",
                    "decision": "rejected",
                    "reject_reason": "wrong_content",
                    "reviewed_at": "2026-05-21T00:02:00Z",
                },
                {
                    "item_id": "pending-item",
                    "decision": "pending",
                    "reviewed_at": "2026-05-21T00:03:00Z",
                },
            ],
        },
    )

    assert status == 200
    response = json.loads(body)
    state = read_review_state(state_path)
    assert response["state_version"] == initial["state_version"] + 1
    assert state["state_version"] == initial["state_version"] + 1
    assert state["updated_at"] != initial["updated_at"]
    assert state["review_decisions"]["accepted-item"]["decision"] == "accept"
    assert state["review_decisions"]["accepted-item"]["edited_caption"] == "approved edit"
    assert state["review_decisions"]["rejected-item"]["decision"] == "reject"
    assert state["review_decisions"]["rejected-item"]["reject_reason"] == "wrong_content"
    assert state["review_decisions"]["pending-item"]["decision"] == "pending"


def test_submit_batch_visible_item_ids_merges_with_same_state_guard(tmp_path: Path) -> None:
    handler, token, state_path, _ = _handler(
        tmp_path,
        data={"items": [{"item_id": "a", "review_status": "pending"}, {"item_id": "b", "review_status": "pending"}]},
        state=_state(),
    )
    initial = read_review_state(state_path)

    status, _, body = _request(
        handler,
        "POST",
        "/submit-batch",
        token=token,
        body={
            "base_state_version": initial["state_version"],
            "item_ids": ["a", "b"],
            "decision": "accepted",
        },
    )

    assert status == 200
    response = json.loads(body)
    assert response["state_version"] == initial["state_version"] + 1
    state = read_review_state(state_path)
    assert state["review_decisions"]["a"]["decision"] == "accept"
    assert state["review_decisions"]["b"]["decision"] == "accept"
    assert state["review_decisions"]["a"]["reviewer_id"] == "human_review_batch"


def test_submit_batch_filtered_scope_selects_matching_data_items(tmp_path: Path) -> None:
    handler, token, state_path, _ = _handler(
        tmp_path,
        data={
            "items": [
                {"item_id": "pending-a", "review_status": "pending"},
                {"item_id": "accepted-a", "review_status": "accepted"},
                {"item_id": "pending-b", "review_status": "pending"},
            ]
        },
        state=_state(),
    )
    initial = read_review_state(state_path)

    status, _, _ = _request(
        handler,
        "POST",
        "/submit-batch",
        token=token,
        body={
            "base_state_version": initial["state_version"],
            "scope": "filtered",
            "filter": {"status": "pending"},
            "decision": "rejected",
            "reject_reason": "low_quality",
        },
    )

    assert status == 200
    state = read_review_state(state_path)
    assert sorted(state["review_decisions"]) == ["pending-a", "pending-b"]
    assert state["review_decisions"]["pending-a"]["decision"] == "reject"
    assert state["review_decisions"]["pending-a"]["reject_reason"] == "low_quality"


def test_submit_batch_filtered_scope_can_select_unsampled_items(tmp_path: Path) -> None:
    handler, token, state_path, _ = _handler(
        tmp_path,
        data={
            "items": [
                {"item_id": "sampled-pending", "review_status": "pending", "review_sampled": {"sampled": True}},
                {"item_id": "unsampled-pending", "review_status": "pending", "review_sampled": {"sampled": False}},
                {"item_id": "unsampled-accepted", "review_status": "accepted", "review_sampled": {"sampled": False}},
            ]
        },
        state=_state(),
    )
    initial = read_review_state(state_path)

    status, _, _ = _request(
        handler,
        "POST",
        "/submit-batch",
        token=token,
        body={
            "base_state_version": initial["state_version"],
            "scope": "filtered",
            "filter": {"status": "pending", "sampled": "false"},
            "decision": "accepted",
        },
    )

    assert status == 200
    state = read_review_state(state_path)
    assert sorted(state["review_decisions"]) == ["unsampled-pending"]
    assert state["review_decisions"]["unsampled-pending"]["decision"] == "accept"


def test_submit_batch_requires_token_and_base_state_version(tmp_path: Path) -> None:
    handler, token, _, _ = _handler(tmp_path, data={"items": [{"item_id": "a"}]}, state=_state())

    no_token_status, _, _ = _request(
        handler,
        "POST",
        "/submit-batch",
        body={"base_state_version": 1, "item_ids": ["a"], "decision": "accepted"},
    )
    missing_base_status, _, missing_base_body = _request(
        handler,
        "POST",
        "/submit-batch",
        token=token,
        body={"item_ids": ["a"], "decision": "accepted"},
    )

    assert no_token_status == 403
    assert missing_base_status == 400
    assert json.loads(missing_base_body)["error"] == "base_state_version_required"


def test_submit_batch_returns_409_on_stale_state_without_mutation(tmp_path: Path) -> None:
    handler, token, state_path, _ = _handler(tmp_path, data={"items": [{"item_id": "a"}]}, state=_state())
    initial = read_review_state(state_path)

    status, _, body = _request(
        handler,
        "POST",
        "/submit-batch",
        token=token,
        body={
            "base_state_version": initial["state_version"] - 1,
            "item_ids": ["a"],
            "decision": "accepted",
        },
    )

    assert status == 409
    assert json.loads(body)["error"] == "stale_state"
    state = read_review_state(state_path)
    assert state["state_version"] == initial["state_version"]
    assert state["review_decisions"] == {}


def test_state_and_save_require_token(tmp_path: Path) -> None:
    handler, _, _, _ = _handler(tmp_path, data=[], state=_state())
    state_status, _, _ = _request(handler, "GET", "/state.json")
    save_status, _, _ = _request(handler, "POST", "/save", body={})

    assert state_status == 403
    assert save_status == 403


def test_state_static_range_and_submit_compatibility(tmp_path: Path) -> None:
    handler, token, _, out_path = _handler(tmp_path, data=[], state=_state())
    state_status, _, state_body = _request(handler, "GET", "/state.json", token=token)
    range_status, headers, range_body = _request(handler, "GET", "/media/clip.mp4", headers={"Range": "bytes=2-5"})
    submit_status, _, _ = _request(handler, "POST", "/submit", body={"ok": True}, token=token)

    assert state_status == 200
    assert json.loads(state_body)["state_version"] == 1
    assert range_status == 206
    assert headers["Content-Range"] == "bytes 2-5/10"
    assert range_body == b"2345"
    assert submit_status == 204
    assert json.loads(out_path.read_text(encoding="utf-8")) == {"ok": True}


def _receiver_bridge(monkeypatch, tmp_path, *, transport="socket"):
    import socket
    from astrid.sdk import _child_bridge
    from astrid.packs.editorial.actions.human_review import run as review
    if transport == "pipe":
        from astrid.core.execution._child_pipe import pipe_pair
        parent, channel = pipe_pair()
    else:
        parent, channel = socket.socketpair()
    bridge = _child_bridge.ChildBridge(channel)
    monkeypatch.setattr(_child_bridge, '_bridge', bridge)
    attempt = tmp_path.resolve() / 'task-attempt'
    (attempt / 'outputs').mkdir(parents=True)
    monkeypatch.setenv('TMPDIR', str(attempt / 'outputs'))
    monkeypatch.setenv('ASTRID_PROGRESS_PATH', str(attempt / '.astrid-progress.json'))
    return review, bridge, parent, attempt


def test_managed_receiver_private_publication_and_exact_retirement(tmp_path, monkeypatch):
    import os
    import stat
    review, bridge, parent, attempt = _receiver_bridge(monkeypatch, tmp_path)
    try:
        path = review._managed_receiver_path(attempt / 'outputs' / 'decisions.json')
        owner = review._publish_receiver_session(path, 'http://127.0.0.1:12345/?token=' + 'a'*32)
        row = json.loads(path.read_bytes())
        assert set(row) == {'schema', 'receiver_url', 'process_pid', 'process_birth_id'}
        assert row['process_pid'] == os.getpid() and row['process_birth_id']
        assert stat.S_IMODE(path.stat().st_mode) == 0o600
        assert not (attempt / '.astrid-progress.json').exists()
        review._retire_receiver_session(owner)
        assert not path.exists()
    finally:
        bridge.close(); parent.close()


def test_managed_receiver_rejects_path_and_closed_bridge(tmp_path, monkeypatch):
    import pytest
    review, bridge, parent, attempt = _receiver_bridge(monkeypatch, tmp_path)
    try:
        with pytest.raises(review.HumanReviewInputError, match='paths'):
            review._managed_receiver_path(tmp_path.resolve() / 'elsewhere' / 'decisions.json')
        alias = tmp_path / 'alias'; alias.symlink_to(attempt, target_is_directory=True)
        with pytest.raises(review.HumanReviewInputError, match='paths'):
            review._managed_receiver_path(alias / 'outputs' / 'decisions.json')
        monkeypatch.setenv('TMPDIR', str(alias / 'outputs'))
        with pytest.raises(review.HumanReviewInputError, match='paths'):
            review._managed_receiver_path(attempt / 'outputs' / 'decisions.json')
        bridge.close()
        with pytest.raises(review.HumanReviewInputError, match='live inherited'):
            review._managed_receiver_path(attempt / 'outputs' / 'decisions.json')
    finally:
        bridge.close(); parent.close()



@pytest.mark.parametrize("case", ["live", "bridge_close", "channel_close", "read_close", "write_close",
                                   "read_replaced", "write_replaced", "read_rebound", "write_rebound"])
def test_managed_pipe_receiver_requires_both_original_open_endpoints(tmp_path, monkeypatch, case):
    import os
    review, bridge, parent, attempt = _receiver_bridge(monkeypatch, tmp_path, transport="pipe")
    channel = bridge._channel
    closed_endpoint = None
    try:
        if case == "bridge_close":
            bridge.close()
        elif case == "channel_close":
            channel.close()
        elif case.endswith("_close"):
            closed_endpoint = case.split("_")[0] + "_fd"
            os.close(getattr(channel, closed_endpoint))
        elif case.endswith("_replaced"):
            replacement = os.open(attempt / "replacement", os.O_CREAT | os.O_RDWR, 0o600)
            try:
                os.dup2(replacement, getattr(channel, case.split("_")[0] + "_fd"))
            finally:
                os.close(replacement)
        elif case.endswith("_rebound"):
            from astrid.core.execution._child_pipe import pipe_pair
            other_parent, other_channel = pipe_pair()
            endpoint = case.split("_")[0] + "_fd"
            try:
                os.dup2(getattr(other_channel, endpoint), getattr(channel, endpoint))
            finally:
                other_channel.close()
                other_parent.close()
        if case == "live":
            assert review._managed_receiver_path(attempt / "outputs/decisions.json") == attempt / 'outputs' / review._RECEIVER_SESSION_NAME
        else:
            with pytest.raises(review.HumanReviewInputError, match="live inherited"):
                review._managed_receiver_path(attempt / "outputs/decisions.json")
        assert not (attempt / 'outputs' / review._RECEIVER_SESSION_NAME).exists()
    finally:
        if closed_endpoint is not None:
            setattr(channel, closed_endpoint, -1)
        bridge.close()
        parent.close()



def test_managed_pipe_receiver_serializes_endpoint_check_with_close(tmp_path, monkeypatch):
    import threading
    review, bridge, parent, attempt = _receiver_bridge(monkeypatch, tmp_path, transport="pipe")
    entered, finished = threading.Event(), threading.Event()
    outcomes = []

    def observe():
        entered.set()
        try:
            review._managed_receiver_path(attempt / "outputs/decisions.json")
            outcomes.append("open")
        except review.HumanReviewInputError:
            outcomes.append("closed")
        finally:
            finished.set()

    worker = threading.Thread(target=observe)
    try:
        with bridge._channel._io_lock:
            worker.start()
            assert entered.wait(1)
            assert not finished.wait(.05)
            bridge._channel.close()
        worker.join(timeout=1)
        assert not worker.is_alive() and outcomes == ["closed"]
    finally:
        worker.join(timeout=1)
        bridge.close()
        parent.close()


def test_managed_pipe_receiver_cannot_be_adopted_by_fork(tmp_path, monkeypatch):
    import os
    review, bridge, parent, attempt = _receiver_bridge(monkeypatch, tmp_path, transport="pipe")
    try:
        child = os.fork()
        if child == 0:
            result = 2
            try:
                review._managed_receiver_path(attempt / "outputs/decisions.json")
                result = 1
            except review.HumanReviewInputError:
                result = 0
            finally:
                os._exit(result)
        _, status = os.waitpid(child, 0)
        assert os.waitstatus_to_exitcode(status) == 0
        # Refusal in the child leaves the original parent's channel and path usable.
        assert review._managed_receiver_path(attempt / "outputs/decisions.json") == attempt / 'outputs' / review._RECEIVER_SESSION_NAME
    finally:
        bridge.close()
        parent.close()



@pytest.mark.parametrize("case", ["missing", "relative", "different", "public"])
def test_managed_receiver_requires_the_confined_private_tmpdir(tmp_path, monkeypatch, case):
    review, bridge, parent, attempt = _receiver_bridge(monkeypatch, tmp_path, transport="pipe")
    try:
        if case == "missing":
            monkeypatch.delenv("TMPDIR")
        elif case == "relative":
            monkeypatch.setenv("TMPDIR", "outputs")
        elif case == "different":
            monkeypatch.setenv("TMPDIR", str(tmp_path.resolve() / "other/outputs"))
        else:
            (attempt / "outputs").chmod(0o777)
        # The old progress environment variable cannot rescue a foreign or
        # absent private root in the actual confined launcher layout.
        with pytest.raises(review.HumanReviewInputError, match="paths|owner controlled"):
            review._managed_receiver_path(attempt / "outputs/decisions.json")
        assert not (attempt / "outputs" / review._RECEIVER_SESSION_NAME).exists()
        assert not (attempt / review._RECEIVER_SESSION_NAME).exists()
    finally:
        (attempt / "outputs").chmod(0o700)
        bridge.close()
        parent.close()


@pytest.mark.parametrize("operation", ["observe", "retire"])
def test_managed_receiver_host_refuses_aliased_output_directory(tmp_path, operation):
    from astrid.core.execution import generic_host as host
    attempt = tmp_path.resolve() / "attempt"
    attempt.mkdir()
    foreign = tmp_path.resolve() / "foreign"
    foreign.mkdir()
    path = foreign / host._REVIEW_SESSION_NAME
    path.write_bytes(b"foreign-private-observation")
    (attempt / "outputs").symlink_to(foreign, target_is_directory=True)
    with pytest.raises(host.HostError, match="alias"):
        if operation == "observe":
            host._observe_owned_review_session(object(), attempt)
        else:
            host._retire_owned_review_session(attempt, None)
    assert path.read_bytes() == b"foreign-private-observation"


def test_unmanaged_receiver_never_uses_caller_progress_path(tmp_path, monkeypatch):
    from astrid.sdk import _child_bridge
    from astrid.packs.editorial.actions.human_review import run as review
    monkeypatch.setattr(_child_bridge, '_bridge', None)
    monkeypatch.setenv('ASTRID_PROGRESS_PATH', str(tmp_path / '.astrid-progress.json'))
    assert review._managed_receiver_path(tmp_path / 'decisions.json') is None
    assert not (tmp_path / review._RECEIVER_SESSION_NAME).exists()
    assert not (tmp_path / '.astrid-progress.json').exists()


def test_managed_receiver_refuses_replace_drift_or_nonloopback(tmp_path, monkeypatch):
    import pytest
    review, bridge, parent, attempt = _receiver_bridge(monkeypatch, tmp_path)
    try:
        path = review._managed_receiver_path(attempt / 'outputs' / 'decisions.json')
        with pytest.raises(review.HumanReviewInputError, match='loopback'):
            review._publish_receiver_session(path, 'http://example.com:12345/?token=' + 'a'*32)
        owner = review._publish_receiver_session(path, 'http://127.0.0.1:12345/?token=' + 'a'*32)
        with pytest.raises(FileExistsError):
            review._publish_receiver_session(path, 'http://127.0.0.1:12345/?token=' + 'b'*32)
        path.write_text('{"foreign":true}')
        with pytest.raises(review.HumanReviewInputError, match='mismatch'):
            review._retire_receiver_session(owner)
        assert path.read_text() == '{"foreign":true}'
    finally:
        bridge.close(); parent.close()


@pytest.mark.parametrize("no_open", [True, False])
def test_managed_receiver_live_http_and_secret_free_stdout(tmp_path, monkeypatch, capsys, caplog, no_open):
    import threading
    import time
    import urllib.request
    import logging
    caplog.set_level(logging.DEBUG)
    review, bridge, parent, attempt = _receiver_bridge(monkeypatch, tmp_path)
    html = attempt / 'inputs.html'; html.write_text('<html>review</html>')
    data = attempt / 'data.json'; data.write_text('{}')
    errors = []
    def failed_browser(url):
        raise RuntimeError(url)
    monkeypatch.setattr(review.webbrowser, 'open', failed_browser)
    def serve():
        try:
            assert review.main(['--html', str(html), '--data', str(data), '--out',
                                str(attempt/'outputs'/'decisions.json'), '--timeout', '5',
                                *(['--no-open'] if no_open else [])]) == 0
        except BaseException as exc:
            errors.append(exc)
    thread = threading.Thread(target=serve); thread.start()
    path = attempt / 'outputs' / review._RECEIVER_SESSION_NAME
    try:
        deadline = time.monotonic() + 3
        while not path.exists() and time.monotonic() < deadline:
            time.sleep(.01)
        row = json.loads(path.read_bytes())
        url = row['receiver_url']; token = url.split('token=')[1]
        with urllib.request.urlopen(url, timeout=2) as response:
            assert response.status == 200
        request = urllib.request.Request(url.split('?')[0] + 'submit', data=b'{}',
                    headers={'Content-Type':'application/json','X-Session-Token':token}, method='POST')
        with urllib.request.urlopen(request, timeout=2) as response:
            assert response.status == 204
        thread.join(timeout=3)
        assert not thread.is_alive() and errors == [] and not path.exists()
        captured = capsys.readouterr()
        assert token not in captured.out + captured.err + caplog.text
        assert url not in captured.out + captured.err + caplog.text
        assert (attempt/'outputs'/'decisions.json').read_text().strip() == '{}'
    finally:
        thread.join(timeout=6)
        bridge.close(); parent.close()


def test_managed_receiver_retirement_fifo_replacement_is_bounded(tmp_path, monkeypatch):
    import os
    import pytest
    review, bridge, parent, attempt = _receiver_bridge(monkeypatch, tmp_path)
    try:
        path = review._managed_receiver_path(attempt/'outputs'/'decisions.json')
        owner = review._publish_receiver_session(path, 'http://127.0.0.1:12345/?token='+'a'*32)
        path.unlink(); os.mkfifo(path, 0o600)
        with pytest.raises(review.HumanReviewInputError, match='mismatch'):
            review._retire_receiver_session(owner)
        assert path.exists()
    finally:
        bridge.close(); parent.close()
