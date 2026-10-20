"""Renderer-free persistence for the frozen timeline commit contract.

Callers supply schema/event validation and request-private input captures. Only
this module owns the acceptance transaction; provider execution belongs outside
RealmStore's mutex.
"""
from __future__ import annotations

import base64
import copy
import hashlib
import json
import math
import re

from .errors import ConflictError, ProtocolError, ValidationError
from .idempotency import command_result
from .util import canonical_json, new_id, now

_METADATA = ("source", "label", "rationale", "group_id")
_DIGEST = re.compile(r"sha256:[0-9a-f]{64}\Z")


def detached(value):
    def finite(item):
        if item is None or type(item) in (str, int, bool):
            return
        if type(item) is float and math.isfinite(item):
            return
        if isinstance(item, list):
            for child in item:
                finite(child)
            return
        if isinstance(item, dict) and all(isinstance(k, str) for k in item):
            for child in item.values():
                finite(child)
            return
        raise ValidationError("commit values must be finite JSON")
    finite(value)
    return copy.deepcopy(value)


def digest(value):
    return "sha256:" + hashlib.sha256(canonical_json(value).encode()).hexdigest()


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
                     and data["commands"] == [r["command"] for r in records["commands"]]
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
        except (KeyError, TypeError, ValueError, IndexError) as exc:
            raise ProtocolError("accepted commit record is corrupt") from exc

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
            ledger = self.conn.execute("SELECT resulting_stream_seq FROM command_idempotency WHERE txn_id=?", (row["publication_id"],)).fetchone()
            untracked = self.conn.execute("SELECT kind FROM timeline_events WHERE timeline_id=? ORDER BY id LIMIT -1 OFFSET ?",
                                           (timeline_id, ledger[0])).fetchall()
            if any(event[0] != "timeline.renamed" for event in untracked):
                reject("history_unavailable", "timeline has untracked writes")
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
        try:
            self.validate_prepared(prepared)
        except Exception:
            reject("invalid_prepared", "prepared commit does not satisfy the frozen schema", status=422)
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
        if any(key != value for key, value in prepared["id_map"].items()):
            reject("invalid_records", "id_map must contain identity pairs", status=422)
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
        if inputs is not None:
            inputs.validate(prepared)
        elif document["dependency_manifest"]["documents"] or any(r["dependencies"] for r in commands):
            reject("dependency_unavailable", "request-private dependency captures required")
        return {"canonical_document": document, "document_digest": prepared["document_digest"],
                "commands": [r["command"] for r in commands], "id_map": prepared["id_map"],
                "provider_version": prepared["provider_version"], "compiler_version": prepared["compiler_version"]}

    def _check_shot_destinations(self, context, prepared):
        # Check the wire shape before inspecting destinations. This preflight
        # precedes closure validation so foreign occupants get the same refusal.
        try:
            self.validate_prepared(prepared)
        except Exception:
            reject("invalid_prepared", "prepared commit does not satisfy the frozen schema", status=422)
        document = prepared["canonical_document"]
        project, timeline = context["request"]["project_id"], context["request"]["timeline_id"]
        # Exact immutable reuse does not write the mutable shot projection.
        writes = [s for s in document["shot_revisions"] if self.conn.execute(
            "SELECT 1 FROM shot_revisions WHERE id=?", (s["revision_id"],)).fetchone() is None]
        occupied = set()
        for image in writes:
            row = self.conn.execute("SELECT project_id FROM project_shots WHERE id=?", (image["shot_id"],)).fetchone()
            if row is not None:
                if row["project_id"] != project:
                    reject("destination_occupied")
                occupied.add(image["shot_id"])
        if not occupied:
            return
        current = self.revision_closure(project, timeline, prepared["expected_head"]["revision_id"])
        occupied -= {s["shot_id"] for s in current["shot_revisions"]}
        if not occupied:
            return
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
                        if output.get(o, (None,))[0] == shot and any(
                                w["ref"] == "shot:" + shot or w["ref"] == owner or w["ref"].startswith(owner + "/")
                                or (w["ref"] == "timeline" and not w["path"] and w["before"] == {
                                    "state": "present", "value": {k: source[k] for k in ("revision_id", "content_digest")}})
                                for r in entry["records"]["commands"] for w in r["writes"]):
                            occupied.discard(shot)
                    remaining.remove(entry["publication_id"])
                after = edges(self.revision_closure(project, timeline, entry["revision_id"]))
                for o, (shot, _) in after.items():
                    owner = "occurrence:" + o
                    if (shot in occupied and output.get(o, (None,))[0] == shot and o in prior
                            and active.get(o) == prior[o] and prior[o][0] != shot
                            and any(any(b["ref"] == owner for b in r["bindings"])
                                    and any(read["ref"] == owner + "/shot" and read["path"] == ["shot_id"]
                                            and read["state"] == {"state": "present", "value": prior[o][0]}
                                            for read in r["reads"]) for r in entry["records"]["commands"])):
                        occupied.remove(shot)
            cursor = previous
        if occupied or remaining:
            reject("destination_occupied")

    def preview(self, context, prepared, *, authorize, inputs=None):
        context, prepared = detached(context), detached(prepared)
        with self.store._mutex:
            authorize()
            if not context["request"].get("dry_run", False):
                reject("preview_requires_dry_run", status=422)
            self._check_context(context)
            self._check_head(context, prepared["expected_head"])
            self._check_shot_destinations(context, prepared)
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
                self._check_shot_destinations(context, prepared)
                candidate = self._validate(context, prepared, inputs)
                request, previous = context["request"], prepared["expected_head"]
                base = {"revision_id": request["base_revision_id"], "publication_id": request["base_publication_id"]}
                data = {"status": "accepted" if previous == base else "rebased", "base_revision_id": base["revision_id"],
                        "base_publication_id": base["publication_id"], "previous_revision_id": previous["revision_id"],
                        "previous_publication_id": previous["publication_id"],
                        "accepted_revision_id": candidate["canonical_document"]["parent_revision"]["revision_id"],
                        "rebased_onto": None if previous == base else previous, **candidate, "publisher": context["publisher"],
                        **{k: request[k] for k in _METADATA if k in request}}
                self._persist_closure(candidate["canonical_document"])
                result = self._publish(context, data, previous, prepared["records"], prepared["semantic_events"])
                if inputs is not None:
                    inputs.persist(prepared, result["receipt"]["receipt_id"], data["accepted_revision_id"])
                return result

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
