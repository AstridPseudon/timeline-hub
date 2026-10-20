"""Renderer-independent semantics for Runtime's fixed timeline commit port.

Runtime owns authority, persistence and completion reconciliation. This provider
only converts exact immutable closures and executes the recorded Agent plan.
"""
from __future__ import annotations

import copy
import hashlib
import json
import re
from collections.abc import Mapping

from astrid.core.timeline.authoring_bundle import (
    AuthoringBundleError,
    _collect_media,
    compile_authoring_candidate,
    open_authoring_bundle,
)

PROVIDER_VERSION = "astrid-v1"
COMPILER_VERSION = "authoring-bundle-1"
_DIGEST = re.compile(r"sha256:[0-9a-f]{64}\Z")


def _json(value):
    try:
        return json.dumps(value, sort_keys=True, separators=(",", ":"),
                          ensure_ascii=False, allow_nan=False)
    except (TypeError, ValueError) as exc:
        raise AuthoringBundleError("canonical document must be finite JSON") from exc


def _digest(value):
    return "sha256:" + hashlib.sha256(_json(value).encode("utf-8")).hexdigest()


def _require(condition, message):
    if not condition:
        raise AuthoringBundleError(message)


def _id(value):
    return isinstance(value, str) and bool(value.strip())


def _document_pin(pin):
    _require(isinstance(pin, Mapping) and set(pin) == {
        "document_id", "version", "content_digest"}, "invalid document pin")
    _require(_id(pin["document_id"]) and type(pin["version"]) is int
             and pin["version"] > 0 and isinstance(pin["content_digest"], str)
             and _DIGEST.fullmatch(pin["content_digest"]), "invalid document pin")
    return dict(pin)


def _manifest(shots, internals, media, documents):
    return {
        "shots": sorted(({
            key: row[key] for key in ("shot_id", "revision_id",
                                     "internal_timeline_revision_id", "content_digest")
        } for row in shots), key=lambda row: (row["shot_id"], row["revision_id"])),
        "internal_timelines": sorted(({
            key: row[key] for key in ("timeline_id", "revision_id", "content_digest")
        } for row in internals), key=lambda row: (row["timeline_id"], row["revision_id"])),
        "media": sorted(media, key=lambda row: row["media_id"]),
        "documents": sorted(documents, key=lambda row: (
            row["document_id"], row["version"], row["content_digest"])),
    }


def _verify_document(document):
    _require(isinstance(document, Mapping) and set(document) == {
        "schema_version", "project_id", "timeline_id", "parent_revision", "shot_revisions",
        "internal_timeline_revisions", "dependency_manifest"}, "invalid canonical document")
    _require(type(document["schema_version"]) is int and document["schema_version"] == 1,
             "unsupported canonical document schema")
    _require(_id(document["project_id"]) and _id(document["timeline_id"]),
             "canonical project and timeline IDs are required")
    _json(document)
    parent = document["parent_revision"]
    shots, internals = document["shot_revisions"], document["internal_timeline_revisions"]
    _require(isinstance(shots, list) and isinstance(internals, list), "invalid closure images")
    for row in [parent, *shots, *internals]:
        _require(isinstance(row, Mapping) and _id(row.get("revision_id"))
                 and isinstance(row.get("payload"), Mapping), "invalid revision image")
        _require(row.get("content_digest") == _digest(row["payload"]),
                 "immutable payload digest mismatch")
        _require("project_id" not in row, "project scope belongs on the canonical document")
    _require(set(parent) == {"revision_id", "content_digest", "payload"}, "invalid parent image")
    payload = parent["payload"]
    config = payload.get("config", {})
    _require(isinstance(config, Mapping), "invalid parent config")
    if payload.get("clips") and config.get("clips"):
        _require(payload["clips"] == config["clips"], "parent clips and config.clips disagree")
    for row in shots:
        _require(set(row) == {"shot_id", "revision_id", "internal_timeline_revision_id",
                              "content_digest", "payload"} and _id(row["shot_id"]),
                 "invalid shot image")
    for row in internals:
        _require(set(row) == {"timeline_id", "revision_id", "content_digest", "payload"}
                 and _id(row["timeline_id"]), "invalid internal image")
    shot_index = {(row["shot_id"], row["revision_id"]): row for row in shots}
    internal_index = {row["revision_id"]: row for row in internals}
    _require(len(shot_index) == len(shots) and len(internal_index) == len(internals)
             and len({row["revision_id"] for row in shots}) == len(shots),
             "duplicate closure identity")
    occurrences = parent["payload"].get("occurrences")
    _require(isinstance(occurrences, list), "parent occurrences are required")
    used_shots = set()
    for row in occurrences:
        _require(isinstance(row, Mapping), "invalid occurrence")
        key = (row.get("shot_id"), row.get("shot_revision_id"))
        _require(key in shot_index, "missing exact occurrence shot revision")
        used_shots.add(key)
    _require(used_shots == set(shot_index), "shot closure is incomplete or contains orphans")
    used_internals = set()
    for row in shots:
        revision = row["internal_timeline_revision_id"]
        _require(row["payload"].get("internal_timeline_revision_id", revision) == revision,
                 "shot internal revision link mismatch")
        _require(revision in internal_index, "missing exact internal revision")
        used_internals.add(revision)
    _require(used_internals == set(internal_index), "internal closure contains orphans")
    manifest = document["dependency_manifest"]
    _require(isinstance(manifest, Mapping) and set(manifest) == {
        "shots", "internal_timelines", "media", "documents"}, "invalid dependency manifest")
    documents = [_document_pin(pin) for pin in manifest["documents"]]
    _require(len({_json(pin) for pin in documents}) == len(documents), "duplicate document pin")
    media = manifest["media"]
    _require(isinstance(media, list), "invalid media manifest")
    for row in media:
        _require(isinstance(row, Mapping) and set(row) == {"media_id", "content_digest"}
                 and isinstance(row["media_id"], str) and _DIGEST.fullmatch(row["media_id"])
                 and row["content_digest"] == row["media_id"], "invalid immutable media pin")
    _require(len({row["media_id"] for row in media}) == len(media), "duplicate media pin")
    required_media = set().union(*(_collect_media(row["payload"])
                                   for row in [parent, *shots, *internals]))
    _require(required_media <= {row["media_id"] for row in media}, "missing media dependency")
    _require(manifest == _manifest(shots, internals, media, documents),
             "dependency manifest does not match the immutable closure")
    _require(shots == sorted(shots, key=lambda row: (row["shot_id"], row["revision_id"]))
             and internals == sorted(internals, key=lambda row: (
                 row["timeline_id"], row["revision_id"])), "closure images must be sorted")


