#!/usr/bin/env python3
"""Render checked-in contract metadata and the Python client from canonical inputs.

The release/conformance client generators consume the same component manifest;
this small repository-local command keeps the package artifacts bound to that
manifest as well.  The Python client is rendered from the tracked template;
``--check`` remains a read-only stale-artifact check.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
from pathlib import Path
from typing import Any, Mapping


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "contract" / "manifest.json"
COMPONENT_MANIFEST = ROOT / "contract" / "component-manifest.json"
PYTHON_CLIENT_TEMPLATE = ROOT / "generators" / "python_client_template.py"
PYTHON_CLIENT_OUTPUT = ROOT / "packages" / "python" / "banodoco_workspace_client" / "generated.py"
TYPESCRIPT_CLIENT_OUTPUT = ROOT / "packages" / "typescript" / "src" / "generated.ts"


def _regular(path: Path, label: str) -> bytes:
    if path.is_symlink() or not path.is_file():
        raise SystemExit(f"{label} must be a regular file")
    return path.read_bytes()


def _component(path: Path = COMPONENT_MANIFEST) -> tuple[bytes, Mapping[str, Any]]:
    raw = _regular(path, "component manifest")
    try:
        value = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise SystemExit("component manifest must be UTF-8 JSON") from exc
    canonical = (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode()
    if raw != canonical:
        raise SystemExit("component manifest must use canonical JSON bytes")
    if value.get("schema_version") != 1 or value.get("manifest_id") != "GENERATOR-CONFORMANCE-ID":
        raise SystemExit("component manifest identity is invalid")
    return raw, value


def _digest(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def contract_digest(manifest_path: Path = MANIFEST) -> str:
    manifest = json.loads(_regular(manifest_path, "schema manifest"))
    paths = [ROOT / "contract" / manifest["openapi"], *(ROOT / "contract" / p for p in manifest["schemas"])]
    h = hashlib.sha256()
    for path in paths:
        relative = path.relative_to(ROOT).as_posix().encode()
        data = _regular(path, "contract input")
        h.update(len(relative).to_bytes(4, "big")); h.update(relative)
        h.update(len(data).to_bytes(8, "big")); h.update(data)
    data = _regular(OPCALL_SCHEMA, "Astrid OpCall contract input")
    # Hash source identity/bytes independently of language projection support.
    # Generating a validator still calls opcall_schema() and refuses constructs
    # it cannot enforce; an unrelated projection must not invent a digest.
    identity = json.loads(data).get("$id")
    if identity != "https://astrid.local/schemas/change-contract/opcall.schema.json":
        raise SystemExit("unexpected OpCall source identity")
    logical = identity.encode()
    h.update(len(logical).to_bytes(4, "big")); h.update(logical)
    h.update(len(data).to_bytes(8, "big")); h.update(data)
    return "sha256:" + h.hexdigest()


def operation_index(manifest_path: Path = MANIFEST) -> list[str]:
    manifest = json.loads(_regular(manifest_path, "schema manifest"))
    text = (ROOT / "contract" / manifest["openapi"]).read_text(encoding="utf-8")
    return [line.split(":", 1)[1].strip() for line in text.splitlines() if re.match(r"^\s+operationId:", line)]


# One source, explicitly selected for isolated source tuples. No editable Runtime copy.
OPCALL_SCHEMA = Path(os.environ.get("ASTRID_OPCALL_SCHEMA", str(ROOT.parent / "Astrid/schemas/change-contract/opcall.schema.json")))


def opcall_schema() -> dict[str, Any]:
    value = json.loads(_regular(OPCALL_SCHEMA, "Astrid OpCall schema (use --opcall-schema or --astrid-root)"))
    if value.get("$id") != "https://astrid.local/schemas/change-contract/opcall.schema.json":
        raise SystemExit("unexpected OpCall source identity")
    _check_opcall_projection(value)
    return value


def _check_opcall_projection(root: dict[str, Any]) -> None:
    """Admit only the JSON Schema subset implemented in both emitted validators.

    Walk definitions and every nested constraint, including opaque-map value
    schemas. Unknown keywords/references/cycles must fail before writing outputs.
    Patterns are an explicit cross-language subset, not arbitrary Python regexes.
    """
    patterns = {
        r"^[a-z][a-z0-9_-]*(\.[a-z][a-z0-9_-]*)+$",
        r"^(?:(?:parent|shot:[^/]+|occurrence:[^/]+)/(?:clip|track):[^/]+|cut:[^/:]+)$",
        r"^(?:(?:parent|shot:[^/]+|occurrence:[^/]+)/(?:clip|track):[^/]+|occurrence:[^/]+(?:/shot)?|cut:[^/:]+)$",
        r"^(?:word:[^:]+:[0-9]+|beat:[0-9]+|cut:[^/:]+:(?:start|end))$",
    }
    annotations = {"description", "title", "default"}
    supported = annotations | {"type", "properties", "required", "additionalProperties", "items", "pattern", "oneOf", "enum", "const", "$ref"}

    def refuse():
        raise SystemExit("OpCall validator projection has an unsupported schema constraint or reference")

    def visit(node, active=(), top=False):
        if not isinstance(node, dict) or set(node) - (supported | ({"$schema", "$id", "$defs"} if top else set())):
            refuse()
        if "$ref" in node:
            ref = node["$ref"]
            if set(node) - (annotations | {"$ref"}) or not isinstance(ref, str) or not ref.startswith("#/$defs/"):
                refuse()
            key = ref.removeprefix("#/$defs/")
            if key not in root.get("$defs", {}) or key in active:
                refuse()
            visit(root["$defs"][key], (*active, key))
        if "type" in node:
            kinds = node["type"] if isinstance(node["type"], list) else [node["type"]]
            if not kinds or any(kind not in ("string", "null", "object", "array") for kind in kinds):
                refuse()
        if "pattern" in node and (node.get("type") != "string" or node["pattern"] not in patterns):
            refuse()
        if "properties" in node:
            if node.get("type") != "object" or not isinstance(node["properties"], dict):
                refuse()
            for field in node["properties"].values():
                visit(field, active)
        if "required" in node:
            required = node["required"]
            if (node.get("type") != "object" or not isinstance(required, list)
                    or any(not isinstance(key, str) or key not in node.get("properties", {}) for key in required)
                    or len(required) != len(set(required))):
                refuse()
        if "additionalProperties" in node:
            extra = node["additionalProperties"]
            if node.get("type") != "object":
                refuse()
            if not isinstance(extra, bool):
                visit(extra, active)
        if "items" in node:
            if node.get("type") != "array":
                refuse()
            visit(node["items"], active)
        if "oneOf" in node:
            if not isinstance(node["oneOf"], list) or not node["oneOf"]:
                refuse()
            for branch in node["oneOf"]:
                visit(branch, active)
        if "const" in node and not isinstance(node["const"], str):
            refuse()
        if "enum" in node and (not isinstance(node["enum"], list) or not node["enum"] or any(not isinstance(v, str) for v in node["enum"])):
            refuse()

    if (root.get("$schema") != "https://json-schema.org/draft/2020-12/schema"
            or root.get("type") != "object" or root.get("additionalProperties") is not False
            or set(root.get("properties", {})) != {"op", "select", "args", "expect", "bindings", "created", "authorship", "version", "resolved"}
            or not {"op", "select", "args"} <= set(root.get("required", []))
            or not isinstance(root.get("$defs"), dict)):
        refuse()
    visit(root, top=True)
    for key, node in root["$defs"].items():
        visit(node, (key,))


COMMIT_SCHEMA = ROOT / "contract" / "schemas" / "timeline-commit.json"
COMMIT_START = "// BEGIN GENERATED TIMELINE COMMIT"
COMMIT_END = "// END GENERATED TIMELINE COMMIT"


def commit_types(language: str) -> str:
    """Project structural types from the Runtime schema, never from generated output.

    JSON Schema conditionals remain validator-enforced. EditCommand and canonical
    timeline documents remain opaque; OpCall comes from its existing Astrid schema.
    """
    opcall = opcall_schema()
    definitions = {"EditCommand": opcall, **json.loads(_regular(COMMIT_SCHEMA, "timeline commit schema"))["$defs"]}

    lines: list[str] = []

    def expression(schema: Mapping[str, Any], name: str) -> str:
        if "$ref" in schema:
            if schema["$ref"].startswith("#/$defs/") and schema["$ref"].rsplit("/", 1)[-1] in opcall["$defs"]:
                return expression(opcall["$defs"][schema["$ref"].rsplit("/", 1)[-1]], name)
            return "EditCommand" if schema["$ref"] == opcall_schema()["$id"] else schema["$ref"].rsplit("/", 1)[-1]
        if "allOf" in schema and "properties" not in schema:
            # allOf here refines a named structural type using JSON conditionals.
            return expression(schema["allOf"][0], name)
        if "const" in schema or "enum" in schema:
            values = schema.get("enum", [schema.get("const")])
            if language == "typescript":
                return " | ".join(json.dumps(v) for v in values)
            return "Literal[" + ", ".join(repr(v) for v in values) + "]"
        for union in ("oneOf", "anyOf"):
            if union in schema:
                return " | ".join(expression(v, name + str(i)) for i, v in enumerate(schema[union]))
        kind = schema.get("type")
        if isinstance(kind, list):
            return " | ".join(expression({**schema, "type": item}, name) for item in kind)
        if kind == "array":
            inner = expression(schema["items"], name + "Item")
            return f"Array<{inner}>" if language == "typescript" else f"list[{inner}]"
        if kind == "object":
            properties = schema.get("properties")
            if properties is None:
                inner = expression(schema.get("additionalProperties") if isinstance(schema.get("additionalProperties"), dict) else {}, name + "Value")
                return f"Record<string, {inner}>" if language == "typescript" else f"dict[str, {inner}]"
            required = schema.get("required", [])
            fields = []
            for key, value in properties.items():
                inner = expression(value, name + key.title().replace("_", ""))
                if language == "typescript":
                    fields.append(json.dumps(key) + ("" if key in required else "?") + ": " + inner)
                else:
                    annotation = repr(inner) if key in required else "NotRequired[" + repr(inner) + "]"
                    fields.append(repr(key) + ": " + annotation)
            if language == "typescript":
                return "{ " + "; ".join(fields) + " }"
            lines.append(name + " = TypedDict(" + repr(name) + ", {" + ", ".join(fields) + "})")
            return name
        return ({"string": "string", "integer": "number", "number": "number", "boolean": "boolean", "null": "null"}.get(kind, "unknown")
                if language == "typescript" else {"string": "str", "integer": "int", "number": "float", "boolean": "bool", "null": "None"}.get(kind, "Any"))

    for name, schema in definitions.items():
        value = expression(schema, name)
        if language == "typescript" or value != name:
            lines.append(f"export type {name} = {value};" if language == "typescript" else f"{name} = {value}")
    interface = json.loads(_regular(COMMIT_SCHEMA, "timeline commit schema"))["x-runtime-interface"]
    lines.append("export interface RuntimeAcceptance {" if language == "typescript" else "class RuntimeAcceptance(Protocol):")
    for name, method in interface.items():
        parameters = ", ".join(key + ": " + expression(value, name + key) for key, value in method["parameters"].items())
        result = expression(method["returns"], name + "Result")
        lines.append(f"  {name}({parameters}): Promise<{result}>;" if language == "typescript" else f"    def {name}(self, {parameters}) -> {result}: ...")
    if language == "typescript":
        lines.append("}")
    return "\n".join(lines) + "\n" + command_support(language)


def command_support(language: str) -> str:
    schema = opcall_schema()
    if language == "python":
        return "OPCALL_SCHEMA = " + repr(schema) + "\n" + PYTHON_COMMAND_VALIDATOR
    return "export const OPCALL_SCHEMA = " + json.dumps(schema, ensure_ascii=False) + " as const;\n" + TYPESCRIPT_COMMAND_VALIDATOR


PYTHON_COMMAND_VALIDATOR = r'''
def validate_edit_command(value: Any) -> Mapping[str, Any]:
    """Validate only the OpCall envelope; return the exact unmodified value."""
    import math
    import re
    def finite_json(item):
        if item is None or isinstance(item, (str, bool, int)):
            return True
        if isinstance(item, float):
            return math.isfinite(item)
        if isinstance(item, list):
            return all(finite_json(v) for v in item)
        if isinstance(item, dict):
            return all(isinstance(k, str) and finite_json(v) for k, v in item.items())
        return False
    if not isinstance(value, dict):
        raise ValueError("OpCall must be an object")
    fields = OPCALL_SCHEMA["properties"]
    if set(value) - set(fields) or not set(OPCALL_SCHEMA["required"]) <= set(value):
        raise ValueError("OpCall missing or unknown field")
    try:
        valid_json = finite_json(value)
    except RecursionError:
        valid_json = False
    if not valid_json:
        raise ValueError("OpCall requires finite JSON values")
    types = {"string": lambda v: isinstance(v, str), "null": lambda v: v is None,
             "object": lambda v: isinstance(v, dict), "array": lambda v: isinstance(v, list)}
    def matches(node, item):
        if "$ref" in node:
            return matches(OPCALL_SCHEMA["$defs"][node["$ref"].rsplit("/", 1)[-1]], item)
        if "oneOf" in node and sum(matches(branch, item) for branch in node["oneOf"]) != 1:
            return False
        if "const" in node and item != node["const"]:
            return False
        if "enum" in node and item not in node["enum"]:
            return False
        if "type" in node:
            kinds = node["type"] if isinstance(node["type"], list) else [node["type"]]
            if not any(types[kind](item) for kind in kinds):
                return False
        if isinstance(item, str) and "pattern" in node and re.search(node["pattern"], item) is None:
            return False
        if isinstance(item, list) and "items" in node and not all(matches(node["items"], v) for v in item):
            return False
        if isinstance(item, dict):
            fields = node.get("properties", {})
            if not set(node.get("required", [])) <= set(item):
                return False
            for key, child in item.items():
                if key in fields:
                    if not matches(fields[key], child):
                        return False
                else:
                    extra = node.get("additionalProperties", True)
                    if extra is False or (isinstance(extra, dict) and not matches(extra, child)):
                        return False
        return True
    if not matches(OPCALL_SCHEMA, value):
        raise ValueError("OpCall invalid envelope")
    return value


def validate_edit_command_bytes(raw: bytes) -> bytes:
    """Validate without reserializing: whitespace, key order and UTF-8 survive."""
    import json
    def unique_object(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError("duplicate JSON field: " + key)
            result[key] = value
        return result
    validate_edit_command(json.loads(raw, object_pairs_hook=unique_object))
    return raw
'''

TYPESCRIPT_COMMAND_VALIDATOR = r'''
export function validateEditCommand(value: unknown): EditCommand {
  const object = (v: unknown): v is Record<string, unknown> => v !== null && typeof v === "object" && !Array.isArray(v) && Object.getPrototypeOf(v) === Object.prototype;
  const seen = new Set<object>();
  const finiteJson = (v: unknown): boolean => {
    if (v === null || typeof v === "string" || typeof v === "boolean") return true;
    if (typeof v === "number") return Number.isFinite(v);
    if (typeof v !== "object" || seen.has(v)) return false;
    seen.add(v);
    const keys = Reflect.ownKeys(v);
    const dataValues = () => keys.filter(key => key !== "length" || !Array.isArray(v)).every(key => {
      const descriptor = Object.getOwnPropertyDescriptor(v, key)!;
      return typeof key === "string" && descriptor.enumerable && "value" in descriptor && finiteJson(descriptor.value);
    });
    const valid = Array.isArray(v)
      ? keys.length === v.length + 1 && keys.every(key => key === "length" || (typeof key === "string" && /^(0|[1-9][0-9]*)$/.test(key) && Number(key) < v.length)) && dataValues()
      : object(v) && dataValues();
    seen.delete(v);
    return valid;
  };
  if (!object(value)) throw new TypeError("OpCall must be an object");
  type Schema = { type?: string | readonly string[]; pattern?: string; items?: Schema;
    properties?: Record<string, Schema>; required?: readonly string[]; additionalProperties?: boolean | Schema;
    oneOf?: readonly Schema[]; enum?: readonly string[]; const?: string; $ref?: string };
  const own = (v: object, key: string) => Object.prototype.hasOwnProperty.call(v, key);
  const fields = OPCALL_SCHEMA.properties;
  if (Object.keys(value).some(key => !own(fields, key)) || OPCALL_SCHEMA.required.some(key => !own(value, key))) throw new TypeError("OpCall missing or unknown field");
  if (!finiteJson(value)) throw new TypeError("OpCall requires finite JSON values");
  const types: Record<string, (v: unknown) => boolean> = { string: v => typeof v === "string", null: v => v === null, object, array: Array.isArray };
  const matches = (node: Schema, item: unknown): boolean => {
    if (node.$ref) return matches((OPCALL_SCHEMA.$defs as Record<string, Schema>)[node.$ref.split("/").pop()!], item);
    if (node.oneOf && node.oneOf.filter(branch => matches(branch, item)).length !== 1) return false;
    if (own(node, "const") && item !== node.const) return false;
    if (node.enum && !node.enum.some(v => v === item)) return false;
    if (node.type) {
      const kinds = typeof node.type === "string" ? [node.type] : node.type;
      if (!kinds.some(kind => types[kind](item))) return false;
    }
    // Match the admitted Python JSON Schema oracle's end anchor, which permits
    // one final LF. Keep CR and Unicode line separators distinct.
    if (typeof item === "string" && node.pattern && !new RegExp(node.pattern.slice(0, -1) + "(?=\\n?(?![\\s\\S]))").test(item)) return false;
    if (Array.isArray(item) && node.items && !item.every(v => matches(node.items!, v))) return false;
    if (object(item)) {
      const fields = node.properties ?? {};
      if (node.required?.some(key => !own(item, key))) return false;
      for (const [key, child] of Object.entries(item)) {
        if (own(fields, key)) {
          if (!matches(fields[key], child)) return false;
        } else {
          const extra = node.additionalProperties ?? true;
          if (extra === false || (typeof extra === "object" && !matches(extra, child))) return false;
        }
      }
    }
    return true;
  };
  if (!matches(OPCALL_SCHEMA, value)) throw new TypeError("OpCall invalid envelope");
  return value as EditCommand;
}
'''


def commit_route() -> str:
    text = (ROOT / "contract/openapi/workspace-v1.yaml").read_text()
    match = re.search(r"^  (/[^\n]+):\n    post:\n      operationId: commitTimeline$", text, re.MULTILINE)
    if not match:
        raise SystemExit("commitTimeline POST route missing from OpenAPI")
    return match[1]


def render_commit_typescript(source: str) -> str:
    block = COMMIT_START + "\n" + commit_types("typescript") + "\n" + COMMIT_END
    if COMMIT_START in source:
        source, count = re.subn(re.escape(COMMIT_START) + r".*?" + re.escape(COMMIT_END), lambda _: block, source, flags=re.DOTALL)
        if count != 1:
            raise SystemExit("invalid generated commit type markers")
    else:
        source = source.replace("export const PROTOCOL", block + "\nexport const PROTOCOL", 1)
    route = commit_route().replace("{project_id}", "${encodeURIComponent(body.project_id)}").replace("{timeline_id}", "${encodeURIComponent(body.timeline_id)}")
    method = '  async commitTimeline(body: CommitRequest): Promise<CommitResult> { return this.json<CommitResult>((await this.request("POST", `' + route + '`, new TextEncoder().encode(JSON.stringify(body)), { "Content-Type": "application/json", "Idempotency-Key": body.request_id, "X-Astrid-Session": body.session_id }, [200, 400, 503])).body) }'
    if re.search(r"^  async commitTimeline\(", source, re.MULTILINE):
        source = re.sub(r"^  async commitTimeline\(.*$", lambda _: method, source, flags=re.MULTILINE)
    else:
        source = source.replace("  async health()", method + "\n  async health()", 1)
    return source


def render_python_client(manifest_path: Path = MANIFEST) -> str:
    """Render the checked-in Python client from its tracked template.

    The template is deliberately separate from the output: ``--check`` must
    detect a mutated generated client rather than merely re-reading it.  The
    contract digest and operation projection are embedded so the artifact is
    also bound to the canonical OpenAPI/schema inputs.
    """
    template = _regular(PYTHON_CLIENT_TEMPLATE, "Python client template").decode("utf-8")
    if "__SCHEMA_DIGEST__" not in template or "__OPERATIONS__" not in template:
        raise SystemExit("Python client template is missing generator placeholders")
    operations = operation_index(manifest_path)
    if not operations or len(operations) != len(set(operations)):
        raise SystemExit("contract operation projection must be non-empty and unique")
    rendered = template.replace("Authoritative Python client template; rendered by generators/generate.py.", "Generated from contract/openapi/workspace-v1.yaml; do not edit by hand.")
    rendered = rendered.replace("__SCHEMA_DIGEST__", contract_digest(manifest_path))
    rendered = rendered.replace("__OPERATIONS__", repr(tuple(operations)))
    rendered = rendered.replace("__COMMIT_TYPES__", commit_types("python"))
    rendered = rendered.replace("__MEDIA_SELECTION_TYPES__", media_selection_types("python"))
    rendered = rendered.replace("__COMMIT_ROUTE__", commit_route().replace("{project_id}", "{_path_part(body['project_id'])}").replace("{timeline_id}", "{_path_part(body['timeline_id'])}"))
    return rendered


def media_selection_types(language: str) -> str:
    schema = json.loads(_regular(ROOT / "contract/schemas/project-media-selection.json", "media selection schema"))
    fields = schema["required"]
    if (schema.get("additionalProperties") is not False or set(fields) != set(schema["properties"])
            or any(value.get("type") != "string" for value in schema["properties"].values())):
        raise SystemExit("unsupported media selection schema projection")
    if language == "python":
        return "class ProjectMediaSelection(TypedDict):\n" + "\n".join(f"    {field}: str" for field in fields)
    return "export interface ProjectMediaSelection { " + "; ".join(f"{field}: string" for field in fields) + " }"


def render_media_selection_typescript(source: str) -> str:
    start, end = "// BEGIN GENERATED PROJECT MEDIA SELECTION", "// END GENERATED PROJECT MEDIA SELECTION"
    block = start + "\n" + media_selection_types("typescript") + "\n" + end
    if start in source:
        source = re.sub(re.escape(start) + r".*?" + re.escape(end), lambda _: block, source, count=1, flags=re.S)
    else:
        source = source.replace("export interface GenerationVariant", block + "\nexport interface GenerationVariant", 1)
    method = '  async getProjectMediaSelection(projectId: string, asset: string, generationId: string, variantId: string): Promise<ProjectMediaSelection> { const query = `asset=${encodeURIComponent(asset)}&generation_id=${encodeURIComponent(generationId)}&variant_id=${encodeURIComponent(variantId)}`; return this.json<ProjectMediaSelection>((await this.request("GET", `/v1/projects/${encodeURIComponent(projectId)}/media-selection?${query}`)).body) }'
    if "  async getProjectMediaSelection(" in source:
        source = re.sub(r"^  async getProjectMediaSelection\([^\n]*", lambda _: method, source, count=1, flags=re.M)
    else:
        anchor = next(line for line in source.splitlines() if line.startswith("  async listGenerations("))
        source = source.replace(anchor, method + "\n" + anchor, 1)
    return source


def render_typescript_client() -> str:
    """Render the source-frame thumbnail operations into the typed TS client."""
    source = render_media_selection_typescript(render_commit_typescript(_regular(TYPESCRIPT_CLIENT_OUTPUT, "TypeScript client").decode("utf-8")))
    child_authority_types = (
        'export interface ChildAuthorityChild { child_id: string; capability_id: string; capability_digest: string }\n'
        'export interface DerivedInputDescriptor { name: string; output_port: string; filename: string; object_id: string; size: number; media_type: string }\n'
        'export interface ChildAuthorityRequest { lease_id: string; fence: number; runtime_epoch: number; child?: ChildAuthorityChild; derived_inputs?: DerivedInputDescriptor[] }'
    )
    if "export interface ChildAuthorityRequest " not in source:
        anchor = "export interface ObjectLocation"
        if anchor not in source:
            raise SystemExit("TypeScript client is missing the child-authority type insertion point")
        source = source.replace(anchor, child_authority_types + "\n" + anchor, 1)
    old_child_authority_method = '  async issueChildAuthority(attemptId: string, body: { lease_id: string; fence: number; runtime_epoch: number }): Promise<Record<string, unknown>>'
    new_child_authority_method = '  async issueChildAuthority(attemptId: string, body: ChildAuthorityRequest): Promise<Record<string, unknown>>'
    if new_child_authority_method not in source:
        if old_child_authority_method not in source:
            raise SystemExit("TypeScript child-authority client projection is partially present")
        source = source.replace(old_child_authority_method, new_child_authority_method, 1)
    snapshot_type = 'export interface RecoverableSnapshotRequest { lease_id: string; fence: number; runtime_epoch: number; revision: number; output: DerivedInputDescriptor }'
    if "export interface RecoverableSnapshotRequest " not in source:
        source = source.replace("export interface ObjectLocation", snapshot_type + "\nexport interface ObjectLocation", 1)
    snapshot_method = '  async publishRecoverableSnapshot(attemptId: string, body: RecoverableSnapshotRequest, idempotencyKey: string): Promise<MutationResult<ManagedOutput>> { return this.mutation<ManagedOutput>((await this.request("POST", `/v1/attempts/${encodeURIComponent(attemptId)}/recoverable-snapshots`, new TextEncoder().encode(JSON.stringify(body)), { "Content-Type": "application/json", "Idempotency-Key": idempotencyKey })).body) }'
    if "  async publishRecoverableSnapshot(" not in source:
        source = source.replace("  async issueChildAuthority(", snapshot_method + "\n  async issueChildAuthority(", 1)
    source = source.replace(
        'export interface GenerationVariant { variant_id: string; generation_id: string; object_id?: string | null; variant_type: string; metadata: Record<string, unknown>; thumbnail?: { object_id: string; source_object_id: string; recipe_version: number } | null; viewed_at?: string | null; created_at: string }',
        'export interface ThumbnailDescriptor { object_id: string; source_object_id: string; recipe_version: number; selection?: { kind: "variant" | "source_frame"; source_time_seconds?: number } }\nexport interface GenerationVariant { variant_id: string; generation_id: string; object_id?: string | null; variant_type: string; metadata: Record<string, unknown>; thumbnail?: ThumbnailDescriptor | null; viewed_at?: string | null; created_at: string }',
        1,
    )
    get_method = '  async getSourceFrameThumbnail(projectId: string, sourceObjectId: string, sourceTimeSeconds: number, recipeVersion = 1): Promise<Record<string, unknown> | null> { const query = `source_object_id=${encodeURIComponent(sourceObjectId)}&source_time_seconds=${sourceTimeSeconds.toFixed(6)}&recipe_version=${recipeVersion}`; return this.json<{ thumbnail: Record<string, unknown> | null }>((await this.request("GET", `/v1/projects/${encodeURIComponent(projectId)}/thumbnails/source-frame?${query}`)).body).thumbnail }'
    ensure_method = '  async ensureSourceFrameThumbnail(projectId: string, thumbnail: Record<string, unknown>, idempotencyKey: string): Promise<MutationResult<Record<string, unknown>>> { return this.mutation<Record<string, unknown>>((await this.request("POST", `/v1/projects/${encodeURIComponent(projectId)}/thumbnails/source-frame`, new TextEncoder().encode(JSON.stringify(thumbnail)), { "Content-Type": "application/json", "Idempotency-Key": idempotencyKey }, [200, 201])).body) }'
    markers = ("  async getSourceFrameThumbnail(", "  async ensureSourceFrameThumbnail(")
    present = tuple(marker in source for marker in markers)
    if all(present):
        return source
    if any(present):
        raise SystemExit("TypeScript source-frame thumbnail client projection is partially present")
    anchor = next((line for line in source.splitlines() if line.startswith("  async listMediaRelations(")), None)
    if anchor is None:
        raise SystemExit("TypeScript client is missing the listMediaRelations insertion point")
    return source.replace(anchor, anchor + "\n" + get_method + "\n" + ensure_method, 1)


def validate_typescript_client(manifest_path: Path = MANIFEST) -> None:
    """Fail closed when the typed product projection drifts from OpenAPI.

    The TypeScript client remains a typed repository source rather than a
    Python-template copy.  This check still binds every public method to the
    canonical operation projection and asserts the execution binding fields
    whose types cannot be inferred by the small metadata renderer.
    """
    source = _regular(TYPESCRIPT_CLIENT_OUTPUT, "TypeScript client").decode("utf-8")
    methods = set(re.findall(r"^  async (\w+)\(", source, re.MULTILINE))
    expected = set(operation_index(manifest_path)) | {"updateTimelineDocument"}
    if methods != expected:
        missing = sorted(expected - methods)
        extra = sorted(methods - expected)
        raise SystemExit(
            "TypeScript client operation projection drifted"
            + (f"; missing={missing}" if missing else "")
            + (f"; extra={extra}" if extra else "")
        )
    required_fragments = (
        "actual_target?: ExecutionTarget",
        "verification?: ExecutionBindingVerification",
        "executor_incarnation?: string",
        "run_id: string; project_id: string | null; lease_id: string",
        "lease_expires_at: string; runtime_epoch: number",
        "provider_state_unknown",
    )
    missing_fragments = [value for value in required_fragments if value not in source]
    if missing_fragments:
        raise SystemExit(
            "TypeScript execution contract projection is stale: "
            + ", ".join(missing_fragments)
        )


def render(manifest_path: Path = MANIFEST, component_path: Path = COMPONENT_MANIFEST) -> dict[str, str]:
    opcall_schema()  # Refuse unprojectable canonical inputs before emitting any metadata.
    component_bytes, component = _component(component_path)
    digest = contract_digest(manifest_path)
    operations = operation_index(manifest_path)
    component_digest = _digest(component_bytes)
    py = ('"""Generated contract metadata; do not edit by hand."""\n\n'
          'PROTOCOL = "workspace.v1"\nCOMPONENT_MANIFEST_SHA256 = ' + repr(component_digest) +
          '\nSCHEMA_DIGEST = ' + repr(digest) + "\nOPERATIONS = " + repr(tuple(operations)) + "\n")
    ts = ('/** Generated contract metadata; do not edit by hand. */\n\n'
          'export const PROTOCOL = "workspace.v1" as const;\nexport const COMPONENT_MANIFEST_SHA256 = ' + json.dumps(component_digest) +
          ';\nexport const SCHEMA_DIGEST = ' + json.dumps(digest) + ";\nexport const OPERATIONS = " + json.dumps(operations) + " as const;\n")
    runtime = ('"""Generated contract metadata; do not edit by hand."""\n\n'
               'PROTOCOL = "workspace.v1"\nCOMPONENT_MANIFEST_SHA256 = ' + repr(component_digest) +
               '\nSCHEMA_DIGEST = ' + repr(digest) + "\nOPERATIONS = " + repr(tuple(operations)) + "\n")
    # Keep the three package metadata modules bound to the same manifest.  The
    # standalone Python/TypeScript client artifacts and fixture bundle are
    # emitted by their language-specific conformance generators.
    _ = component
    return {"packages/python/banodoco_workspace_client/contract_metadata.py": py, "packages/typescript/src/contract-metadata.ts": ts, "runtime_protocol/contract_metadata.py": runtime}


def main() -> int:
    parser = argparse.ArgumentParser()
    global OPCALL_SCHEMA
    parser.add_argument("--opcall-schema", help="existing Astrid OpCall source, not a Runtime schema copy")
    parser.add_argument("--check", action="store_true", help="fail if generated metadata differs")
    parser.add_argument("--component-manifest", default=str(COMPONENT_MANIFEST))
    parser.add_argument("--python-output", default=str(PYTHON_CLIENT_OUTPUT), help="Python client output path (for isolated checks)")
    parser.add_argument("--typescript-output", default=str(TYPESCRIPT_CLIENT_OUTPUT), help="TypeScript client output path (for isolated checks)")
    parser.add_argument("--astrid-root", help="sync/check only the existing Astrid generated client and metadata")
    parser.add_argument("--app-root", help="sync/check only the existing App generated client and metadata")
    args = parser.parse_args()
    if args.opcall_schema:
        OPCALL_SCHEMA = Path(args.opcall_schema).expanduser().resolve()
    elif args.astrid_root:
        OPCALL_SCHEMA = Path(args.astrid_root).expanduser().resolve() / "schemas/change-contract/opcall.schema.json"
    generated = render(component_path=Path(args.component_manifest).expanduser())
    generated["runtime_protocol/edit_command.py"] = ('"""Generated from Astrid OpCall; no timing or edit execution."""\nfrom typing import Any, Mapping\n' + command_support("python"))
    generated["packages/python/banodoco_workspace_client/generated.py"] = render_python_client()
    generated["packages/typescript/src/generated.ts"] = render_typescript_client()
    products: dict[Path, str] = {}
    if args.astrid_root:
        product = Path(args.astrid_root).expanduser().resolve() / "banodoco_workspace_client"
        if not (product / "generated.py").is_file():
            raise SystemExit("Astrid existing generated client is required")
        products[product / "generated.py"] = generated["packages/python/banodoco_workspace_client/generated.py"]
        products[product / "contract_metadata.py"] = generated["packages/python/banodoco_workspace_client/contract_metadata.py"]
    if args.app_root:
        product = Path(args.app_root).expanduser().resolve() / "src/integrations/runtime"
        if not (product / "generated.ts").is_file():
            raise SystemExit("App existing generated client is required")
        products[product / "generated.ts"] = generated["packages/typescript/src/generated.ts"]
        products[product / "generated-contract-metadata.ts"] = generated["packages/typescript/src/contract-metadata.ts"]
    for path, content in products.items():
        if args.check:
            if not path.is_file() or path.read_text(encoding="utf-8") != content:
                print(f"stale generated product file: {path}")
                return 1
        else:
            path.write_text(content, encoding="utf-8")
            print(path)
    for relative, content in generated.items():
        if relative == "packages/python/banodoco_workspace_client/generated.py":
            path = Path(args.python_output).expanduser().resolve()
        elif relative == "packages/typescript/src/generated.ts":
            path = Path(args.typescript_output).expanduser().resolve()
        else:
            path = ROOT / relative
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                print(f"stale generated file: {relative}")
                return 1
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
            print(relative)
    validate_typescript_client()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
