"""Project lifecycle retention over the existing transaction and command ledger.

The inventory is deliberately finite. References are parsed JSON values, never
substring matches. A new resolving storage family must be admitted here before
retention can claim its closure. No object/media files are garbage collected.
"""
import hashlib
import json

from .errors import AuthorizationError, ConflictError, ValidationError
from .util import canonical_json


# Readers: service composition/history/project-document/shot-text endpoints;
# store task_spec, continuation admission, execution bindings and managed output
# readers; timeline_render publication recovery; command_result replay.
REFERENCE_TABLES = (
    "parent_composition_heads", "parent_composition_publications",
    "parent_composition_revisions", "composition_revision_occurrences",
    "composition_revision_dependencies", "shot_revision_heads", "shot_revisions",
    "internal_timeline_revisions", "timeline_revisions", "timeline_shots",
    "timeline_references", "timeline_shot_state", "timeline_reference_state",
    "project_documents", "timeline_render_publications", "tasks", "runs",
    "continuation_admissions", "execution_bindings", "managed_output_associations",
    "shot_text_bindings", "shot_text_binding_events", "project_shots", "shot_items",
    "project_references", "media_references", "reference_links", "generations",
    "generation_variants", "media_relations", "command_idempotency", "recovery_checkpoints",
    "projects", "user_preferences",
    "timeline_events", "events", "timelines",
)
AUDIT_TABLES = {"timeline_events", "events"}
SCALAR_REFERENCES = {"timeline_id", "timeline_ref", "revision_id", "parent_revision_id",
    "shot_id", "shot_revision_id", "internal_timeline_id", "internal_timeline_revision_id",
    "publication_id", "previous_revision_id", "previous_publication_id", "restored_from_revision_id",
    "head_revision_id", "head_publication_id", "expected_head", "base_revision_id", "new_head", "old_head"}
OBJECT_JSON = {("tasks", "spec_json"), ("runs", "spec_json"),
    ("tasks", "execution_request_json"), ("tasks", "authority_binding_json"),
    ("parent_composition_revisions", "payload_json"), ("shot_revisions", "payload_json"),
    ("internal_timeline_revisions", "payload_json"), ("timeline_render_publications", "prepared_json")}


def _validate_reference_shapes(value):
    if isinstance(value, dict):
        for key, item in value.items():
            if key in SCALAR_REFERENCES and item is not None and not isinstance(item, str):
                raise ValueError("malformed identity")
            _validate_reference_shapes(item)
    elif isinstance(value, list):
        for item in value:
            _validate_reference_shapes(item)


def owner(identity):
    if (not isinstance(identity, dict) or identity.get("actor") != "owner"
            or "admin" not in identity.get("scopes", [])
            or not identity.get("_credential_binding")
            or identity.get("connector_assertion") or identity.get("_paired_session")):
        raise AuthorizationError("authenticated local owner required for retention")


def source_provenance(service, project_id, timeline_id, source, identity):
    if (not isinstance(source, dict)
            or set(source) != {"timeline_id", "expected_revision_id", "expected_publication_id"}
            or not all(isinstance(v, str) and v for v in source.values())
            or source["timeline_id"] == timeline_id):
        raise ValidationError("duplicate_source requires distinct source and exact publication")
    if (not isinstance(identity, dict) or not identity.get("_credential_binding")
            or not ({"admin", "projects:write"} & set(identity.get("scopes", [])))):
        raise AuthorizationError("authenticated duplicate creator required")
    row = service.store.conn.execute(
        "SELECT t.project_id, t.archived_at, h.revision_id, h.publication_id FROM timelines t "
        "JOIN parent_composition_heads h ON h.timeline_id=t.id WHERE t.id=?",
        (source["timeline_id"],)).fetchone()
    if (not row or row["project_id"] != project_id or row["archived_at"] is not None
            or row["revision_id"] != source["expected_revision_id"]
            or row["publication_id"] != source["expected_publication_id"]):
        raise ConflictError("duplicate source publication changed or unavailable")
    return {"source": source, "actor": identity["actor"], "project_id": project_id,
            "timeline_id": timeline_id, "realm_id": service.realm["id"]}