def bundle_from_document(document):
    """Open a complete immutable Runtime document without a Runtime dependency."""
    document = copy.deepcopy(document)
    _verify_document(document)
    project, timeline = document["project_id"], document["timeline_id"]
    bundle = open_authoring_bundle(
        {**document["parent_revision"], "project_id": project, "timeline_id": timeline},
        shot_revisions=[{**row, "project_id": project} for row in document["shot_revisions"]],
        internal_timeline_revisions=[{**row, "project_id": project}
                                     for row in document["internal_timeline_revisions"]],
    )
    bundle["source_mapping"]["_runtime_document"] = document
    return bundle


def _inverse_media_removals(records, bundle):
    """Only accepted edges can prove that a retained pin was introduced by writes."""
    from ._collections import AcceptedRecords
    from ._command_state import CommandError, State, equal

    if not records:
        return set()
    if not isinstance(records, AcceptedRecords):
        raise CommandError('media inverse needs accepted boundaries', kind='history_unavailable')
    if not equal(list(records), [record for entry in records.entries
                                for record in entry['records']['commands']]):
        raise CommandError('media inverse records differ from accepted history', kind='history_unavailable')
    removed = set()
    for entry in reversed(records.entries):
        before, after = records.load_boundary(entry)
        images = [value['source_mapping']['_runtime_document'] for value in (before, after)]
        for image, pin in zip(images, (entry['previous'], entry)):
            _verify_document(image)
            _require((image['project_id'], image['timeline_id']) ==
                     (bundle['project_id'], bundle['timeline_id'])
                     and image['parent_revision']['revision_id'] == pin['revision_id'],
                     'inverse media boundary mismatch')
        commands = entry['records']['commands']
        # Whole-closure restoration already selects its exact source manifest.
        if any(write['ref'] == 'timeline' for record in commands for write in record['writes']):
            continue
        prior_media, accepted_media = ({row['media_id'] for row in image['dependency_manifest']['media']}
                                       for image in images)
        introduced = accepted_media - prior_media
        if prior_media - accepted_media and any(record['command']['op'] != 'timeline.inverse'
                                                for record in commands):
            raise CommandError('unproven media removal boundary', kind='history_unavailable')
        removed.difference_update(prior_media - accepted_media)
        if not introduced:
            continue
        state = State(copy.deepcopy(before))
        for record in commands:
            for write in [*record['writes'], *record['derived_writes']]:
                if not state.matches(write['ref'], write['path'], write['before']):
                    raise CommandError('media boundary differs from accepted writes', kind='history_unavailable')
                state.set(write['ref'], write['path'], write['after'])
        replayed = document_from_bundle(state.bundle, source_bundles=(after,))
        if (not equal(replayed['parent_revision']['payload'], images[1]['parent_revision']['payload'])
                or any(not equal(replayed[key], images[1][key]) for key in (
                    'shot_revisions', 'internal_timeline_revisions'))
                or not equal(replayed['dependency_manifest']['documents'],
                             images[1]['dependency_manifest']['documents'])
                or not introduced <= _collect_media([write['after'] for record in commands
                                                     for write in record['writes']])):
            raise CommandError('unproven media boundary scope', kind='history_unavailable')
        removed.update(introduced)
    return removed


