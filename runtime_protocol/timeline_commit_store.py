"""Renderer-free persistence for the frozen timeline commit contract.

Callers supply schema/event validation and request-private input captures. Only
this module owns the acceptance transaction; provider execution belongs outside
RealmStore's mutex.
"""
from __future__ import annotations

import base64
import hashlib
import json
import re

from .errors import ConflictError, ProtocolError, ValidationError
from .idempotency import command_result
from .timeline_commit_validation import detached, digest
from .timeline_materialization import has_materialization, item_identity, materialization_join, root_identity
from .util import canonical_json, new_id, now

_METADATA = ("source", "label", "rationale", "group_id")
_DIGEST = re.compile(r"sha256:[0-9a-f]{64}\Z")
_TEXT_BINDING_REF = re.compile(r"occurrence:([^/]+)/text-binding:(prompt|voiceover_script|transcript)(?::([a-z][a-z0-9-]{0,63}))?\Z")


def reject(reason, message=None, *, status=409):
    from .timeline_commit import CommitRejected

    raise CommitRejected({"http_status": status, "code": "conflict" if status == 409 else "validation_error",
                          "message": message or reason, "details": {"status": "refused", "reason": reason,
                          "base": None, "current": None, "conflicts": []}})


def request_identity(context):
    invocation = context["invocation"]
    return hashlib.sha256(canonical_json({"operation": invocation["operation"], "path": invocation["path"],
                          "publisher": context["publisher"], "request": invocation["body"]}).encode()).hexdigest()


def scope(context):
    request = context["request"]
    return canonical_json([request["project_id"], request["timeline_id"]])


_SHELL_SCOPE_TABLES = ("timeline_shots", "timeline_references", "timeline_render_publications",
                       "timeline_document_input_links", "timeline_commit_history")


def has_authored_content(value):
    if isinstance(value, dict):
        return any(has_authored_content(item) for item in value.values())
    if isinstance(value, list):
        return any(has_authored_content(item) for item in value)
    return value is not None


def timeline_scope_is_empty(conn, timeline_id, *, project_id=None):
    """True when nothing is authored under the timeline or its legacy document."""
    if project_id is not None:
        document = conn.execute("SELECT content_json FROM project_documents WHERE id=? AND project_id=?",
                                (f"timeline:{timeline_id}", project_id)).fetchone()
        if document is not None:
            # Baseline verification already rejects duplicate/non-finite JSON.
            # Use the same parser here so corrupt legacy bytes cannot hide
            # authored content behind a last-key-wins decode.
            from .timeline_commit_baseline import _json
            try:
                content = _json(document["content_json"])
            except (TypeError, ValueError):
                return False
            if has_authored_content(content):
                return False
    # Any row keyed to the timeline is authored data.
    for table in _SHELL_SCOPE_TABLES:
        if conn.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name=?", (table,)).fetchone() and \
                conn.execute(f"SELECT 1 FROM {table} WHERE timeline_id=? LIMIT 1", (timeline_id,)).fetchone():
            return False
    # create_timeline snapshots the empty shell as timeline_revisions v1; only a non-empty snapshot is authored.
    if conn.execute("SELECT 1 FROM timeline_revisions WHERE timeline_id=? AND (shots_json!='[]' OR references_json!='[]') LIMIT 1",
                    (timeline_id,)).fetchone():
        return False
    for child in ("composition_revision_occurrences", "composition_revision_dependencies"):
        if conn.execute(f"SELECT 1 FROM {child} c JOIN parent_composition_revisions r ON r.id=c.parent_revision_id "
                        "WHERE r.timeline_id=? LIMIT 1", (timeline_id,)).fetchone():
            return False
    return True