def provenance(service, timeline_id):
    row = service.store.conn.execute(
        "SELECT payload_json FROM timeline_events WHERE timeline_id=? "
        "AND kind='timeline.duplicate_created' ORDER BY id LIMIT 1", (timeline_id,)).fetchone()
    if not row:
        return None
    try:
        value = json.loads(row[0])
        if (set(value) != {"source", "actor", "project_id", "timeline_id", "realm_id"}
                or value["timeline_id"] != timeline_id
                or value["realm_id"] != service.realm["id"]):
            return None
        return value
    except (ValueError, TypeError):
        return None


def validate_targets(body):
    if not isinstance(body, dict) or not isinstance(body.get("targets"), list) or not body["targets"]:
        raise ValidationError("targets must be a nonempty exact set")
    targets = body["targets"]
    fields = {"timeline_id", "expected_version", "expected_revision_id", "expected_publication_id"}
    for t in targets:
        if (not isinstance(t, dict) or set(t) != fields
                or not isinstance(t["timeline_id"], str) or not t["timeline_id"]
                or type(t["expected_version"]) is not int or t["expected_version"] < 1
                or any(t[k] is not None and (not isinstance(t[k], str) or not t[k])
                       for k in ("expected_revision_id", "expected_publication_id"))):
            raise ValidationError("invalid exact target state")
    if len({t["timeline_id"] for t in targets}) != len(targets):
        raise ValidationError("duplicate purge target")
    return sorted(targets, key=lambda t: t["timeline_id"])


def _strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, list):
        for item in value:
            yield from _strings(item)
    elif isinstance(value, dict):
        for key, item in value.items():
            yield key
            yield from _strings(item)


def _terminal_result(row):
    if row["command_kind"] == "timeline.commit":
        # COMMIT lookup/revision readers expect this wrapper even when its
        # payload has been reclaimed. Replay returns a valid terminal error,
        # never the previous accepted document or a chance to execute again.
        from .timeline_commit import result_template
        wrapper = json.loads(row["result_json"])
        old = wrapper.get("result", {}) if isinstance(wrapper, dict) else {}
        old = old if isinstance(old, dict) else {}
        result = result_template({"request_id": row["idempotency_key"],
            "base_revision_id": old.get("base_revision_id") or "purged"}, row["request_hash"])
        result["error"] = {"code": "base_not_found", "message": "timeline permanently purged",
                           "hint": "terminal purge receipt", "next_action": "create a new timeline identity"}
        return canonical_json({"result": result, "summary": None, "evidence": None,
                               "previous_publication_id": None})
    return canonical_json({"status": "purged", "terminal": True})