def document_from_bundle(bundle, *, document_pins=None, source_bundles=(), inverse_records=()):
    """Compile exact inputs; inverse pin removal requires provider-verified records.

    Historical source images alone never authorize dropping retained media.
    """
    from ._command_state import equal

    source = bundle["source_mapping"]["_runtime_document"]
    publication = compile_authoring_candidate(bundle).publication
    shot_index = {row["revision_id"]: copy.deepcopy(row) for row in source["shot_revisions"]}
    internal_index = {row["revision_id"]: copy.deepcopy(row)
                      for row in source["internal_timeline_revisions"]}
    shot_index.update({row["revision_id"]: copy.deepcopy(row)
                       for row in publication["shot_revisions"]})
    internal_index.update({row["revision_id"]: copy.deepcopy(row)
                           for row in publication["internal_timeline_revisions"]})
    # Only authenticated publication boundaries may supply earlier immutable
    # images. Reuse them after exact authored-content comparison, never restore
    # a parent snapshot or replace a sibling's currently accepted pins.
    for historical in source_bundles:
        document = historical['source_mapping']['_runtime_document']
        _verify_document(document)
        _require((document['project_id'], document['timeline_id']) ==
                 (bundle['project_id'], bundle['timeline_id']), 'foreign inverse source')
        shot_index.update({row['revision_id']: copy.deepcopy(row) for row in document['shot_revisions']})
        internal_index.update({row['revision_id']: copy.deepcopy(row)
                               for row in document['internal_timeline_revisions']})
    parent = copy.deepcopy(publication["parent_composition"])
    # Opening shared occurrences gives them independent editing identities. A
    # parent-only edit must still reuse their ORIGINAL immutable shot images.
    for occurrence in parent["occurrences"]:
        identity = occurrence["shot_id"]
        shot = bundle["shots"][identity]
        origin = bundle["source_mapping"]["shots"].get(identity)
        if (origin is not None and shot["payload"] == shot["base_payload"]
                and shot["internal_timeline"] == shot["base_internal_timeline"]
                and origin.get("revision_id") in shot_index):
            occurrence["shot_id"] = origin["shot_id"]
            occurrence["shot_revision_id"] = origin["revision_id"]
            continue
        for historical in source_bundles:
            prior = next((row for row in historical['placements']
                          if row['occurrence_id'] == occurrence['occurrence_id']), None)
            if prior is None or prior['shot_id'] != identity:
                continue
            old = historical['shots'][identity]
            payload, old_payload = copy.deepcopy(shot['payload']), copy.deepcopy(old['payload'])
            payload.pop('internal_timeline_revision_id', None)
            old_payload.pop('internal_timeline_revision_id', None)
            if not equal(payload, old_payload) or not equal(shot['internal_timeline'], old['internal_timeline']):
                continue
            origin = historical['source_mapping']['shots'][identity]
            occurrence['shot_id'] = origin['shot_id']
            occurrence['shot_revision_id'] = origin['revision_id']
            break
    shot_ids = {row["shot_revision_id"] for row in parent["occurrences"]}
    shots = sorted((shot_index[key] for key in shot_ids),
                   key=lambda row: (row["shot_id"], row["revision_id"]))
    internal_ids = {row["internal_timeline_revision_id"] for row in shots}
    internals = sorted((internal_index[key] for key in internal_ids),
                       key=lambda row: (row["timeline_id"], row["revision_id"]))
    documents = (source["dependency_manifest"]["documents"]
                 if document_pins is None else document_pins)
    if document_pins is None:
        documents = copy.deepcopy(documents)
        for capture in bundle['source_mapping'].get('pinned_documents', []):
            if capture['pin'] not in documents:
                documents.append(copy.deepcopy(capture['pin']))
    # Retained inputs may include media consumed through a transcript or other
    # immutable binding rather than a selected clip. Keep those existing pins.
    media = {row["media_id"]: row for row in source["dependency_manifest"]["media"]}
    media.update({row["media_id"]: row for row in publication["dependency_manifest"]["media"]})
    removals = _inverse_media_removals(inverse_records, bundle)
    if removals:
        from ._command_state import CommandError

        required = _collect_media([parent, *[row['payload'] for row in shots + internals]])
        captures = bundle['source_mapping'].get('pinned_documents', [])
        if any(not any(capture['pin'] == pin for capture in captures) for pin in documents):
            raise CommandError('media inverse source scope is unavailable', kind='history_unavailable')
        required.update(_collect_media([capture['document']['content'] for capture in captures
                                       if capture['pin'] in documents]))
        if required & removals:
            raise CommandError('introduced media has surviving dependents', kind='surviving_dependents')
        for identity in removals:
            media.pop(identity, None)
    manifest = _manifest(shots, internals, list(media.values()), documents)
    digest = _digest(parent)
    if (parent == source["parent_revision"]["payload"]
            and manifest == source["dependency_manifest"]):
        revision = source["parent_revision"]["revision_id"]
    else:
        revision = "authoring-parent-revision-" + _digest({
            "project_id": bundle["project_id"], "timeline_id": bundle["timeline_id"],
            "parent": parent, "manifest": manifest,
        }).removeprefix("sha256:")
    for historical in source_bundles:
        prior = historical['source_mapping']['_runtime_document']
        if equal(parent, prior['parent_revision']['payload']) and equal(manifest, prior['dependency_manifest']):
            revision = prior['parent_revision']['revision_id']
            break
    document = {
        "schema_version": 1, "project_id": bundle["project_id"],
        "timeline_id": bundle["timeline_id"],
        "parent_revision": {"revision_id": revision, "content_digest": digest, "payload": parent},
        "shot_revisions": shots, "internal_timeline_revisions": internals,
        "dependency_manifest": manifest,
    }
    _verify_document(document)
    return copy.deepcopy(document)


