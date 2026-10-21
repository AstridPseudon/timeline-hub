"""Ordered project-data restoration through the accepted-record provider boundary."""

from __future__ import annotations

import copy

from tests.editing_conformance.test_recipe_m2_project_data import TARGET, command, remove
from tests.sdk.test_timeline_commit_provider import (
    DetachedRealm,
    inverse,
    runtime_abi,  # noqa: F401 -- detached provider ABI fixture
)


def test_ordered_namespace_inverse_preserves_accepted_records_and_exact_documents():
    realm = DetachedRealm()
    created = realm.call([
        command("keep", {"opaque": [None, False, 0]}, target="before"),
        command("gone", False),
        command("keep", {"opaque": [None, 0]}, target="after"),
    ])
    original = created["data"]["canonical_document"]
    removed = realm.call([remove("gone")])
    writes = realm.entries[-1]["records"]["commands"][0]["writes"]
    assert writes[1]["before"] == {"state": "present", "value": {}}
    assert writes[1]["insertion_order"] == ["before", TARGET, "after"]

    for expected, order in (
        (original, ["before", TARGET, "after"]),
        (removed["data"]["canonical_document"], ["before", "after"]),
        (original, ["before", TARGET, "after"]),
    ):
        accepted = copy.deepcopy(realm.entries)
        publication = realm.head["publication_id"]
        result = realm.call([inverse([publication])])
        document = result["data"]["canonical_document"]
        assert document == expected
        assert list(document["parent_revision"]["payload"]["config"]["app"]) == order
        assert realm.entries[:-1] == accepted