def build_plan(service, project_id, body):
    targets = validate_targets(body)
    conn = service.store.conn
    project = service.store.get_project(project_id)
    project_id = project["id"]
    ids = {t["timeline_id"] for t in targets}
    blockers, states = [], []
    for target in targets:
        tid = target["timeline_id"]
        row = conn.execute("SELECT * FROM timelines WHERE id=? AND project_id=?", (tid, project_id)).fetchone()
        head = conn.execute("SELECT revision_id, publication_id FROM parent_composition_heads WHERE timeline_id=?", (tid,)).fetchone()
        actual = {"expected_version": row["version"] if row else None,
                  "expected_revision_id": head[0] if head else None,
                  "expected_publication_id": head[1] if head else None}
        evidence = provenance(service, tid)
        states.append({"timeline_id": tid, **actual, "archived_at": row["archived_at"] if row else None,
                       "creation_provenance": evidence})
        for bad, code in ((not row or any(target[k] != v for k, v in actual.items()), "state_changed"),
                          (not row or row["archived_at"] is None, "not_archived"),
                          (bool(head and (head[0] or head[1])), "current_publication"),
                          (not evidence or evidence["project_id"] != project_id, "duplicate_provenance_missing")):
            if bad:
                blockers.append({"code": code, "timeline_id": tid})

    rows, keys, refs = {}, {}, {}
    for table in REFERENCE_TABLES:
        columns = conn.execute(f'PRAGMA table_info("{table}")').fetchall()
        keys[table] = [r[1] for r in sorted(columns, key=lambda c: c[5]) if r[5]]
        rows[table] = [dict(r) for r in conn.execute(f'SELECT * FROM "{table}"').fetchall()]
        for n, row in enumerate(rows[table]):
            values = set()
            for field, value in row.items():
                if table == "parent_composition_publications" and field == "provenance_json":
                    # History attribution is presented, never dereferenced;
                    # previous/restored publication columns are checked below.
                    continue
                if (field.endswith("_json") or (table == "user_preferences" and field == "content")) and value is not None:
                    try:
                        parsed = json.loads(value)
                        if (table, field) in OBJECT_JSON and not isinstance(parsed, dict):
                            raise ValueError("reference container must be an object")
                        if table == "command_idempotency" and field == "result_json" and row["command_kind"] == "timeline.commit":
                            if not isinstance(parsed, dict) or not isinstance(parsed.get("result"), dict):
                                raise ValueError("malformed commit replay wrapper")
                        _validate_reference_shapes(parsed)
                    except (ValueError, TypeError):
                        blockers.append({"code": "malformed_reference_data", "table": table,
                                         "row_id": canonical_json([row[key] for key in keys[table]]), "field": field})
                        continue
                    values.update(_strings(parsed))
                elif isinstance(value, str) and field not in {"created_at", "updated_at", "request_hash", "content_digest", "event_hash", "previous_hash"}:
                    values.add(value)
                    if table == "internal_timeline_revisions" and field == "timeline_id" and value.startswith("shot:"):
                        # C011 inspection resolves this exact namespaced
                        # identity through its project-shot owner.
                        values.add(value[len("shot:"):])
            refs[table, n] = values

    parent_ids = {r["id"] for r in rows["parent_composition_revisions"] if r["timeline_id"] in ids}
    publication_ids = {r["publication_id"] for r in rows["parent_composition_publications"] if r["timeline_id"] in ids}
    # Child ownership follows Runtime's internal timeline identity, rather
    # than reachability from a parent (which can legitimately be shared).
    internal_ids = {r["id"] for r in rows["internal_timeline_revisions"] if r["timeline_id"] in ids}
    # Runtime records projection births in the same publication transaction.
    # Reachability alone cannot claim an existing independent project shot.
    # A duplicate's own shot may refer to a shared source internal payload.
    shot_ids = set()
    for event in rows["timeline_events"]:
        if event["timeline_id"] in ids and event["kind"] == "timeline.duplicate_projections_created":
            try:
                value = json.loads(event["payload_json"])
                births = value["project_shot_ids"]
                if (value["project_id"] != project_id or value["timeline_id"] != event["timeline_id"]
                        or not isinstance(births, list) or any(not isinstance(v, str) or not v for v in births)):
                    raise ValueError("invalid projection birth provenance")
                shot_ids.update(births)
            except (ValueError, TypeError, KeyError):
                blockers.append({"code": "malformed_reference_data", "table": "timeline_events", "row_id": str(event["id"])})
    internal_ids |= {r["id"] for r in rows["internal_timeline_revisions"]
                     if r["project_id"] == project_id and r["timeline_id"] in {"shot:" + sid for sid in shot_ids}}
    shot_revision_ids = {r["id"] for r in rows["shot_revisions"] if r["shot_id"] in shot_ids}
    legacy_ids = {r["id"] for r in rows["timeline_shots"] + rows["timeline_references"] if r["timeline_id"] in ids}
    binding_ids = {r["id"] for r in rows["shot_text_bindings"] if r["shot_id"] in shot_ids}

    def owned(table, row):
        if table in {"timelines", "timeline_shot_state", "timeline_reference_state"}:
            return row["id"] in (ids if table == "timelines" else legacy_ids)
        if table in {"parent_composition_heads", "parent_composition_publications", "parent_composition_revisions", "timeline_revisions", "timeline_shots", "timeline_references", "timeline_events"}:
            return row["timeline_id"] in ids
        if table in {"composition_revision_dependencies", "composition_revision_occurrences"}:
            return row["parent_revision_id"] in parent_ids
        if table == "project_documents":
            return row["project_id"] == project_id and row["id"] in {"timeline:" + tid for tid in ids}
        if table == "internal_timeline_revisions":
            return row["id"] in internal_ids
        if table == "shot_revisions":
            return row["id"] in shot_revision_ids
        if table in {"project_shots", "shot_revision_heads", "shot_items", "shot_text_bindings"}:
            return row["id" if table == "project_shots" else "shot_id"] in shot_ids
        if table == "shot_text_binding_events":
            return row["binding_id"] in binding_ids
        return False

    def command_owned(row):
        kind = row["command_kind"]
        if kind == "timeline.purge":
            return False  # The compact permanent project receipt is audit-only.
        if row["primary_stream_id"] in ids | binding_ids:
            return True
        if kind == "timeline.commit":
            try:
                aggregate = json.loads(row["aggregate_id"])
                return isinstance(aggregate, list) and len(aggregate) == 2 and aggregate[0] == project_id and aggregate[1] in ids
            except (ValueError, TypeError):
                return False
        if kind != "timeline.create" and kind.startswith(("timeline.", "timeline_document.", "parent_composition.")) and row["aggregate_id"] in ids:
            return True
        if kind.startswith(("shot.", "shot_text_binding.", "shot.text_binding.")) and row["aggregate_id"] in shot_ids | binding_ids:
            return True
        try:
            value = json.loads(row["result_json"])
            return isinstance(value, dict) and (value.get("timeline_id") in ids
                or value.get("shot_id") in shot_ids or value.get("binding_id") in binding_ids)
        except (ValueError, TypeError):
            return False

    # Shared children survive. Resolve to a fixed point because retaining a
    # shot also retains its immutable internal payload and text history.
    while True:
        terminal = {n for n, r in enumerate(rows["command_idempotency"]) if command_owned(r)}
        removed = {(t, n) for t in rows for n, r in enumerate(rows[t]) if owned(t, r)}
        retained_refs = set().union(*(v for (t, n), v in refs.items()
                                     if (t, n) not in removed and t not in AUDIT_TABLES
                                     and not (t == "command_idempotency" and (n in terminal or rows[t][n]["command_kind"] == "timeline.purge"))))
        shared_shots = shot_ids & retained_refs
        # Text history and item IDs can be pinned independently of the shot.
        # Retain their entire owner rather than deleting a shared projection.
        shared_bindings = {r["id"] for r in rows["shot_text_bindings"]
                           if r["id"] in retained_refs or r["event_stream_id"] in retained_refs}
        shared_bindings |= {r["binding_id"] for r in rows["shot_text_binding_events"]
                            if r["event_id"] in retained_refs}
        shared_shots |= {r["shot_id"] for r in rows["shot_text_bindings"] if r["id"] in shared_bindings}
        shared_shots |= {r["shot_id"] for r in rows["shot_items"] if r["id"] in retained_refs}
        shared_shots &= shot_ids
        shared_revisions = shot_revision_ids & retained_refs
        shared_shots |= {r["shot_id"] for r in rows["shot_revisions"] if r["id"] in shared_revisions}
        shared_internal = internal_ids & retained_refs
        if not shared_shots and not shared_internal:
            break
        shot_ids -= shared_shots
        shot_revision_ids = {r["id"] for r in rows["shot_revisions"] if r["shot_id"] in shot_ids}
        internal_ids -= shared_internal
        binding_ids = {r["id"] for r in rows["shot_text_bindings"] if r["shot_id"] in shot_ids}

    # The render task reader resolves legacy timeline_ref by exact ID or the
    # saved timeline document slug (store._bind_render_timeline_request).
    slugs = set()
    for row in rows["project_documents"]:
        if row["project_id"] == project_id and row["id"] in {"timeline:" + tid for tid in ids}:
            try:
                content = json.loads(row["content_json"])
                if isinstance(content, dict) and isinstance(content.get("slug"), str):
                    slugs.add(content["slug"])
            except (ValueError, TypeError):
                pass  # Already refused above as malformed reference data.
    # Occurrence IDs are scoped by parent_revision_id, not globally unique;
    # the parent pin already protects every resolving occurrence reference.
    protected = ids | parent_ids | publication_ids | legacy_ids | {"timeline:" + tid for tid in ids} | slugs
    for (table, n), values in refs.items():
        if ((table, n) in removed or table in AUDIT_TABLES
                or (table == "command_idempotency" and (n in terminal or rows[table][n]["command_kind"] == "timeline.purge"))):
            continue
        hits = sorted(values & protected)
        if hits:
            blockers.append({"code": "external_reference", "table": table,
                             "row_id": canonical_json([rows[table][n][key] for key in keys[table]]), "identities": hits})
    counts = {t: sum(1 for table, _ in removed if table == t) for t in rows}
    counts = {t: count for t, count in counts.items() if count}
    if terminal:
        counts["command_idempotency_compacted"] = len(terminal)
    payload_bytes = sum(len(v.encode("utf-8")) for t, n in removed
                        for k, v in rows[t][n].items() if k.endswith("_json") and isinstance(v, str))
    payload_bytes += sum(max(0, len(rows["command_idempotency"][n]["result_json"].encode())
                             - len(_terminal_result(rows["command_idempotency"][n]).encode())) for n in terminal)
    evidence = {"targets": states, "blockers": blockers,
                "deleted_rows": [(t, rows[t][n]) for t, n in sorted(removed)],
                "terminal_records": [rows["command_idempotency"][n] for n in sorted(terminal)]}
    result = {"project_id": project_id, "realm_id": service.realm["id"], "targets": states,
              "plan_digest": "sha256:" + hashlib.sha256(canonical_json(evidence).encode()).hexdigest(),
              "eligible": not blockers, "blockers": blockers, "deletion_counts": counts,
              "reclaimable_payload_bytes": payload_bytes}
    return result, (rows, keys, removed, terminal)