def _failure(reason, message, base, current=None, *, conflicts=None):
    return {
        "http_status": 409, "code": "conflict", "message": message,
        "details": {"status": "conflict" if conflicts else "refused", "reason": reason,
                    "base": copy.deepcopy(base), "current": copy.deepcopy(current),
                    "conflicts": conflicts or []},
    }


def _load(port, context, revision):
    document = port.revision_closure(revision)
    request = context["request"]
    _require(document.get("project_id") == request["project_id"]
             and document.get("timeline_id") == request["timeline_id"]
             and document.get("parent_revision", {}).get("revision_id") == revision,
             "Runtime returned a different revision or project/timeline scope")
    return bundle_from_document(document)


def _hydrate(port, bundle, calls=()):
    captures, schema_inputs = [], []
    document = bundle["source_mapping"]["_runtime_document"]
    pins = copy.deepcopy(document["dependency_manifest"]["documents"])
    for call in calls:
        pin = call.get('args', {}).get('schema_source')
        if call['op'] == 'clip.set-params' and pin is not None:
            pin = _document_pin(pin)
            if pin not in pins:
                pins.append(pin)
    for pin in pins:
        transcript = pin["document_id"].startswith("transcript:")
        verified = (port.transcript_source(pin) if transcript else port.config_source(pin))
        _require(isinstance(verified, Mapping) and isinstance(verified.get("document"), Mapping),
                 "invalid scoped source capture")
        source = verified["document"]
        _require(verified["pin"] == pin and source.get("document_id") == pin["document_id"]
                 and source.get("project_id") == bundle["project_id"]
                 and type(source.get("version")) is int
                 and source.get("version") == pin["version"]
                 and _digest(source.get("content")) == pin["content_digest"],
                 "captured document does not match its exact scoped pin")
        if transcript:
            from astrid.sdk.media_transcript import transcript_document_id
            content = source["content"]
            _require(isinstance(content, Mapping) and source.get("kind") == "media.transcript"
                     and content.get("schema") == "media.transcript/v1"
                     and isinstance(content.get("media_id"), str)
                     and _DIGEST.fullmatch(content["media_id"])
                     and _id(content.get("source_id"))
                     and content["media_id"] in {
                         row["media_id"] for row in document["dependency_manifest"]["media"]}
                     and pin["document_id"] == transcript_document_id(
                         bundle["project_id"], content.get("media_id"), content.get("source_id")),
                     "invalid transcript source identity")
        elif source.get('kind') == 'astrid.project-pack':
            schema_inputs.append((copy.deepcopy(verified), {}))
        else:
            _require(isinstance(source.get("kind"), str) and source["kind"].endswith(".config"),
                     "unregistered config source kind")
        captures.append(copy.deepcopy(verified))
    bundle["source_mapping"]["pinned_documents"] = captures
    return schema_inputs