class TimelineCommitStore:
    def __init__(self, store, *, validate_prepared, validate_event=None):
        self.store = store
        # Validation uses the wire worker's authoritative schema, including
        # Agent-owned leaves. It must raise on invalid data, never normalize it.
        self.validate_prepared = validate_prepared
        self.validate_event = validate_event

    @property
    def conn(self):
        return self.store.conn

    def _membership(self, project_id, timeline_id):
        row = self.conn.execute("SELECT p.realm_id FROM timelines t JOIN projects p ON p.id=t.project_id "
                                "WHERE t.id=? AND t.project_id=? AND t.archived_at IS NULL",
                                (timeline_id, project_id)).fetchone()
        if row is None:
            reject("history_unavailable")
        return row["realm_id"]

    def lookup(self, context, *, authorize):
        with self.store._mutex:
            authorize()
            request = context["request"]
            if self._membership(request["project_id"], request["timeline_id"]) != context["realm_id"]:
                reject("authority_changed")
            return self._lookup(context)

    def _lookup(self, context):
        row = self.conn.execute("SELECT * FROM command_idempotency WHERE command_kind='timeline.commit' "
                                "AND aggregate_id=? AND idempotency_key=?", (scope(context), context["idempotency_key"])).fetchone()
        if row is None:
            return None
        if row["request_hash"] != context["request_hash"]:
            reject("idempotency_mismatch")
        edge = self.conn.execute("SELECT * FROM timeline_commit_history WHERE publication_id=?", (row["txn_id"],)).fetchone()
        if edge is None or edge["project_id"] != context["request"]["project_id"] or edge["timeline_id"] != context["request"]["timeline_id"]:
            raise ProtocolError("accepted commit history is missing or corrupt")
        self._verify_accepted(row, edge)
        return self._envelope(row, edge["project_id"])

    def _verify_accepted(self, row, edge):
        from .timeline_commit import CommitRejected
        try:
            data, records = json.loads(row["result_json"]), json.loads(edge["records_json"])
            previous = {"revision_id": edge["previous_revision_id"], "publication_id": edge["previous_publication_id"]}
            document = data["canonical_document"]
            valid = (edge["intent"] == "recorded" and row["command_kind"] == "timeline.commit"
                     and row["txn_id"] == edge["publication_id"]
                     and row["aggregate_id"] == canonical_json([edge["project_id"], edge["timeline_id"]])
                     and row["primary_stream_id"] == edge["timeline_id"]
                     and row["first_project_seq"] == row["last_project_seq"] == edge["project_seq"]
                     and data["accepted_revision_id"] == document["parent_revision"]["revision_id"] == edge["revision_id"]
                     and document["project_id"] == edge["project_id"] and document["timeline_id"] == edge["timeline_id"]
                     and data["document_digest"] == digest(document)
                     and canonical_json(data["commands"]) == canonical_json([r["command"] for r in records["commands"]])
                     and data["previous_revision_id"] == previous["revision_id"]
                     and data["previous_publication_id"] == previous["publication_id"]
                     and data["publisher"] == edge["publisher"]
                     and all(data[k] == edge[k] for k in ("provider_version", "compiler_version"))
                     and {k: data[k] for k in _METADATA if k in data} == json.loads(edge["metadata_json"]))
            base = {"revision_id": data["base_revision_id"], "publication_id": data["base_publication_id"]}
            valid = valid and data["status"] == ("accepted" if previous == base else "rebased")
            valid = valid and data["rebased_onto"] == (None if previous == base else previous)
            ids = json.loads(row["event_ids_json"])
            seq = row["resulting_stream_seq"]
            # Replay verifies the accepted prefix, independent of later writes.
            events = self.conn.execute("SELECT * FROM timeline_events WHERE timeline_id=? ORDER BY id LIMIT ?",
                                       (edge["timeline_id"], seq)).fetchall()
            valid = valid and isinstance(ids, list) and 0 < len(ids) <= seq <= len(events)
            valid = valid and ids == [str(e["id"]) for e in events[seq - len(ids):seq]]
            project_seq = self.conn.execute("SELECT next_seq FROM project_sequences WHERE project_id=?",
                                            (edge["project_id"],)).fetchone()
            valid = valid and project_seq is not None and 0 < edge["project_seq"] < project_seq[0]
            previous_hash = ""
            for event in events:
                hashed = {"timeline_id": edge["timeline_id"], "kind": event["kind"],
                          "payload": json.loads(event["payload_json"]), "previous_hash": previous_hash,
                          "created_at": event["created_at"]}
                valid = valid and event["previous_hash"] == previous_hash and event["event_hash"] == digest(hashed)[7:]
                previous_hash = event["event_hash"]
            event = self.conn.execute("SELECT * FROM timeline_events WHERE id=? AND timeline_id=?",
                                      (ids[-1], edge["timeline_id"])).fetchone()
            valid = valid and event is not None and event["kind"] == "timeline.commit.accepted"
            if valid:
                payload = json.loads(event["payload_json"])
                valid = payload == {"project_id": edge["project_id"], "timeline_id": edge["timeline_id"],
                                    "previous": previous, "revision_id": edge["revision_id"],
                                    "publisher": edge["publisher"], "intent": "recorded",
                                    "records_digest": digest(records)}
            if not valid:
                raise ValueError()
            prepared = {**data, "records": records, "expected_head": previous}
            if has_materialization(prepared):
                project, timeline = edge["project_id"], edge["timeline_id"]
                allocations = materialization_join(prepared, project, timeline,
                    lambda revision: self.revision_closure(project, timeline, revision))
                if canonical_json(document) != canonical_json(self.revision_closure(project, timeline, edge["revision_id"])):
                    raise ValueError()
                self._check_inherited_allocations(project, timeline, records, allocations, edge["project_seq"])
        except (KeyError, TypeError, ValueError, IndexError, ValidationError, CommitRejected) as exc:
            raise ProtocolError("accepted commit record is corrupt") from exc

    def _check_inherited_allocations(self, project, timeline, records, allocations, before_seq=None):
        inverse_refs = {d["key"].removeprefix("materialization.source:")
                        for r in records["commands"] if r["command"]["op"] == "timeline.inverse"
                        for d in r["dependencies"] if d["key"].startswith("materialization.source:")}
        if not inverse_refs:
            return
        inherited = {}
        for publication in records["undo_of"]:
            if before_seq is not None:
                row = self.conn.execute("SELECT project_seq FROM timeline_commit_history WHERE publication_id=?",
                                        (publication,)).fetchone()
                if row is None or row[0] >= before_seq:
                    reject("invalid_records")
            entry = self.history_entry(project, timeline, publication)
            data = entry["receipt"]["result"]
            target = {**data, "records": entry["records"], "expected_head": entry["previous"]}
            if has_materialization(target):
                for shot, allocation in materialization_join(target, project, timeline,
                        lambda revision: self.revision_closure(project, timeline, revision)).items():
                    if shot in inherited and canonical_json(inherited[shot]) != canonical_json(allocation):
                        reject("invalid_records")
                    inherited[shot] = allocation
        if any(canonical_json(allocations.get(ref.removeprefix("shot:"))) !=
               canonical_json(inherited.get(ref.removeprefix("shot:"))) for ref in inverse_refs):
            reject("invalid_records", "inverse allocation lacks authenticated provenance")

    @staticmethod
    def _envelope(row, project_id):
        data = (json.loads(row["result_json"]) if row["command_kind"] == "parent_composition.publish" else
                command_result(row["result_json"], kind="timeline.commit", created_at=row["created_at"]))
        receipt = {"receipt_id": row["txn_id"], "command_kind": row["command_kind"],
                   "idempotency_key": row["idempotency_key"], "request_hash": row["request_hash"],
                   "project_id": project_id, "project_seq": [row["first_project_seq"], row["last_project_seq"]],
                   "event_ids": json.loads(row["event_ids_json"]), "result": data, "created_at": row["created_at"]}
        return detached({"data": data, "receipt": receipt})

    def head(self, project_id, timeline_id):
        with self.store._mutex:
            self._membership(project_id, timeline_id)
            row = self.conn.execute("SELECT revision_id, publication_id FROM parent_composition_heads "
                                    "WHERE project_id=? AND timeline_id=?", (project_id, timeline_id)).fetchone()
            if row is None or not row["revision_id"] or not row["publication_id"]:
                reject("history_unavailable")
            entry = self.history_entry(project_id, timeline_id, row["publication_id"])
            if entry["revision_id"] != row["revision_id"]:
                reject("history_unavailable")
            from .timeline_commit_baseline import _publication_events, _shot_projection, _text_bindings
            from .timeline_catalog import verify_catalog_tail
            ledger = self.conn.execute("SELECT resulting_stream_seq, last_project_seq FROM command_idempotency WHERE txn_id=?",
                                       (row["publication_id"],)).fetchone()
            try:
                events, _, _ = _publication_events(self.conn, project_id, timeline_id)
                catalog = verify_catalog_tail(self.conn, project_id, timeline_id, events, ledger[0], ledger[1],
                                              legacy=entry["intent"] == "legacy_unknown")
                if catalog:
                    from .cas import ContentAddressedStore
                    document = self.revision_closure(project_id, timeline_id, row["revision_id"])
                    if entry["intent"] == "recorded" and document != entry["receipt"]["result"]["canonical_document"]:
                        reject("history_unavailable", "canonical film differs from accepted publication")
                    for shot in document["shot_revisions"]:
                        _shot_projection(self.conn, project_id, shot["shot_id"])
                        _text_bindings(self.conn, project_id, shot, ContentAddressedStore(self.store.cas_root).read)
            except ConflictError as exc:
                from .timeline_commit import CommitRejected
                raise CommitRejected({"http_status": 409, "code": "conflict",
                                      "message": "timeline has untracked writes",
                                      "details": {"base": None, "current": None, "conflicts": [], **exc.details}}) from exc
            except (KeyError, TypeError, ValueError, IndexError):
                reject("history_unavailable", "timeline catalog facts are corrupt")
            return dict(row)

    def history_entry(self, project_id, timeline_id, publication_id):
        with self.store._mutex:
            self._membership(project_id, timeline_id)
            row = self.conn.execute("SELECT * FROM timeline_commit_history WHERE publication_id=? "
                                    "AND project_id=? AND timeline_id=?", (publication_id, project_id, timeline_id)).fetchone()
            if row is None:
                reject("history_unavailable")
            ledger = self.conn.execute("SELECT * FROM command_idempotency WHERE txn_id=?", (publication_id,)).fetchone()
            if ledger is None or ledger["first_project_seq"] != row["project_seq"]:
                reject("history_unavailable")
            if row["intent"] == "recorded" or ledger["command_kind"] == "timeline.commit":
                self._verify_accepted(ledger, row)
            previous = None if row["previous_publication_id"] is None else {
                "revision_id": row["previous_revision_id"], "publication_id": row["previous_publication_id"]}
            return {"publication_id": publication_id, "revision_id": row["revision_id"], "previous": previous,
                    "receipt": self._envelope(ledger, project_id)["receipt"], "intent": row["intent"],
                    "records": json.loads(row["records_json"]) if row["records_json"] is not None else None,
                    "provider_version": row["provider_version"], "compiler_version": row["compiler_version"],
                    "publisher": row["publisher"], **json.loads(row["metadata_json"])}

    def history(self, project_id, timeline_id, through, after_publication_id=None, cursor=None, limit=100):
        if type(limit) is not int or not 1 <= limit <= 200:
            raise ValidationError("history limit must be 1–200")
        with self.store._mutex:
            bound = self.history_entry(project_id, timeline_id, through["publication_id"])
            if bound["revision_id"] != through["revision_id"]:
                reject("history_unavailable")
            after = self.history_entry(project_id, timeline_id, after_publication_id) if after_publication_id else None
            low = after["receipt"]["project_seq"][0] if after else 0
            high = bound["receipt"]["project_seq"][0]
            cursor_scope = [project_id, timeline_id, through, after_publication_id]
            start = low
            if cursor is not None:
                try:
                    decoded = json.loads(base64.urlsafe_b64decode(cursor.encode()))
                    if decoded["scope"] != cursor_scope or type(decoded["seq"]) is not int or not low < decoded["seq"] <= high:
                        raise ValueError()
                    start = decoded["seq"]
                except (ValueError, KeyError, TypeError) as exc:
                    raise ValidationError("invalid history cursor") from exc
            if low > high:
                reject("history_unavailable")
            rows = self.conn.execute("SELECT publication_id FROM timeline_commit_history WHERE project_id=? AND timeline_id=? "
                                     "AND project_seq>? AND project_seq<=? ORDER BY project_seq LIMIT ?",
                                     (project_id, timeline_id, start, high, limit + 1)).fetchall()
            items = [self.history_entry(project_id, timeline_id, row[0]) for row in rows[:limit]]
            previous = self.conn.execute("SELECT publication_id, revision_id FROM timeline_commit_history WHERE project_id=? "
                                        "AND timeline_id=? AND project_seq<=? ORDER BY project_seq DESC LIMIT 1",
                                        (project_id, timeline_id, start)).fetchone()
            expected = dict(previous) if previous else None
            for entry in items:
                if entry["previous"] != expected:
                    reject("history_unavailable")
                expected = {"publication_id": entry["publication_id"], "revision_id": entry["revision_id"]}
            if len(rows) <= limit and expected != through:
                reject("history_unavailable")
            next_cursor = None
            if len(rows) > limit:
                next_cursor = base64.urlsafe_b64encode(canonical_json({"scope": cursor_scope,
                    "seq": items[-1]["receipt"]["project_seq"][0]}).encode()).decode()
            return {"items": items, "next_cursor": next_cursor, "head": detached(through)}

    def revision_closure(self, project_id, timeline_id, revision_id):
        with self.store._mutex:
            self._membership(project_id, timeline_id)
            parent = self.conn.execute("SELECT * FROM parent_composition_revisions WHERE id=? AND project_id=? AND timeline_id=?",
                                       (revision_id, project_id, timeline_id)).fetchone()
            if parent is None:
                reject("history_unavailable")
            if parent["commit_manifest_json"] is None:
                from .cas import ContentAddressedStore
                from .timeline_commit_baseline import verify_revision_source
                document = verify_revision_source(self.conn, project_id, timeline_id, revision_id,
                                                   read_object=ContentAddressedStore(self.store.cas_root).read)
                self._validate_closure(document)
                return document
            manifest = json.loads(parent["commit_manifest_json"])
            document = {"schema_version": 1, "project_id": project_id, "timeline_id": timeline_id,
                        "parent_revision": self._image(parent), "shot_revisions": [],
                        "internal_timeline_revisions": [], "dependency_manifest": manifest}
            for family, table in (("shot_revisions", "shot_revisions"), ("internal_timeline_revisions", "internal_timeline_revisions")):
                pins = manifest["shots" if family == "shot_revisions" else "internal_timelines"]
                for pin in pins:
                    row = self.conn.execute(f"SELECT * FROM {table} WHERE id=? AND project_id=?", (pin["revision_id"], project_id)).fetchone()
                    if row is None:
                        reject("history_unavailable")
                    image = self._image(row)
                    image.update({key: row[key] for key in ("shot_id", "internal_timeline_revision_id") if key in row.keys()})
                    if family == "internal_timeline_revisions":
                        image["timeline_id"] = row["timeline_id"]
                    document[family].append(image)
            self._validate_closure(document)
            self._verify_inputs(document)
            return document

    def _verify_inputs(self, document):
        for pin in document["dependency_manifest"]["documents"]:
            row = self.conn.execute("SELECT c.content_json, c.content_size, b.kind FROM timeline_document_input_contents c "
                "JOIN timeline_document_input_bindings b ON b.content_digest=c.content_digest "
                "JOIN timeline_document_input_links l ON l.project_id=b.project_id AND l.document_id=b.document_id "
                "AND l.document_version=b.document_version AND l.content_digest=b.content_digest "
                "WHERE l.project_id=? AND l.timeline_id=? AND l.revision_id=? AND b.document_id=? "
                "AND b.document_version=? AND b.content_digest=? LIMIT 1",
                (document["project_id"], document["timeline_id"], document["parent_revision"]["revision_id"],
                 pin["document_id"], pin["version"], pin["content_digest"])).fetchone()
            if row is None or digest(json.loads(row["content_json"])) != pin["content_digest"] or len(row["content_json"].encode()) != row["content_size"]:
                reject("dependency_unavailable", "retained input is missing or corrupt")
            from .timeline_commit_inputs import PROJECT_PACK_KIND, validate_pack_snapshot_objects
            if row["kind"] == PROJECT_PACK_KIND:
                validate_pack_snapshot_objects(self.conn, document["project_id"], json.loads(row["content_json"]))

    def integrity_errors(self):
        errors = []
        previous = {}
        for edge in self.conn.execute("SELECT * FROM timeline_commit_history ORDER BY project_id, timeline_id, project_seq"):
            try:
                key = (edge["project_id"], edge["timeline_id"])
                expected = previous.get(key)
                actual = (edge["previous_publication_id"], edge["previous_revision_id"])
                if actual != (expected if expected else (None, None)):
                    raise ValueError("history ancestry mismatch")
                previous[key] = (edge["publication_id"], edge["revision_id"])
                ledger = self.conn.execute("SELECT * FROM command_idempotency WHERE txn_id=?", (edge["publication_id"],)).fetchall()
                if len(ledger) != 1 or ledger[0]["first_project_seq"] != edge["project_seq"]:
                    raise ValueError("history receipt missing or ambiguous")
                if edge["intent"] == "recorded":
                    self._verify_accepted(ledger[0], edge)
                    self._verify_inputs(json.loads(ledger[0]["result_json"])["canonical_document"])
                elif edge["records_json"] is not None or ledger[0]["command_kind"] != "parent_composition.publish":
                    raise ValueError("invented legacy provenance")
            except Exception as exc:
                errors.append({"table": "timeline_commit_history", "id": edge["publication_id"], "reason": str(exc)})
        for key, expected in previous.items():
            head = self.conn.execute("SELECT publication_id, revision_id FROM parent_composition_heads WHERE project_id=? AND timeline_id=?", key).fetchone()
            if head is None or tuple(head) != expected:
                errors.append({"table": "parent_composition_heads", "id": key[1], "reason": "publication head mismatch"})
        for row in self.conn.execute("SELECT * FROM timeline_document_input_contents"):
            try:
                value = detached(json.loads(row["content_json"]))
                if digest(value) != row["content_digest"] or canonical_json(value) != row["content_json"] or len(row["content_json"].encode()) != row["content_size"]:
                    raise ValueError("retained input digest mismatch")
            except Exception as exc:
                errors.append({"table": "timeline_document_input_contents", "id": row["content_digest"], "reason": str(exc)})
        for row in self.conn.execute("SELECT l.* FROM timeline_document_input_links l LEFT JOIN timeline_commit_history h "
                                     "ON h.publication_id=l.publication_id AND h.project_id=l.project_id "
                                     "AND h.timeline_id=l.timeline_id AND h.revision_id=l.revision_id WHERE h.publication_id IS NULL"):
            errors.append({"table": "timeline_document_input_links", "id": row["publication_id"], "reason": "orphan retained input link"})
        return errors

    def shot_closure(self, project_id, shot_id, revision_id):
        with self.store._mutex:
            row = self.conn.execute("SELECT * FROM shot_revisions WHERE id=? AND project_id=? AND shot_id=?",
                                    (revision_id, project_id, shot_id)).fetchone()
            if row is None:
                reject("dependency_unavailable")
            internal = self.conn.execute("SELECT * FROM internal_timeline_revisions WHERE id=? AND project_id=?",
                                         (row["internal_timeline_revision_id"], project_id)).fetchone()
            if internal is None:
                reject("dependency_unavailable")
            shot = {**self._image(row), "shot_id": shot_id, "internal_timeline_revision_id": internal["id"]}
            image = {**self._image(internal), "timeline_id": internal["timeline_id"]}
            if digest(shot["payload"]) != shot["content_digest"] or digest(image["payload"]) != image["content_digest"]:
                reject("dependency_unavailable")
            if shot["payload"].get("internal_timeline_revision_id") != internal["id"]:
                reject("dependency_unavailable")
            manifests = self.conn.execute("SELECT DISTINCT json_extract(p.commit_manifest_json, '$.media'), "
                "json_extract(p.commit_manifest_json, '$.documents') FROM parent_composition_revisions p "
                "JOIN composition_revision_occurrences o ON o.parent_revision_id=p.id "
                "WHERE p.project_id=? AND o.shot_id=? AND o.shot_revision_id=? AND p.commit_manifest_json IS NOT NULL LIMIT 2",
                (project_id, shot_id, revision_id)).fetchall()
            if len(manifests) != 1:
                reject("history_unavailable", "shot input closure is unavailable or ambiguous")
            parent = self.conn.execute("SELECT p.timeline_id, p.id FROM parent_composition_revisions p "
                "JOIN composition_revision_occurrences o ON o.parent_revision_id=p.id "
                "WHERE p.project_id=? AND o.shot_id=? AND o.shot_revision_id=? AND p.commit_manifest_json IS NOT NULL ORDER BY p.id LIMIT 1",
                (project_id, shot_id, revision_id)).fetchone()
            if parent is None:
                reject("history_unavailable")
            document = self.revision_closure(project_id, parent["timeline_id"], parent["id"])
            return {"shot_revision": shot, "internal_timeline_revision": image,
                    "media": document["dependency_manifest"]["media"], "documents": document["dependency_manifest"]["documents"]}

    def _verify_parent_rows(self, document):
        parent_id = document["parent_revision"]["revision_id"]
        occurrences = document["parent_revision"]["payload"]["occurrences"]
        rows = self.conn.execute("SELECT * FROM composition_revision_occurrences WHERE parent_revision_id=? ORDER BY ordinal", (parent_id,)).fetchall()
        if len(rows) != len(occurrences):
            reject("history_unavailable")
        for ordinal, (row, occurrence) in enumerate(zip(rows, occurrences)):
            expected = {"parent_revision_id": parent_id, "project_id": document["project_id"], "ordinal": ordinal,
                        **{k: occurrence[k] for k in ("occurrence_id", "shot_id", "shot_revision_id", "duration_ms", "track")},
                        "gain": occurrence.get("gain", 1),
                        "muted": int(occurrence.get("muted", occurrence.get("mute", False))),
                        "placement_json": canonical_json(occurrence["placement"]),
                        **{k + "_json": canonical_json(occurrence.get(k, default)) for k, default in
                           (("source_offset", 0), ("speed", 1), ("transform", {}), ("provenance", {}))}}
            if dict(row) != expected:
                reject("history_unavailable")
        manifest = document["dependency_manifest"]
        expected = [("shot_revision", p["revision_id"], p["content_digest"]) for p in manifest["shots"]]
        expected += [("internal_timeline_revision", p["revision_id"], p["content_digest"]) for p in manifest["internal_timelines"]]
        expected += [("media", p["media_id"], p["content_digest"]) for p in manifest["media"]]
        rows = self.conn.execute("SELECT dependency_kind, dependency_id, content_digest, ordinal FROM composition_revision_dependencies "
                                 "WHERE parent_revision_id=? ORDER BY ordinal", (parent_id,)).fetchall()
        if [tuple(row) for row in rows] != [(*pin, ordinal) for ordinal, pin in enumerate(expected)]:
            reject("history_unavailable")

    @staticmethod
    def _image(row):
        return {"revision_id": row["id"], "content_digest": row["content_digest"], "payload": json.loads(row["payload_json"])}

    def _validate_closure(self, document):
        from .visual_seam import parent_clips

        project_id, timeline_id = document["project_id"], document["timeline_id"]
        self._membership(project_id, timeline_id)
        parent = document["parent_revision"]
        try:
            parent_clips(parent["payload"])
        except (ConflictError, ValidationError) as exc:
            reject("invalid_closure", str(exc), status=422)
        shots, internals = document["shot_revisions"], document["internal_timeline_revisions"]
        manifest = document["dependency_manifest"]
        for clip in parent["payload"]["clips"]:
            if not isinstance(clip, dict) or set(clip) & {"occurrence_id", "shot_revision_id", "parent_revision_id", "composition_revision_id"}:
                reject("invalid_closure", "ordinary clips cannot contain nested compositions", status=422)
        for images, table, identity in (([parent], "parent_composition_revisions", "timeline_id"),
                                        (shots, "shot_revisions", "shot_id"), (internals, "internal_timeline_revisions", "timeline_id")):
            if len({image["revision_id"] for image in images}) != len(images):
                reject("invalid_closure", status=422)
            for image in images:
                if digest(image["payload"]) != image["content_digest"]:
                    reject("invalid_closure", "revision content digest mismatch", status=422)
                owner_id = image.get(identity, timeline_id)
                existing = self.conn.execute(f"SELECT * FROM {table} WHERE id=?", (image["revision_id"],)).fetchone()
                if existing is not None and (existing["project_id"] != project_id or existing[identity] != owner_id
                        or existing["payload_json"] != canonical_json(image["payload"]) or existing["content_digest"] != image["content_digest"]):
                    reject("revision_identity_mismatch")
                if table == "parent_composition_revisions" and existing is not None and existing["commit_manifest_json"] is not None:
                    if existing["commit_manifest_json"] != canonical_json(manifest):
                        reject("revision_identity_mismatch", "revision dependency closure changed")
                if table == "internal_timeline_revisions":
                    payload = image["payload"]
                    nested_fields = {"occurrences", "occurrence_records", "parent_composition", "nested_composition",
                                     "occurrence_id", "shot_revision_id", "parent_revision_id", "composition_revision_id"}
                    # Only authored structure is reserved; params and provenance remain opaque.
                    if set(payload) & nested_fields or any(set(clip) & nested_fields for clip in payload.get("clips", [])):
                        reject("invalid_closure", "internal timeline cannot contain a nested composition", status=422)
                    owner = self.conn.execute("SELECT project_id FROM timelines WHERE id=?", (owner_id,)).fetchone()
                    shot_id = owner_id.removeprefix("shot:") if owner_id.startswith("shot:") else None
                    if owner is None and shot_id:
                        owner = self.conn.execute("SELECT project_id FROM project_shots WHERE id=?", (shot_id,)).fetchone()
                        if owner is None and any(s["shot_id"] == shot_id for s in shots):
                            owner = {"project_id": project_id}
                    if owner is None or owner["project_id"] != project_id:
                        reject("invalid_closure", "internal timeline scope mismatch")
                if table == "shot_revisions":
                    if existing is not None and existing["internal_timeline_revision_id"] != image["internal_timeline_revision_id"]:
                        reject("revision_identity_mismatch")
                    owner = self.conn.execute("SELECT project_id FROM project_shots WHERE id=?", (owner_id,)).fetchone()
                    if owner is not None and owner["project_id"] != project_id:
                        reject("invalid_closure", "shot scope mismatch")
                    if image["payload"].get("internal_timeline_revision_id") != image["internal_timeline_revision_id"]:
                        reject("invalid_closure", status=422)
                    payload = image["payload"]
                    if set(payload) & {"occurrences", "occurrence_records", "parent_composition", "parent_revision_id", "composition_revision_id"}:
                        reject("invalid_closure", "nested shot composition", status=422)
                    if not isinstance(payload.get("items", []), list) or any(not isinstance(item, dict)
                            or not isinstance(item.get("item_id", item.get("id")), str) or not item.get("media_id")
                            for item in payload.get("items", [])):
                        reject("invalid_closure", "shot items cannot be projected", status=422)
        shot_keys = {(s["shot_id"], s["revision_id"]) for s in shots}
        occurrences = parent["payload"]["occurrences"]
        for occurrence in occurrences:
            speed = occurrence.get("speed", 1)
            valid_speed = (type(speed) in (int, float) and speed > 0) or (isinstance(speed, dict)
                and set(speed) == {"numerator", "denominator"} and all(type(v) is int and v > 0 for v in speed.values()))
            if not valid_speed or not occurrence["placement"] or not isinstance(occurrence.get("muted", occurrence.get("mute", False)), bool):
                reject("invalid_closure", "invalid occurrence timing or placement", status=422)
            if "muted" in occurrence and "mute" in occurrence and occurrence["muted"] != occurrence["mute"]:
                reject("invalid_closure", "ambiguous occurrence mute", status=422)
        if shot_keys != {(o["shot_id"], o["shot_revision_id"]) for o in occurrences}:
            reject("invalid_closure", "incomplete or extraneous shot closure", status=422)
        if len({o["occurrence_id"] for o in occurrences}) != len(occurrences):
            reject("invalid_closure", "duplicate occurrences", status=422)
        if {s["internal_timeline_revision_id"] for s in shots} != {i["revision_id"] for i in internals}:
            reject("invalid_closure", "incomplete or extraneous internal closure", status=422)
        for images, key, fields, sort_keys in ((shots, "shots", ("shot_id", "revision_id", "internal_timeline_revision_id", "content_digest"), ("shot_id", "revision_id")),
                (internals, "internal_timelines", ("timeline_id", "revision_id", "content_digest"), ("timeline_id", "revision_id"))):
            ordered = sorted(images, key=lambda image: tuple(image[k] for k in sort_keys))
            if images != ordered or manifest[key] != [{k: image[k] for k in fields} for image in ordered]:
                reject("invalid_closure", "manifest does not equal complete closure", status=422)
        media = manifest["media"]
        if media != sorted(media, key=lambda item: item["media_id"]) or len({m["media_id"] for m in media}) != len(media):
            reject("invalid_closure", status=422)
        for pin in media:
            if not _DIGEST.fullmatch(pin["media_id"]) or pin["content_digest"] != pin["media_id"]:
                reject("invalid_closure", status=422)
            row = self.conn.execute("SELECT o.size FROM objects o JOIN project_objects p ON p.digest=o.digest "
                                    "WHERE p.project_id=? AND p.relation='managed' AND o.digest=?", (project_id, pin["media_id"][7:])).fetchone()
            if row is None:
                reject("dependency_unavailable")
            from .cas import ContentAddressedStore
            data = ContentAddressedStore(self.store.cas_root).read(pin["media_id"][7:])
            if len(data) != row["size"] or "sha256:" + hashlib.sha256(data).hexdigest() != pin["media_id"]:
                reject("dependency_unavailable")
        payload_media = set()
        def collect(value):
            if isinstance(value, dict):
                for key, child in value.items():
                    if key in {"media_id", "object_id"} and isinstance(child, str):
                        normalized = child if child.startswith("sha256:") else "sha256:" + child
                        if _DIGEST.fullmatch(normalized):
                            payload_media.add(normalized)
                    collect(child)
            elif isinstance(value, list):
                for child in value:
                    collect(child)
        for image in [parent, *shots, *internals]:
            collect(image["payload"])
        if not payload_media <= {m["media_id"] for m in media}:
            reject("invalid_closure", "unaccounted media", status=422)
        pins = manifest["documents"]
        if pins != sorted(pins, key=lambda p: (p["document_id"], p["version"], p["content_digest"])) or len({canonical_json(p) for p in pins}) != len(pins):
            reject("invalid_closure", status=422)
        existing = self.conn.execute("SELECT 1 FROM parent_composition_revisions WHERE id=?", (parent["revision_id"],)).fetchone()
        if existing is not None:
            self._verify_parent_rows(document)

    def _validate(self, context, prepared, inputs):
        # Callers run _check_shot_destinations first, which validates the schema.
        request = context["request"]
        document = prepared["canonical_document"]
        if (document["project_id"], document["timeline_id"]) != (request["project_id"], request["timeline_id"]):
            reject("invalid_closure", status=422)
        if prepared["document_digest"] != digest(document):
            reject("invalid_closure", "whole-document digest mismatch", status=422)
        self._validate_closure(document)
        records = prepared["records"]
        commands = records["commands"]
        if not commands or [r["ordinal"] for r in commands] != list(range(len(commands))):
            reject("invalid_records", status=422)
        for record in commands:
            if any(write["cause"] >= len(commands) for write in record["derived_writes"]):
                reject("invalid_records", status=422)
        undo_seqs = [self.history_entry(request["project_id"], request["timeline_id"], publication_id)["receipt"]["project_seq"][0]
                     for publication_id in records["undo_of"]]
        if undo_seqs != sorted(set(undo_seqs)):
            reject("invalid_records", "undo targets must follow acceptance order", status=422)
        restored = records["restored_from"]
        if restored is not None:
            source = self.revision_closure(request["project_id"], request["timeline_id"], restored["revision_id"])
            if source["parent_revision"]["content_digest"] != restored["content_digest"]:
                reject("invalid_records", status=422)
        for event in prepared["semantic_events"]:
            if event["command_ordinal"] >= len(commands) or self.validate_event is None:
                reject("invalid_event", status=422)
            self.validate_event(event)
        if inputs is not None and not has_materialization(prepared):
            inputs.validate(prepared)
        elif inputs is None and (document["dependency_manifest"]["documents"] or any(r["dependencies"] for r in commands)):
            reject("dependency_unavailable", "request-private dependency captures required")
        allocations = self._materializations(context, prepared, inputs)
        self._check_inherited_allocations(request["project_id"], request["timeline_id"], records, allocations)
        return {"canonical_document": document, "document_digest": prepared["document_digest"],
                "commands": [r["command"] for r in commands], "id_map": prepared["id_map"],
                "provider_version": prepared["provider_version"], "compiler_version": prepared["compiler_version"]}

    def _materializations(self, context, prepared, inputs):
        if has_materialization(prepared):
            from .timeline_commit_port import RequestCommitPort
            if not isinstance(inputs, RequestCommitPort) or canonical_json(inputs._provider_context()) != canonical_json(context):
                reject("dependency_unavailable", "request-private materialization captures required")
            return inputs.validate(prepared)
        return materialization_join(prepared, context["request"]["project_id"], context["request"]["timeline_id"],
                                    lambda _: reject("dependency_unavailable"))

    @staticmethod
    def _same_materialization_slot(shot, owner, allocation, prior_allocation, before, after):
        if allocation is None or allocation[0] != owner:
            return False
        pin = allocation[1]
        source = pin["source"]
        edge = [(o["shot_id"], o["shot_revision_id"]) for o in before["parent_revision"]["payload"]["occurrences"]
                if o["occurrence_id"] == owner]
        if edge != [(source["shot_id"], source["revision_id"])]:
            return False
        output = [o["shot_id"] for o in after["parent_revision"]["payload"]["occurrences"] if o["occurrence_id"] == owner]
        members = {i.get("item_id", i.get("id")) for s in after["shot_revisions"]
                   if s["shot_id"] == shot for i in s["payload"].get("items", [])}
        if output != [shot]:
            return False
        if prior_allocation is not None:
            return canonical_json(allocation) == canonical_json(prior_allocation)
        # Frozen M1 edges have no new allocation facts. Their already verified
        # source/binding/read proof remains usable only with this exact closure.
        return (canonical_json(pin["parent"]) == canonical_json({k: before["parent_revision"][k]
                                                                for k in ("revision_id", "content_digest")})
                and members == set(source["item_id_map"].values()))

    def _check_shot_destinations(self, context, prepared, inputs=None):
        # Check the wire shape before inspecting destinations. This preflight
        # precedes closure validation so foreign occupants get the same refusal.
        try:
            self.validate_prepared(prepared)
        except Exception:
            reject("invalid_prepared", "prepared commit does not satisfy the frozen schema", status=422)
        document, records = prepared["canonical_document"], prepared["records"]
        project, timeline = context["request"]["project_id"], context["request"]["timeline_id"]
        # Exact immutable reuse does not write the mutable shot projection.
        writes = [s for s in document["shot_revisions"] if self.conn.execute(
            "SELECT 1 FROM shot_revisions WHERE id=?", (s["revision_id"],)).fetchone() is None]
        if len({s["shot_id"] for s in writes}) != len(writes):
            reject("identity_collision")
        # Agent owns command.created consistency. Reserve the exact recorded
        # reference without interpreting command arguments or inventing ID forms.
        claims = [(item["kind"], item["ref"]) for record in records["commands"]
                  if record["command"]["op"] != "timeline.inverse" for item in record["created"]]
        claims = [(kind, self._reservation_identity(kind, ref)) for kind, ref in claims]
        if len(set(claims)) != len(claims):
            reject("identity_collision")
        self._check_birth_destinations(claims)
        occupied = set()
        for image in writes:
            row = self.conn.execute("SELECT project_id FROM project_shots WHERE id=?", (image["shot_id"],)).fetchone()
            if row is not None:
                if row["project_id"] != project:
                    reject("destination_occupied")
                occupied.add(image["shot_id"])
        allocations = self._materializations(context, prepared, inputs)
        if not writes and not claims:
            return
        current = self.revision_closure(project, timeline, prepared["expected_head"]["revision_id"])
        owned = {s["shot_id"] for s in current["shot_revisions"]}
        fresh = {s["shot_id"] for s in writes} - owned
        for shot in fresh:
            for row in self.conn.execute("SELECT project_id FROM shot_revisions WHERE shot_id=?", (shot,)):
                if row["project_id"] != project:
                    reject("destination_occupied")
                occupied.add(shot)
        heads = {shot: self.conn.execute("SELECT revision_id FROM shot_revision_heads WHERE shot_id=? AND project_id=?",
                                        (shot, project)).fetchone() for shot in occupied}

        def unchanged(shot, revision):
            return heads[shot] is not None and heads[shot]["revision_id"] == revision

        authorized = set()
        for image in current["shot_revisions"]:
            shot = image["shot_id"]
            if shot in occupied and unchanged(shot, image["revision_id"]):
                # A film pin authorizes its own projection, not a newer catalog
                # head written since that pin was accepted.
                occupied.remove(shot)
                authorized.add(shot)
        restored_items = set()
        if occupied:
            from .timeline_commit_port import command_leaves

            requested = [p for c in command_leaves(context["request"]["commands"])
                         if c["op"] == "timeline.inverse" for p in c["args"]["publications"]]
            if requested != prepared["records"]["undo_of"]:
                reject("destination_occupied")

            def edges(value):
                return {o["occurrence_id"]: (o["shot_id"], o["shot_revision_id"])
                        for o in value["parent_revision"]["payload"]["occurrences"]}

            active, output = edges(current), edges(document)
            cursor, remaining = prepared["expected_head"], set(requested)
            while cursor and (occupied or remaining):
                # history_entry authenticates the records against the receipt/event.
                entry = self.history_entry(project, timeline, cursor["publication_id"])
                previous = entry["previous"]
                if entry["intent"] == "recorded":
                    before = self.revision_closure(project, timeline, previous["revision_id"])
                    prior = edges(before)
                    if entry["publication_id"] in remaining:
                        for o, (shot, _) in prior.items():
                            owner, source = "occurrence:" + o, before["parent_revision"]
                            if (shot in occupied and unchanged(shot, prior[o][1])
                                    and output.get(o, (None,))[0] == shot) and any(
                                    w["ref"] == "shot:" + shot or w["ref"] == owner or w["ref"].startswith(owner + "/")
                                    or (w["ref"] == "timeline" and not w["path"] and w["before"] == {
                                        "state": "present", "value": {k: source[k] for k in ("revision_id", "content_digest")}})
                                    for r in entry["records"]["commands"] for w in r["writes"]):
                                occupied.discard(shot)
                                authorized.add(shot)
                                restored_items.update(i.get("item_id", i.get("id"))
                                    for s in before["shot_revisions"] if s["shot_id"] == shot
                                    for i in s["payload"].get("items", []))
                        remaining.remove(entry["publication_id"])
                    accepted_document = self.revision_closure(project, timeline, entry["revision_id"])
                    after = edges(accepted_document)
                    historical = {**entry["receipt"]["result"], "records": entry["records"], "expected_head": previous}
                    prior_allocations = (materialization_join(historical, project, timeline,
                        lambda revision: self.revision_closure(project, timeline, revision))
                        if has_materialization(historical) else {})
                    for o, (shot, _) in after.items():
                        owner = "occurrence:" + o
                        if shot in allocations or shot in prior_allocations:
                            if not self._same_materialization_slot(shot, o, allocations.get(shot),
                                    prior_allocations.get(shot), before, accepted_document):
                                continue
                        if (shot in occupied and unchanged(shot, after[o][1])
                                and output.get(o, (None,))[0] == shot and o in prior
                                and active.get(o) == prior[o]
                                and any(any(b["ref"] == owner for b in r["bindings"])
                                        and any(read["ref"] == owner + "/shot" and read["path"] == ["shot_id"]
                                                and read["state"] == {"state": "present", "value": prior[o][0]}
                                                for read in r["reads"]) for r in entry["records"]["commands"])):
                            occupied.remove(shot)
                            authorized.add(shot)
                cursor = previous
            if occupied or remaining:
                reject("destination_occupied")
        destinations, fresh_items = {}, set()
        old_items = {s["shot_id"]: {i.get("item_id", i.get("id")) for i in s["payload"].get("items", [])}
                     for s in current["shot_revisions"]}
        for image in writes:
            shot = image["shot_id"]
            for item in image["payload"].get("items", []):
                identity = item.get("item_id", item.get("id"))
                if not identity or identity in destinations:
                    reject("identity_collision")
                destinations[identity] = shot
                if identity not in old_items.get(shot, set()):
                    fresh_items.add(identity)
        for identity, shot in destinations.items():
            row = self.conn.execute("SELECT shot_id FROM shot_items WHERE id=?", (identity,)).fetchone()
            if row is not None and (row["shot_id"] != shot or shot not in authorized):
                reject("identity_collision")
            for retained in self.conn.execute(
                    "SELECT DISTINCT s.* FROM shot_revisions s, json_each(s.payload_json, '$.items') i "
                    "WHERE COALESCE(json_extract(i.value, '$.item_id'), json_extract(i.value, '$.id'))=?", (identity,)):
                if (digest(json.loads(retained["payload_json"])) != retained["content_digest"]
                        or retained["project_id"] != project or retained["shot_id"] != shot or shot not in authorized):
                    reject("identity_collision")
        if not fresh and not fresh_items and not claims:
            return
        # Missing history cannot prove that a free ID was never reserved. Exact
        # matching records are authenticated against their durable receipt/event.
        if self.conn.execute("SELECT 1 FROM command_idempotency c LEFT JOIN timeline_commit_history h ON h.publication_id=c.txn_id "
                             "WHERE c.command_kind='timeline.commit' AND h.publication_id IS NULL LIMIT 1").fetchone():
            reject("identity_collision")
        reservations = set(claims) | {("shot", "shot:" + shot) for shot in fresh - authorized}
        reservations.update(("item", identity) for identity in fresh_items - restored_items)
        for kind, ref in reservations:
            rows = self.conn.execute(
                "SELECT DISTINCT h.* FROM timeline_commit_history h, "
                "json_each(h.records_json, '$.commands') r, json_each(r.value, '$.created') i "
                "WHERE json_extract(i.value, '$.kind')=? AND (json_extract(i.value, '$.ref')=? OR ?='item') "
                "AND (h.project_id=? OR ?='item') AND (h.timeline_id=? OR ? IN ('shot', 'item'))",
                (kind, ref, kind, project, kind, timeline, kind)).fetchall()
            for entry in rows:
                if kind == "item" and not any(i["kind"] == "item" and self._reservation_identity("item", i["ref"]) == ref
                        for r in json.loads(entry["records_json"])["commands"]
                        if r["command"]["op"] != "timeline.inverse" for i in r["created"]):
                    continue
                ledger = self.conn.execute("SELECT * FROM command_idempotency WHERE txn_id=?", (entry["publication_id"],)).fetchone()
                if ledger is None:
                    reject("identity_collision")
                self._verify_accepted(ledger, entry)
                reject("identity_collision")

    @staticmethod
    def _reservation_identity(kind, ref):
        if kind == "item":
            member = item_identity(ref)
            if member is None:
                reject("invalid_records", "item reservation requires a canonical item ref", status=422)
            return member[1]
        if kind == "shot" and (root_identity(ref) is None or root_identity(ref)[0] != "shot"):
            reject("invalid_records", "shot reservation requires a canonical shot ref", status=422)
        return ref

    def _check_birth_destinations(self, claims):
        # Native births reserve even if a later command removes the new root.
        # Derived allocations never supply these claims; inverses were excluded.
        for kind, ref in claims:
            if kind == "shot":
                shot = root_identity(ref)[1]
                if (self.conn.execute("SELECT 1 FROM project_shots WHERE id=?", (shot,)).fetchone()
                        or self.conn.execute("SELECT 1 FROM shot_revisions WHERE shot_id=?", (shot,)).fetchone()):
                    reject("destination_occupied")
            elif kind == "item":
                if (self.conn.execute("SELECT 1 FROM shot_items WHERE id=?", (ref,)).fetchone()
                        or self.conn.execute("SELECT 1 FROM shot_revisions s, json_each(s.payload_json, '$.items') i "
                            "WHERE COALESCE(json_extract(i.value, '$.item_id'), json_extract(i.value, '$.id'))=? LIMIT 1", (ref,)).fetchone()):
                    reject("identity_collision")

    def preview(self, context, prepared, *, authorize, inputs=None):
        context, prepared = detached(context), detached(prepared)
        with self.store._mutex:
            authorize()
            if not context["request"].get("dry_run", False):
                reject("preview_requires_dry_run", status=422)
            self._check_context(context)
            self._check_head(context, prepared["expected_head"])
            self._check_shot_destinations(context, prepared, inputs)
            candidate = self._validate(context, prepared, inputs)
            request = context["request"]
            return {"data": {"status": "preview", "base_revision_id": request["base_revision_id"],
                            "base_publication_id": request["base_publication_id"],
                            "evaluated_head": prepared["expected_head"], **candidate}, "receipt": None}

    def _check_context(self, context):
        request = context["request"]
        realm = self._membership(request["project_id"], request["timeline_id"])
        if realm != context["realm_id"] or request_identity(context) != context["request_hash"]:
            reject("invocation_mismatch", status=422)
        if context["invocation"]["operation"] == "commitTimeline" and request != context["invocation"]["body"]:
            reject("invocation_mismatch", status=422)
        if self.history_entry(request["project_id"], request["timeline_id"], request["base_publication_id"])["revision_id"] != request["base_revision_id"]:
            reject("history_unavailable")

    def _check_head(self, context, expected):
        from .timeline_commit import StaleHead

        request = context["request"]
        current = self.head(request["project_id"], request["timeline_id"])
        if current != expected:
            raise StaleHead(current)
        base = {"revision_id": request["base_revision_id"], "publication_id": request["base_publication_id"]}
        if any(c["op"] == "timeline.restore" for c in request["commands"]) and expected != base:
            reject("stale_head")

    def accept(self, context, prepared, *, authorize, inputs=None):
        context, prepared = detached(context), detached(prepared)
        with self.store._mutex:
            if self.conn.in_transaction:
                raise ProtocolError("commit acceptance requires the outer transaction")
            with self.store._transaction():
                authorize()
                replay = self._lookup(context)
                if replay is not None:
                    return replay
                if context["request"].get("dry_run", False):
                    reject("dry_run_accept", status=422)
                self._check_context(context)
                self._check_head(context, prepared["expected_head"])
                self._check_shot_destinations(context, prepared, inputs)
                candidate = self._validate(context, prepared, inputs)
                request, previous = context["request"], prepared["expected_head"]
                from .timeline_commit_reference_projection import (
                    ReferenceProjectionError,
                    prepare_reference_projection,
                )
                try:
                    previous_document = self.revision_closure(
                        request["project_id"], request["timeline_id"], previous["revision_id"]
                    )
                    timeline = self.conn.execute(
                        "SELECT version FROM timelines WHERE id=? AND project_id=?",
                        (request["timeline_id"], request["project_id"]),
                    ).fetchone()
                    reference_projection = prepare_reference_projection(
                        self.conn, candidate["canonical_document"], previous_document,
                        next_version=int(timeline["version"]) + 1,
                    )
                except ReferenceProjectionError as exc:
                    reject(exc.reason, exc.message, status=exc.status)
                base = {"revision_id": request["base_revision_id"], "publication_id": request["base_publication_id"]}
                data = {"status": "accepted" if previous == base else "rebased", "base_revision_id": base["revision_id"],
                        "base_publication_id": base["publication_id"], "previous_revision_id": previous["revision_id"],
                        "previous_publication_id": previous["publication_id"],
                        "accepted_revision_id": candidate["canonical_document"]["parent_revision"]["revision_id"],
                        "rebased_onto": None if previous == base else previous, **candidate, "publisher": context["publisher"],
                        **{k: request[k] for k in _METADATA if k in request}}
                self._persist_closure(candidate["canonical_document"])
                result = self._publish(context, data, previous, prepared["records"], prepared["semantic_events"])
                from .timeline_commit_reference_projection import (
                    apply_reference_projection,
                )
                if reference_projection is not None:
                    apply_reference_projection(self.conn, reference_projection)
                self._project_text_bindings(candidate["canonical_document"], prepared["records"], result["receipt"]["receipt_id"])
                if inputs is not None:
                    inputs.persist(prepared, result["receipt"]["receipt_id"], data["accepted_revision_id"])
                return result

    def _project_text_bindings(self, document, records, publication_id):
        """Derive live text-binding rows and events from the accepted recorder's writes.

        Runs in the acceptance transaction after _persist_closure; only this commit's
        writes are projected, so historical reuse never repoints a live row.
        """
        project_id = document["project_id"]
        shots = {o["occurrence_id"]: o["shot_id"] for o in document["parent_revision"]["payload"]["occurrences"]}
        for record in records["commands"]:
            for write in record["writes"]:
                if "/text-binding:" not in write["ref"]:
                    continue
                match = _TEXT_BINDING_REF.fullmatch(write["ref"])
                if match is None or write["path"]:
                    reject("invalid_records", "malformed text binding write", status=422)
                occurrence, kind, slot = match.groups()
                owner = "occurrence:" + occurrence
                read = next((r for r in record["reads"] if r["ref"] == owner + "/shot" and r["path"] == ["shot_id"]), None)
                shot_id = shots.get(occurrence)
                if shot_id is None or read is None or read["state"] != {"state": "present", "value": shot_id}:
                    reject("text_binding_owner_changed", "text binding owner differs from the accepted shot")
                self._project_text_binding(project_id, shot_id, kind, slot, write["before"], write["after"], publication_id)

    def _project_text_binding(self, project_id, shot_id, kind, slot, before, after, publication_id):
        from .service import RuntimeService
        from .timeline_commit_port import verify_retained_text_object, verify_text_object
        from .cas import ContentAddressedStore

        owner = self.conn.execute("SELECT project_id FROM project_shots WHERE id=?", (shot_id,)).fetchone()
        if owner is None or owner["project_id"] != project_id:
            reject("dependency_unavailable", "text binding shot is not in this project")
        binding_id = RuntimeService._text_binding_id(project_id, shot_id, kind, slot)
        row = self.conn.execute("SELECT * FROM shot_text_bindings WHERE id=? AND project_id=?", (binding_id, project_id)).fetchone()
        latest = None
        if row is not None:
            events = RuntimeService._text_binding_events(self.conn, row)
            latest = json.loads(events[-1]["payload_json"])
        live = latest is not None and latest.get("state", "present") == "present"
        current = None
        if live:
            media = self.conn.execute("SELECT size, media_type FROM objects WHERE digest=?", (row["media_digest"],)).fetchone()
            if media is None:
                reject("dependency_unavailable", "bound text media is missing")
            current = {"kind": row["kind"], "slot": row["slot"], "media_id": "sha256:" + row["media_digest"],
                       "content_hash": "sha256:" + row["media_digest"], "byte_size": media["size"], "mime_type": media["media_type"]}
        fields = ("kind", "slot", "media_id", "content_hash", "byte_size", "mime_type")
        if (before["state"] == "present") != live or (live and any(
                before["value"].get(field) != current[field] for field in fields)):
            reject("text_binding_mismatch", "recorded text binding state differs from the live binding")
        clearing = after["state"] == "absent"
        if clearing and not live:
            reject("text_binding_mismatch", "cannot clear an absent text binding")
        value = current if clearing else after["value"]
        for descriptor in ([current] if live else []) + ([] if clearing else [value]):
            selection = {"object_id": descriptor.get("media_id"), "digest": descriptor.get("content_hash"),
                         "size": descriptor.get("byte_size"), "media_type": descriptor.get("mime_type")}
            if (descriptor.get("kind"), descriptor.get("slot")) != (kind, slot):
                reject("invalid_records", "text binding row differs from its key", status=422)
            cas = ContentAddressedStore(self.store.cas_root)
            if selection["media_type"] == "text/plain" and row is not None:
                verify_retained_text_object(self.conn, cas, row, selection)
            else:
                verify_text_object(self.conn, cas, project_id, selection)
        object_digest = value["media_id"][7:]
        timestamp = now()
        if row is None:
            self.conn.execute("INSERT INTO shot_text_bindings(id, project_id, shot_id, kind, slot, media_digest, event_stream_id, head_seq, created_at, updated_at) "
                              "VALUES (?, ?, ?, ?, ?, ?, ?, 0, ?, ?)",
                              (binding_id, project_id, shot_id, kind, slot, object_digest, binding_id + ":shot.text_binding", timestamp, timestamp))
            head, previous_hash = 0, ""
        elif live and not clearing and row["media_digest"] == object_digest:
            return
        else:
            head = row["head_seq"]
            previous_hash = self.conn.execute("SELECT event_hash FROM shot_text_binding_events WHERE binding_id=? AND seq=?",
                                              (binding_id, head)).fetchone()["event_hash"]
        event_id, seq = new_id(), head + 1
        event_kind = "shot.text_binding.created" if seq == 1 else "shot.text_binding.rebound"
        payload = {"binding_id": binding_id, "project_id": project_id, "shot_id": shot_id, "kind": kind, "slot": slot,
                   "media_id": value["media_id"], "content_hash": value["content_hash"], "byte_size": value["byte_size"],
                   "mime_type": value["mime_type"], "publication_id": publication_id,
                   "state": "absent" if clearing else "present"}
        event_hash = hashlib.sha256(canonical_json({"event_id": event_id, "binding_id": binding_id, "seq": seq,
                                                    "kind": event_kind, "payload": payload,
                                                    "previous_hash": previous_hash}).encode()).hexdigest()
        self.conn.execute("INSERT INTO shot_text_binding_events(event_id, binding_id, project_id, seq, kind, payload_json, previous_hash, event_hash, created_at) "
                          "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                          (event_id, binding_id, project_id, seq, event_kind, canonical_json(payload), previous_hash, event_hash, timestamp))
        self.conn.execute("UPDATE shot_text_bindings SET media_digest=?, head_seq=?, updated_at=? WHERE id=?",
                          (object_digest, seq, timestamp, binding_id))

    def _persist_closure(self, document):
        project_id, timestamp = document["project_id"], now()
        for image in document["internal_timeline_revisions"]:
            self.conn.execute("INSERT OR IGNORE INTO internal_timeline_revisions(id, project_id, timeline_id, payload_json, content_digest, created_at) "
                              "VALUES (?, ?, ?, ?, ?, ?)", (image["revision_id"], project_id, image["timeline_id"], canonical_json(image["payload"]), image["content_digest"], timestamp))
        for image in document["shot_revisions"]:
            existing = self.conn.execute("SELECT 1 FROM shot_revisions WHERE id=?", (image["revision_id"],)).fetchone()
            if existing:
                continue
            payload, shot_id = image["payload"], image["shot_id"]
            self.conn.execute("INSERT INTO project_shots(id, project_id, name, metadata_json, version, created_at, updated_at, archived_at) "
                              "VALUES (?, ?, ?, ?, 1, ?, ?, ?) ON CONFLICT(id) DO UPDATE SET name=excluded.name, metadata_json=excluded.metadata_json, "
                              "version=project_shots.version+1, updated_at=excluded.updated_at, archived_at=excluded.archived_at",
                              (shot_id, project_id, payload.get("name") or shot_id, canonical_json(payload.get("metadata", {})), timestamp, timestamp,
                               timestamp if payload.get("archived", False) else None))
            self.conn.execute("DELETE FROM shot_items WHERE shot_id=?", (shot_id,))
            for ordinal, item in enumerate(payload.get("items", [])):
                self.conn.execute("INSERT INTO shot_items(id, shot_id, media_id, sort_key, source_frame, metadata_json, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
                                  (item.get("item_id", item.get("id")), shot_id, item["media_id"].removeprefix("sha256:"), f"{ordinal:08d}",
                                   item.get("source_frame"), canonical_json(item.get("metadata", {})), timestamp))
            self.conn.execute("INSERT INTO shot_revisions(id, project_id, shot_id, internal_timeline_revision_id, payload_json, content_digest, created_at) "
                              "VALUES (?, ?, ?, ?, ?, ?, ?)", (image["revision_id"], project_id, shot_id, image["internal_timeline_revision_id"],
                                                             canonical_json(payload), image["content_digest"], timestamp))
            self.conn.execute("INSERT INTO shot_revision_heads(shot_id, project_id, revision_id, updated_at) VALUES (?, ?, ?, ?) "
                              "ON CONFLICT(shot_id) DO UPDATE SET revision_id=excluded.revision_id, updated_at=excluded.updated_at",
                              (shot_id, project_id, image["revision_id"], timestamp))
        parent, manifest = document["parent_revision"], document["dependency_manifest"]
        existing = self.conn.execute("SELECT 1 FROM parent_composition_revisions WHERE id=?", (parent["revision_id"],)).fetchone()
        if existing is None:
            self.conn.execute("INSERT INTO parent_composition_revisions(id, project_id, timeline_id, payload_json, content_digest, commit_manifest_json, created_at) "
                              "VALUES (?, ?, ?, ?, ?, ?, ?)", (parent["revision_id"], project_id, document["timeline_id"], canonical_json(parent["payload"]),
                                                             parent["content_digest"], canonical_json(manifest), timestamp))
            for ordinal, occurrence in enumerate(parent["payload"]["occurrences"]):
                self.conn.execute("INSERT INTO composition_revision_occurrences(parent_revision_id, occurrence_id, ordinal, project_id, shot_id, shot_revision_id, "
                                  "placement_json, source_offset_json, duration_ms, speed_json, track, transform_json, gain, muted, provenance_json) "
                                  "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                  (parent["revision_id"], occurrence["occurrence_id"], ordinal, project_id, occurrence["shot_id"], occurrence["shot_revision_id"],
                                   canonical_json(occurrence["placement"]), canonical_json(occurrence.get("source_offset", 0)), occurrence["duration_ms"],
                                   canonical_json(occurrence.get("speed", 1)), occurrence["track"], canonical_json(occurrence.get("transform", {})), occurrence.get("gain", 1),
                                   int(occurrence.get("muted", occurrence.get("mute", False))), canonical_json(occurrence.get("provenance", {}))))
            dependencies = [("shot_revision", p["revision_id"], p["content_digest"]) for p in manifest["shots"]]
            dependencies += [("internal_timeline_revision", p["revision_id"], p["content_digest"]) for p in manifest["internal_timelines"]]
            dependencies += [("media", p["media_id"], p["content_digest"]) for p in manifest["media"]]
            for ordinal, (kind, identity, content_digest) in enumerate(dependencies):
                self.conn.execute("INSERT INTO composition_revision_dependencies VALUES (?, ?, ?, ?, ?)",
                                  (parent["revision_id"], kind, identity, content_digest, ordinal))
        else:
            self.conn.execute("UPDATE parent_composition_revisions SET commit_manifest_json=? WHERE id=? AND commit_manifest_json IS NULL",
                              (canonical_json(manifest), parent["revision_id"]))

    def _publish(self, context, data, previous, records, semantic_events):
        request = context["request"]
        project_id, timeline_id = request["project_id"], request["timeline_id"]
        revision_id = data["canonical_document"]["parent_revision"]["revision_id"]
        event_ids = []
        for event in semantic_events:
            event_ids.append(self.store._append_timeline_event(timeline_id, event["kind"],
                {"project_id": project_id, "timeline_id": timeline_id, "publisher": context["publisher"], **event}))
        event_ids.append(self.store._append_timeline_event(timeline_id, "timeline.commit.accepted",
            {"project_id": project_id, "timeline_id": timeline_id, "previous": previous, "revision_id": revision_id,
             "publisher": context["publisher"], "intent": "recorded", "records_digest": digest(records)}))
        seq = self.conn.execute("SELECT COUNT(*) FROM timeline_events WHERE timeline_id=?", (timeline_id,)).fetchone()[0]
        publication_id = self.store._record_command_receipt("timeline.commit", scope(context), context["idempotency_key"], context["request_hash"],
            data, project_id=project_id, event_ids=event_ids, primary_stream_id=timeline_id, resulting_stream_seq=seq)
        ledger = self.conn.execute("SELECT * FROM command_idempotency WHERE txn_id=?", (publication_id,)).fetchone()
        self.conn.execute("INSERT INTO timeline_commit_history VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (publication_id, project_id, timeline_id, revision_id, previous["publication_id"] if previous else None,
             previous["revision_id"], "recorded", canonical_json(records),
             canonical_json({k: request[k] for k in _METADATA if k in request}), data.get("provider_version"), data.get("compiler_version"),
             context["publisher"], ledger["first_project_seq"]))
        changed = self.conn.execute("UPDATE parent_composition_heads SET revision_id=?, publication_id=?, updated_at=? "
            "WHERE project_id=? AND timeline_id=? AND revision_id=? AND publication_id=?", (revision_id, publication_id, now(), project_id, timeline_id,
            previous["revision_id"], previous["publication_id"])).rowcount
        if changed != 1:
            raise ProtocolError("head changed inside acceptance transaction")
        self.conn.execute("UPDATE timelines SET version=version+1 WHERE id=? AND project_id=?", (timeline_id, project_id))
        return self._envelope(ledger, project_id)

    def _install_entries(self, project_id, timeline_id, plan):
        for entry in plan["entries"]:
            previous = entry["previous"]
            self.conn.execute("INSERT INTO timeline_commit_history VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (entry["publication_id"], project_id, timeline_id, entry["revision_id"],
                 previous["publication_id"] if previous else None, previous["revision_id"] if previous else None,
                 entry["intent"], None, canonical_json({k: entry[k] for k in _METADATA if k in entry}),
                 entry["provider_version"], entry["compiler_version"], entry["publisher"], entry["receipt"]["project_seq"][0]))
        changed = self.conn.execute("UPDATE parent_composition_heads SET publication_id=? WHERE project_id=? AND timeline_id=? "
                                   "AND revision_id=? AND publication_id IS NULL", (plan["head"]["publication_id"], project_id,
                                   timeline_id, plan["head"]["revision_id"])).rowcount
        if changed != 1:
            reject("stale_head")

    def install_verified_baseline(self, project_id, timeline_id, *, authorize):
        from .cas import ContentAddressedStore
        from .timeline_commit_baseline import baseline_install_plan, verify_baseline

        with self.store._mutex, self.store._transaction():
            authorize()
            self._membership(project_id, timeline_id)
            current = self.conn.execute("SELECT revision_id, publication_id FROM parent_composition_heads WHERE project_id=? AND timeline_id=?",
                                        (project_id, timeline_id)).fetchone()
            if current is not None and current["publication_id"]:
                return self.head(project_id, timeline_id)
            read_object = ContentAddressedStore(self.store.cas_root).read
            facts = verify_baseline(self.conn, project_id, timeline_id, read_object=read_object)
            plan = baseline_install_plan(self.conn, facts, read_object=read_object)
            document = facts["canonical_document"]
            self._validate_closure(document)
            for entry in plan["entries"]:
                event = self.conn.execute("SELECT payload_json FROM timeline_events WHERE id=? AND timeline_id=?",
                                          (entry["receipt"]["event_ids"][0], timeline_id)).fetchone()
                manifest = {**json.loads(event[0])["dependency_manifest"], "documents": []}
                self.conn.execute("UPDATE parent_composition_revisions SET commit_manifest_json=? WHERE id=? AND commit_manifest_json IS NULL",
                                  (canonical_json(manifest), entry["revision_id"]))
            self._install_entries(project_id, timeline_id, plan)
            return detached(plan["head"])

    def adopt_empty_shell(self, project_id, timeline_id, *, authorize):
        """Bootstrap an empty headless shell or adopt its verified publication.

        A shell without a parent must have no retained parent or publication.
        Returns the publication event installed by the existing bootstrap path.
        """
        from .cas import ContentAddressedStore
        from .timeline_commit_baseline import bootstrap_install_plan

        with self.store._mutex, self.store._transaction():
            authorize()
            self._membership(project_id, timeline_id)
            current = self.conn.execute("SELECT project_id, revision_id, publication_id FROM parent_composition_heads WHERE timeline_id=?",
                                        (timeline_id,)).fetchone()
            if current is not None and (current["project_id"] != project_id or current["publication_id"] is not None):
                reject("history_unavailable")
            if not timeline_scope_is_empty(self.conn, timeline_id, project_id=project_id):
                reject("history_unavailable")
            if current is None or current["revision_id"] is None:
                if self.conn.execute("SELECT 1 FROM parent_composition_revisions WHERE timeline_id=? LIMIT 1", (timeline_id,)).fetchone():
                    reject("history_unavailable")
                # Normal create retains its empty legacy projection as well.
                empty_legacy = {"shots": [], "references": []}
                for row in self.conn.execute("SELECT * FROM internal_timeline_revisions WHERE timeline_id=?", (timeline_id,)):
                    if row["project_id"] != project_id or row["payload_json"] != canonical_json(empty_legacy) or row["content_digest"] != digest(empty_legacy):
                        reject("history_unavailable")
                if self.conn.execute("SELECT 1 FROM command_idempotency WHERE command_kind='parent_composition.publish' AND aggregate_id=? LIMIT 1",
                                     (timeline_id,)).fetchone() or self.conn.execute(
                        "SELECT 1 FROM timeline_events WHERE timeline_id=? AND kind='parent.composition.published' LIMIT 1", (timeline_id,)).fetchone():
                    reject("history_unavailable")
                head = self.bootstrap(project_id, timeline_id, authorize=authorize)
                entry = self.history_entry(project_id, timeline_id, head["publication_id"])
                return entry["receipt"]["event_ids"][0]
            plan = bootstrap_install_plan(self.conn, project_id, timeline_id,
                                          read_object=ContentAddressedStore(self.store.cas_root).read)
            self._install_entries(project_id, timeline_id, plan)
            return plan["entries"][0]["receipt"]["event_ids"][0]

    def bootstrap(self, project_id, timeline_id, *, authorize):
        from .cas import ContentAddressedStore
        from .timeline_commit_baseline import bootstrap_install_plan, empty_bootstrap_document

        # May compose with main's atomic create transaction. This is the sole
        # exception to accept's outer-transaction requirement.
        with self.store._mutex, self.store._transaction():
            authorize()
            self._membership(project_id, timeline_id)
            current = self.conn.execute("SELECT revision_id, publication_id FROM parent_composition_heads WHERE project_id=? AND timeline_id=?",
                                        (project_id, timeline_id)).fetchone()
            if current is not None and current["revision_id"]:
                if current["publication_id"]:
                    return self.head(project_id, timeline_id)
                reject("history_unavailable")
            document = empty_bootstrap_document(project_id, timeline_id, "bootstrap-" + new_id())
            self._validate_closure(document)
            self._persist_closure(document)
            parent, timestamp = document["parent_revision"], now()
            manifest = {k: v for k, v in document["dependency_manifest"].items() if k != "documents"}
            self.conn.execute("INSERT INTO parent_composition_heads(timeline_id, project_id, revision_id, updated_at) VALUES (?, ?, ?, ?) "
                              "ON CONFLICT(timeline_id) DO UPDATE SET revision_id=excluded.revision_id, updated_at=excluded.updated_at",
                              (timeline_id, project_id, parent["revision_id"], timestamp))
            event = self.store._append_timeline_event(timeline_id, "parent.composition.published",
                {"project_id": project_id, "timeline_id": timeline_id, "old_head": None, "new_head": parent["revision_id"],
                 "content_digest": parent["content_digest"], "dependency_manifest": manifest})
            result = {"project_id": project_id, "timeline_id": timeline_id, "revision_id": parent["revision_id"],
                      "parent_revision_id": parent["revision_id"], "content_digest": parent["content_digest"], "payload": parent["payload"],
                      "old_head": None, "new_head": parent["revision_id"], "dependency_manifest": manifest,
                      "content_digests": {"parent": parent["content_digest"]}, "event_id": event, "created_at": timestamp}
            event_seq = self.conn.execute("SELECT COUNT(*) FROM timeline_events WHERE timeline_id=?", (timeline_id,)).fetchone()[0]
            self.store._record_command_receipt("parent_composition.publish", timeline_id, "bootstrap:" + timeline_id,
                digest({"project_id": project_id, "timeline_id": timeline_id, "bootstrap": True})[7:], result,
                project_id=project_id, event_ids=[event], primary_stream_id=timeline_id, resulting_stream_seq=event_seq, created_at=timestamp)
            plan = bootstrap_install_plan(self.conn, project_id, timeline_id,
                                          read_object=ContentAddressedStore(self.store.cas_root).read)
            self._install_entries(project_id, timeline_id, plan)
            return detached(plan["head"])