def delete_plan(service, snapshot):
    rows, keys, removed, terminal = snapshot
    conn = service.store.conn
    # Existing ledger keys/request hashes remain to prevent resurrection;
    # full publication/create payloads do not survive as replay snapshots.
    for n in terminal:
        row = rows["command_idempotency"][n]
        conn.execute("UPDATE command_idempotency SET result_json=? WHERE command_kind=? AND aggregate_id=? AND idempotency_key=?",
                     (_terminal_result(row), row["command_kind"], row["aggregate_id"], row["idempotency_key"]))
    order = ("composition_revision_dependencies", "composition_revision_occurrences", "parent_composition_heads",
             "parent_composition_publications", "parent_composition_revisions", "shot_text_binding_events",
             "shot_text_bindings", "shot_revision_heads", "shot_revisions", "shot_items", "project_shots",
             "internal_timeline_revisions", "timeline_shot_state", "timeline_reference_state", "timeline_shots",
             "timeline_references", "timeline_revisions", "project_documents", "timeline_events", "timelines")
    for table in order:
        for t, n in sorted(removed):
            if t == table:
                row = rows[t][n]
                where = " AND ".join(f'"{key}" IS ?' for key in keys[t])
                conn.execute(f'DELETE FROM "{t}" WHERE {where}', tuple(row[key] for key in keys[t]))
    if conn.execute("PRAGMA foreign_key_check").fetchone():
        raise ConflictError("retention integrity check failed")