def _schema_resolver(port, inputs, inverse_records):
    """Resolve bytes at the real command stage, never by simulating handlers."""
    from astrid.core.element.project_packs import admitted_element_snapshot_descriptor

    from ._command_state import CommandError

    def resolve(ctx):
        command = ctx.record['command']
        required = []
        if command['op'] == 'clip.set-params' and 'schema_source' in command['args']:
            row = ctx.state.entity(command['select'])
            selected = row.get('elementRef') or row.get('element_ref')
            if isinstance(selected, dict) and selected.get('packId'):
                required.append((command['args']['schema_source'], selected))
        elif command['op'] == 'timeline.inverse':
            for record in inverse_records:
                snapshots = [dep['pin'] for dep in record['dependencies']
                             if dep['key'] == 'params.snapshot']
                required.extend((pin['source'], pin['element']) for pin in snapshots)
                # Older accepted PARAM records already contain exact source and identity reads.
                if not snapshots and record['command']['op'] == 'clip.set-params':
                    pin = record['command']['args'].get('schema_source')
                    identity = {read['path'][0]: read['state'].get('value')
                                for read in record['reads']
                                if read['ref'] == record['command']['select']
                                and read['path'] in (['elementRef'], ['element_ref'])}
                    selected = identity.get('elementRef') or identity.get('element_ref')
                    if pin and isinstance(selected, dict) and selected.get('packId'):
                        required.append((pin, selected))
        for pin, selected in required:
            matches = [(verified, objects) for verified, objects in inputs
                       if verified['pin'] == pin and verified['document']['content'].get(
                           'pack_id') == selected.get('packId')]
            if len(matches) != 1:
                raise CommandError('selected pack snapshot input unavailable')
            verified, objects = matches[0]
            admissions = [item for item in verified['document']['content']['admissions']
                          if all(item.get(key) == selected.get(key)
                                 for key in ('id', 'kind', 'revision'))]
            descriptor = admissions[0].get('snapshot_object') if len(admissions) == 1 else None
            snapshot = None
            if descriptor is not None:
                _require(callable(getattr(port, 'document_object', None)),
                         'Runtime document_object support is required for pack snapshots')
                object_id = descriptor['object_id']
                if object_id not in objects:
                    objects[object_id] = port.document_object(pin, object_id)
                snapshot = objects[object_id]
            if command['op'] == 'timeline.inverse':
                try:
                    admitted_element_snapshot_descriptor(
                        ctx.realm_id, ctx.state.bundle['project_id'], selected, verified, snapshot)
                except ValueError as exc:
                    raise CommandError(str(exc)) from exc
                ctx.dependency('params.schema', 'source', pin)
                ctx.dependency('params.snapshot', 'entity', {
                    'source': pin, 'element': selected, 'object': descriptor})
        return inputs

    return resolve


def _history(port, through, after, rejected, base):
    """Read a complete, bounded ancestry segment, never infer intent from bytes."""
    previous = copy.deepcopy(after)
    entries, cursor, cursors = [], None, set()
    while previous != through:
        page = port.history(through, after_publication_id=after["publication_id"] if after else None,
                            cursor=cursor, limit=100)
        if page["head"] != through:
            raise rejected(_failure("history_unavailable", "history head changed", base, through))
        for entry in page["items"]:
            if entry["previous"] != previous or entry["publication_id"] in {
                    row["publication_id"] for row in entries}:
                raise rejected(_failure("history_unavailable", "incomplete publication ancestry",
                                        base, through))
            entries.append(copy.deepcopy(entry))
            previous = {"revision_id": entry["revision_id"],
                        "publication_id": entry["publication_id"]}
        cursor = page["next_cursor"]
        if cursor is None:
            if previous != through:
                raise rejected(_failure("history_unavailable", "missing publication ancestry",
                                        base, through))
            break
        if cursor in cursors or previous == through:
            raise rejected(_failure("history_unavailable", "invalid history cursor", base, through))
        cursors.add(cursor)
    return entries


def _records(entries, rejected, base, current):
    records = []
    for entry in entries:
        recorder = entry.get("records")
        if (entry.get("intent") != "recorded" or not isinstance(recorder, Mapping)
                or recorder.get("schema_version") != 1
                or not isinstance(recorder.get("commands"), list) or not recorder["commands"]
                or any(not isinstance(record, Mapping) or record.get("ordinal") != ordinal
                       or set(record) != {"ordinal", "command", "writes", "reads", "selections",
                                          "bindings", "created", "dependencies", "derived_writes"}
                       for ordinal, record in enumerate(recorder["commands"]))):
            raise rejected(_failure("history_unavailable", "intervening write intent is unavailable",
                                    base, current))
        records.extend(copy.deepcopy(recorder["commands"]))
    return records


