import assert from "node:assert/strict";
import test from "node:test";
import { OPERATION_VERSIONS } from "../src/contract-metadata.ts";
import { ApiError, WorkspaceClient } from "../src/generated.ts";

const response = () => ({
  data: { document_id: "doc", kind: "notes", content: { text: "value" }, version: 1 },
  receipt: { receipt_id: "r", command_kind: "document.create", idempotency_key: "key",
    request_hash: "a".repeat(64), project_id: "p", project_seq: [1, 1], event_ids: [], result: {},
    created_at: "2026-10-16T00:00:00Z" },
});

test("document replay mode stays in the query and preserves the mutation body", async () => {
  const calls = [];
  const transport = async (method, path, headers, body) => {
    if (method === "GET" && path === "/v1/health") {
      calls.push({ method, path, headers, body: null });
      return { status: 200, headers: {}, body: new TextEncoder().encode(JSON.stringify({
        status: "ok", protocol: "workspace.v1", schema_digest: "sha256:" + "a".repeat(64),
        runtime_epoch: 1, runtime_session_id: "runtime",
        operation_versions: { createDocument: [1, 2], updateDocument: [1, 2] },
      })) };
    }
    calls.push({ method, path, headers, body: JSON.parse(new TextDecoder().decode(body)) });
    return { status: method === "POST" ? 201 : 200, headers: {}, body: new TextEncoder().encode(JSON.stringify(response())) };
  };
  const client = new WorkspaceClient("http://runtime", "token", transport);
  await client.createDocument("p", "doc", "notes", { text: "create" }, "create-key", true);
  await client.createDocument("p", "doc", "notes", { text: "ordinary" }, "ordinary-key");
  await client.updateDocument("p", "doc", 1, "update-key", { text: "update" }, undefined, true);

  assert.deepEqual(calls.filter(({ path }) => path !== "/v1/health").map(({ method, path }) => [method, path]), [
    ["POST", "/v1/projects/p/documents?replay_only=true"],
    ["POST", "/v1/projects/p/documents"],
    ["PATCH", "/v1/projects/p/documents/doc?replay_only=true"],
  ]);
  const mutationCalls = calls.filter(({ method }) => method !== "GET");
  assert.deepEqual(mutationCalls[0].body, { document_id: "doc", kind: "notes", content: { text: "create" } });
  assert.deepEqual(mutationCalls[2].body, { expected_version: 1, content: { text: "update" } });
  assert.ok(mutationCalls.every(({ body }) => !Object.hasOwn(body, "replay_only")));
  assert.equal(calls.filter(({ path }) => path === "/v1/health").length, 2);
});

test("document replay mode requires v2 on the matching advertised operation", async () => {
  for (const operation of ["create", "update"]) {
    const calls = [];
    const operationVersions = { createDocument: [1, 2], updateDocument: [1, 2] };
    operationVersions[operation === "create" ? "createDocument" : "updateDocument"] = [1];
    const transport = async (method, path) => {
      calls.push([method, path]);
      return { status: 200, headers: {}, body: new TextEncoder().encode(JSON.stringify({
        status: "ok", protocol: "workspace.v1", schema_digest: "sha256:" + "a".repeat(64),
        runtime_epoch: 1, runtime_session_id: "runtime", operation_versions: operationVersions,
      })) };
    };
    const client = new WorkspaceClient("http://old-runtime", "token", transport);
    const request = operation === "create"
      ? client.createDocument("p", "doc", "notes", {}, "key", true)
      : client.updateDocument("p", "doc", 1, "key", undefined, undefined, true);
    await assert.rejects(request, error => error instanceof ApiError && error.code === "unsupported_operation_version");
    assert.deepEqual(calls, [["GET", "/v1/health"]]);
  }
});

test("document operation metadata retains v1 and advertises replay-only v2", () => {
  assert.deepEqual(OPERATION_VERSIONS.createDocument, [1, 2]);
  assert.deepEqual(OPERATION_VERSIONS.updateDocument, [1, 2]);
});