def _reservation_refs(state):
    """Known authored identities only; opaque payloads never allocate IDs."""
    bundle = state.bundle
    refs = {'shot:' + bundle['source_mapping']['shots'].get(identity, {}).get('shot_id', identity)
            for identity in bundle['shots']}
    owners = ['parent', *('occurrence:' + row['occurrence_id'] for row in bundle['placements'])]
    refs.update(owners[1:])
    for owner in owners:
        assets = state.config(owner).get('registry', {}).get('assets', {})
        _require(isinstance(assets, dict), 'invalid asset identity collection')
        refs.update(owner + '/asset:' + identity for identity in assets)
        for kind in ('clip', 'track'):
            collection = state.collection(owner, kind)
            if collection is None:
                continue
            _require(isinstance(collection, list), 'invalid semantic identity collection')
            for row in collection:
                _require(isinstance(row, Mapping) and _id(row.get('id')),
                         'missing semantic identity')
                refs.add(owner + '/' + kind + ':' + row['id'])
    return refs


def _check_reservations(port, plan, current, rejected, base):
    from astrid.sdk.timeline.commands import CommandError

    from ._command_state import State, root_identity

    def valid(item):
        if (not isinstance(item, Mapping) or set(item) != {'ref', 'kind', 'owner'}
                or not _id(item['ref']) or not _id(item['kind'])):
            return False
        root = root_identity(item['ref'])
        if root is not None:
            return (item['kind'] == root[0]
                    and item['owner'] == (None if root[0] == 'shot' else 'parent'))
        owner = item['owner']
        if not _id(owner) or not (owner == 'parent' or (
                root_identity(owner) is not None and root_identity(owner)[0] == 'occurrence')):
            return False
        return (item['kind'] in ('track', 'clip', 'asset')
                and re.fullmatch(re.escape(owner + '/' + item['kind'] + ':') + r'(?!.*::)[^/]+',
                                 item['ref']) is not None)

    for record in plan.records:
        if (any(not valid(item) for item in record['created'])
                or record['command'].get('created') != [item['ref'] for item in record['created']]):
            raise CommandError('invalid created identity scope', kind='identity_collision')

    # This scan is timeline-local. Runtime atomic admission must additionally
    # check project-wide shot occupancy/reservations before persisting a closure.
    # Inverse creates restore authenticated accepted writes. Ordinary creates
    # must never claim an identity retired by an earlier accepted publication.
    created = [item["ref"] for record in plan.records
               if record["command"]["op"] != "timeline.inverse" for item in record["created"]]
    if not created:
        return
    reserved, recorded = set(), False
    context = {'request': {key: plan.bundle[key] for key in ('project_id', 'timeline_id')}}

    def boundary(revision):
        return _load(port, context, revision)

    def scan(records, bundle, *, ordinary=False, output=None):
        state = State(bundle)
        reserved.update(_reservation_refs(state))
        for record in records:
            items = record['created']
            if (not isinstance(items, list) or any(not valid(item) for item in items)
                    or not isinstance(record['command'], Mapping)
                    or record['command'].get('created') != [item['ref'] for item in items]):
                raise CommandError('created identity history is unavailable', kind='history_unavailable')
            check = ordinary and record['command']['op'] != 'timeline.inverse'
            claimed = set()
            for item in items:
                ref = item['ref']
                if check and (ref in reserved or ref in claimed):
                    raise CommandError('created identity was already reserved', kind='identity_collision', ref=ref)
                claimed.add(ref)
            for write in record['writes']:
                if write['ref'] == 'timeline':
                    for pin in (write['before']['value'], write['after']['value']):
                        source = boundary(pin['revision_id'])
                        image = source['source_mapping']['_runtime_document']['parent_revision']
                        _require(pin == {key: image[key] for key in ('revision_id', 'content_digest')},
                                 'historical closure pin mismatch')
                        state.closures[pin['revision_id']] = source
                if not state.matches(write['ref'], write['path'], write['before']):
                    raise CommandError('semantic identity boundary differs from writes', kind='history_unavailable')
                if (record['command']['op'] == 'timeline.inverse' and root_identity(write['ref']) is not None
                        and write['ref'].startswith('occurrence:') and not write['path']
                        and write['after']['state'] == 'present'):
                    from ._root_inverse import recover_source
                    recover_source(state, write['after']['value'], output)
                before = _reservation_refs(state)
                state.set(write['ref'], write['path'], write['after'])
                if write['ref'] == 'timeline':
                    state = State(state.bundle, closures=state.closures)
                after = _reservation_refs(state)
                collisions = (after - before) & reserved if check else set()
                if collisions:
                    raise CommandError('created identity was already reserved', kind='identity_collision',
                                       ref=sorted(collisions)[0])
                reserved.update(after)
            reserved.update(claimed)
            for write in record['derived_writes']:
                state.set(write['ref'], write['path'], write['after'])

    try:
        for entry in _history(port, current, None, rejected, base):
            if (not recorded and entry.get('intent') in {'bootstrap', 'legacy_unknown'}
                    and entry.get('records') is None):
                # Unknown legacy intent is not allocation proof. The first
                # recorded edge supplies its authenticated original boundary.
                continue
            recorded = True
            records = _records([entry], rejected, base, current)
            _require(entry.get('previous') is not None, 'missing original identity boundary')
            scan(records, boundary(entry['previous']['revision_id']), output=boundary(entry['revision_id']))
            reserved.update(_reservation_refs(State(boundary(entry['revision_id']))))
    except (AuthoringBundleError, CommandError, KeyError, TypeError, ValueError) as exc:
        raise rejected(_failure('history_unavailable', 'semantic identity history is unavailable',
                                base, current)) from exc
    scan(plan.records, boundary(current['revision_id']), ordinary=True, output=plan.bundle)


class RuntimeCommitService:
    provider_id = "astrid-v1"
    interface_version = 1

    def __init__(self, contract_digest):
        self.contract_digest = contract_digest

    def commit(self, context, port):
        from runtime_protocol.timeline_commit import CommitRejected, StaleHead

        from astrid.sdk.timeline._collections import AcceptedRecords
        from astrid.sdk.timeline._command_state import State
        from astrid.sdk.timeline.commands import CommandError, execute
        from astrid.sdk.timeline.inverse import check_intervening
        from astrid.sdk.timeline.rebase import replay

        context = copy.deepcopy(context)
        request = context["request"]
        base = {"revision_id": request["base_revision_id"],
                "publication_id": request["base_publication_id"]}
        current = None
        try:
            calls = request["commands"]
            from astrid.sdk.timeline.commands import validate_command
            verified_media = []
            for call in calls:
                validate_command(call)
                if call['op'] in ('occurrence.add-media', 'occurrence.swap-media'):
                    for key in ('old_media', 'media'):
                        if key in call['args']:
                            verified_media.append(port.selected_media(copy.deepcopy(call['args'][key])))
            restore = any(call["op"] == "timeline.restore" for call in calls)
            if restore:
                current = port.head()
                if len(calls) != 1:
                    raise CommitRejected(_failure("invalid_commands", "restore must be the sole command",
                                                  base, current))
                if current != base:
                    raise CommitRejected(_failure("stale_head", "restore requires the exact head pair",
                                                  base, current))
            bundle = _load(port, context, base["revision_id"])
            current = port.head()
            base_entry = port.history_entry(base["publication_id"])
            if base_entry["revision_id"] != base["revision_id"]:
                raise CommitRejected(_failure("history_unavailable", "base publication/revision mismatch",
                                              base, current))
            undo_of = []
            if sum(call["op"] == "timeline.inverse" for call in calls) > 1:
                raise CommitRejected(_failure("unsupported_operation",
                                              "use one inverse command listing all target publications",
                                              base, current))
            for call in calls:
                if call["op"] == "timeline.inverse":
                    for publication in call["args"]["publications"]:
                        if publication not in undo_of:
                            undo_of.append(publication)
            inverse_records, inverse_intervening, inverse_sources = [], [], []
            if undo_of:
                targets = [port.history_entry(publication) for publication in undo_of]
                segments = []
                for target in targets:
                    pin = {"revision_id": target["revision_id"],
                           "publication_id": target["publication_id"]}
                    # Loading the exact target also verifies source scope; no
                    # client-provided inverse writes enter the core engine.
                    _load(port, context, target["revision_id"])
                    segment = [target, *_history(port, base, pin, CommitRejected, base)]
                    segments.append(segment)
                # The longest segment begins at the earliest targeted edge.
                ordered = max(segments, key=len)
                if undo_of != [entry["publication_id"] for entry in ordered
                               if entry["publication_id"] in undo_of]:
                    raise CommitRejected(_failure("invalid_inverse_order",
                                                  "inverse publications must be oldest to newest",
                                                  base, current))
                accepted = [entry for entry in ordered if entry['publication_id'] in undo_of]

                def load_boundary(entry):
                    previous = entry.get('previous')
                    if not previous:
                        raise CommandError('inverse input boundary is unavailable', kind='history_unavailable')
                    prior = port.history_entry(previous['publication_id'])
                    if prior['revision_id'] != previous['revision_id']:
                        raise CommandError('inverse input boundary mismatch', kind='history_unavailable')
                    pin = {key: entry[key] for key in ('revision_id', 'publication_id')}
                    _history(port, pin, previous, CommitRejected, base)
                    return (_load(port, context, previous['revision_id']),
                            _load(port, context, entry['revision_id']))

                inverse_sources = [source for entry in accepted for source in load_boundary(entry)]
                inverse_records = AcceptedRecords(accepted, _records(
                    accepted, CommitRejected, base, current), load_boundary)
                # A gap before a later target is that target's input, not an
                # intervening write after it. Check every target's own suffix
                # before any reversal can mask a non-target overlapping edge.
                for index, entry in enumerate(ordered):
                    if entry['publication_id'] in undo_of:
                        check_intervening(_records([entry], CommitRejected, base, current),
                                          _records([later for later in ordered[index + 1:]
                                                    if later['publication_id'] not in undo_of],
                                                   CommitRejected, base, current),
                                          state=State(_load(port, context, entry['revision_id'])))
            closures, restored_from = {}, None
            if restore:
                restored_from = copy.deepcopy(calls[0]['args'])
                source = _load(port, context, restored_from['revision_id'])
                image = source['source_mapping']['_runtime_document']['parent_revision']
                _require(image['content_digest'] == restored_from['content_digest'],
                         "restore source digest mismatch")
                closures[restored_from['revision_id']] = source
            else:
                # Only authenticated accepted writes can authorize an inverse
                # closure replacement. Never accept a caller-supplied image.
                for write in (write for record in inverse_records for write in record['writes']):
                    if write['ref'] == 'timeline' and not write['path']:
                        pin = write['before']['value']
                        source = _load(port, context, pin['revision_id'])
                        image = source['source_mapping']['_runtime_document']['parent_revision']
                        _require(pin == {key: image[key] for key in ('revision_id', 'content_digest')},
                                 "inverse historical closure pin mismatch")
                        closures[pin['revision_id']] = source
            # The port captures exactly the resulting document inputs. Discarded
            # current/source closures must not retain unrelated document pins.
            schema_inputs = []
            for source in closures.values():
                schema_inputs.extend(_hydrate(port, source))
            if not closures:
                schema_inputs = _hydrate(port, bundle, calls)
            resolve_inputs = _schema_resolver(port, schema_inputs, inverse_records)
            original = execute(bundle, calls, inverse_records=inverse_records,
                               intervening_records=inverse_intervening, closures=closures,
                               verified_media=verified_media, realm_id=context['realm_id'],
                               resolve_inputs=resolve_inputs)
            for attempt in range(3):
                if attempt:
                    current = port.head()
                if current == base:
                    plan = original
                else:
                    if restore:
                        raise CommitRejected(_failure("stale_head", "restore requires the exact head pair",
                                                      base, current))
                    entries = _history(port, current, base, CommitRejected, base)
                    head_bundle = _load(port, context, current["revision_id"])
                    if not closures:
                        schema_inputs = _hydrate(port, head_bundle, calls)
                    resolve_inputs = _schema_resolver(port, schema_inputs, inverse_records)
                    plan = replay(original, head_bundle, inverse_records=inverse_records,
                                  intervening_records=[*inverse_intervening, *_records(
                                      entries, CommitRejected, base, current)], closures=closures,
                                  verified_media=verified_media, realm_id=context['realm_id'],
                                  resolve_inputs=resolve_inputs)
                _check_reservations(port, plan, current, CommitRejected, base)
                document = document_from_bundle(plan.bundle, source_bundles=inverse_sources,
                                                inverse_records=inverse_records)
                prepared = {
                    "expected_head": copy.deepcopy(current), "canonical_document": document,
                    "document_digest": _digest(document),
                    "records": {"schema_version": 1, "commands": copy.deepcopy(plan.records),
                                "undo_of": undo_of, "restored_from": restored_from},
                    "id_map": {}, "semantic_events": copy.deepcopy(plan.semantic_events),
                    "provider_version": PROVIDER_VERSION, "compiler_version": COMPILER_VERSION,
                }
                try:
                    return (port.preview(prepared) if request.get("dry_run", False)
                            else port.accept(prepared))
                except StaleHead as exc:
                    current = copy.deepcopy(exc.current_head)
                    if restore:
                        raise CommitRejected(_failure("stale_head", "restore head changed at acceptance",
                                                      base, current)) from exc
                    continue
            raise CommitRejected(_failure("head_busy", "timeline head changed on three attempts",
                                          base, current))
        except AuthoringBundleError as exc:
            raise CommitRejected(_failure("invalid_document", str(exc), base, current)) from exc
        except CommandError as exc:
            conflicts = ([exc.to_json()] if exc.kind in {
                "value_conflict", "identity_conflict", "identity_collision", "inverse_conflict",
                "dependency_changed", "inverse_dependency_changed",
                "intervening_write", "selection_changed", "surviving_dependents"} else None)
            raise CommitRejected(_failure(exc.kind, str(exc), base, current,
                                          conflicts=conflicts)) from exc


def create_runtime_commit_service():
    """Load Runtime compatibility only when the fixed provider is selected."""
    from runtime_protocol.contract_metadata import SCHEMA_DIGEST

    return RuntimeCommitService(SCHEMA_DIGEST)
