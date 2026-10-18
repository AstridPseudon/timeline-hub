// deno-lint-ignore-file
import type { SupabaseClient } from "https://esm.sh/@supabase/supabase-js@2.49.4";
import Ajv from "https://esm.sh/ajv@6.12.6";
import timelineJsonSchema from "../../../vendor/timeline-schema/typescript/dist/timeline.schema.json" with { type: "json" };
import {
  serializeTimelineConfigSnapshot,
  serializeTimelinePair,
  TimelineDomainError,
  type AssetRegistry,
  type TimelineConfig,
} from "../../../src/tools/video-editor/index.ts";
import {
  appendTimelineConfigViaService,
  createTimelineViaService,
  AstridAppendServiceError,
} from "../_shared/astridAppendService.ts";
import { validateTimelinePayload } from "./validate.ts";
import type {
  TimelineImportBody,
  TimelineImportResponseBody,
} from "./types.ts";

// Unknown keys are the canonical domain validator's job: it names them with structured
// per-path issues (unexpected_clip_key, ...), which a generic schema error would hide. The shape
// check therefore keeps the vendored schema's types and required fields but not its closed objects.
function withoutClosedObjects(node: unknown): unknown {
  if (Array.isArray(node)) return node.map(withoutClosedObjects);
  if (node && typeof node === "object") {
    return Object.fromEntries(
      Object.entries(node as Record<string, unknown>)
        .filter(([key, value]) => !(key === "additionalProperties" && value === false))
        .map(([key, value]) => [key, withoutClosedObjects(value)]),
    );
  }
  return node;
}

// Compiled once per isolate from the vendored canonical schema (the TS package only ships types).
const validateTimelineShape = new Ajv({ allErrors: true }).compile(withoutClosedObjects(timelineJsonSchema) as object);

interface Logger {
  info(message: string, context?: Record<string, unknown>): void;
  warn(message: string, context?: Record<string, unknown>): void;
  error(message: string, context?: Record<string, unknown>): void;
}

interface OwnershipVerifier {
  (projectId: string, userId: string): Promise<{
    success: boolean;
    error?: string;
    statusCode?: number;
  }>;
}

function canonicalizeImportPayload(
  timeline: Record<string, unknown>,
  assetRegistry: Record<string, unknown> | null,
): { config: TimelineConfig; assetRegistry: AssetRegistry | null } {
  const typedTimeline = timeline as TimelineConfig;

  if (assetRegistry === null) {
    const serialized = serializeTimelineConfigSnapshot(typedTimeline);
    return {
      config: serialized.config,
      assetRegistry: null,
    };
  }

  const serialized = serializeTimelinePair(
    typedTimeline,
    assetRegistry as AssetRegistry,
  );
  return {
    config: serialized.config,
    assetRegistry: serialized.registry,
  };
}

export interface HandleTimelineImportInput {
  body: TimelineImportBody;
  userId: string;
  supabaseAdmin: SupabaseClient;
  logger: Logger;
  verifyOwnership: OwnershipVerifier;
}

export interface HandleTimelineImportResult {
  status: number;
  body: TimelineImportResponseBody;
}

function isUuid(value: unknown): value is string {
  return (
    typeof value === "string" &&
    /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(value)
  );
}

export async function handleTimelineImport(
  input: HandleTimelineImportInput,
): Promise<HandleTimelineImportResult> {
  const { body, userId, supabaseAdmin, logger, verifyOwnership } = input;

  if (!isUuid(body.project_id)) {
    return { status: 400, body: { ok: false, error: "project_id must be a uuid" } };
  }
  if (!isUuid(body.timeline_id)) {
    return { status: 400, body: { ok: false, error: "timeline_id must be a uuid" } };
  }
  const projectId = body.project_id;
  const timelineId = body.timeline_id;
  const createIfMissing = body.create_if_missing === true;
  const expectedVersionRaw = body.expected_version;
  const expectedVersion =
    typeof expectedVersionRaw === "number" && Number.isFinite(expectedVersionRaw)
      ? Math.trunc(expectedVersionRaw)
      : null;

  // Shape-validate the timeline against the canonical JSON Schema before
  // doing anything else. Astrid's runtime treats unknown clipTypes with the
  // loud-placeholder fallback, so we purposely do NOT enforce the strict
  // effect-id registry here — that's the authoring surface's job.
  if (!validateTimelineShape(body.timeline)) {
    return {
      status: 400,
      body: {
        ok: false,
        error: "timeline payload failed schema validation",
        details: (validateTimelineShape.errors ?? [])
          .map((issue: { dataPath?: string; message?: string }) => `${issue.dataPath ?? ""} ${issue.message ?? ""}`.trim())
          .join("; "),
      },
    };
  }
  const validated = validateTimelinePayload(body);
  if (!validated.ok) {
    return {
      status: 400,
      body: { ok: false, error: validated.error },
    };
  }

  let canonicalized: ReturnType<typeof canonicalizeImportPayload>;
  try {
    canonicalized = canonicalizeImportPayload(validated.timeline, validated.assetRegistry);
  } catch (error) {
    if (error instanceof TimelineDomainError) {
      return {
        status: 400,
        body: {
          ok: false,
          error: "timeline payload failed canonical validation",
          details: {
            level: error.level,
            issues: error.issues,
          },
        },
      };
    }
    throw error;
  }

  // Ownership check: the JWT subject must own the project. SD-022: the user
  // JWT authorizes intent; the service-role key is then used for the actual
  // DB write below. authenticateRequest() already verified the JWT and gave
  // us userId; verifyProjectOwnership compares against projects.user_id.
  const ownership = await verifyOwnership(projectId, userId);
  if (!ownership.success) {
    return {
      status: ownership.statusCode ?? 403,
      body: {
        ok: false,
        error: ownership.error ?? "Forbidden",
      },
    };
  }

  // Lookup current row + version. We need this for: (a) 404/create_if_missing
  // branching, (b) timeline.project_id ownership check, (c) --force fetch.
  const { data: existing, error: lookupError } = await supabaseAdmin
    .from("timelines")
    .select("id, project_id, config_version")
    .eq("id", timelineId)
    .maybeSingle();

  if (lookupError) {
    logger.error("timeline lookup failed", { error: lookupError.message });
    return {
      status: 500,
      body: { ok: false, error: "failed to load timeline", details: lookupError.message },
    };
  }

  if (!existing) {
    if (!createIfMissing) {
      return {
        status: 404,
        body: { ok: false, error: "timeline not found" },
      };
    }
    return await insertNewTimeline({
      logger,
      projectId,
      timelineId,
      userId,
      timelineConfig: canonicalized.config,
      assetRegistry: canonicalized.assetRegistry,
    });
  }

  if (existing.project_id !== projectId) {
    return {
      status: 403,
      body: {
        ok: false,
        error: "timeline belongs to a different project",
      },
    };
  }

  // Version handshake. expected_version is omitted on --force; we then
  // adopt the current version as the expected value (last-write-wins).
  const versionToSend = expectedVersion ?? existing.config_version;

  return await callVersionedRpc({
    logger,
    timelineId,
    timelineConfig: canonicalized.config,
    assetRegistry: canonicalized.assetRegistry,
    expectedVersion: versionToSend,
    currentVersion: existing.config_version,
  });
}

interface InsertNewTimelineInput {
  logger: Logger;
  projectId: string;
  timelineId: string;
  userId: string;
  timelineConfig: TimelineConfig;
  assetRegistry: AssetRegistry | null;
}

async function insertNewTimeline(
  input: InsertNewTimelineInput,
): Promise<HandleTimelineImportResult> {
  const { logger, projectId, timelineId, timelineConfig, assetRegistry } = input;
  try {
    const configVersion = await createTimelineViaService({
      projectId,
      timelineId,
      userId: input.userId,
      config: timelineConfig,
      assetRegistry,
      actor: { type: "agent", id: "timeline-import" },
      source: "supabase_config",
      name: "Imported timeline",
    });
    return {
      status: 201,
      body: {
        ok: true,
        config_version: configVersion,
        created: true,
      },
    };
  } catch (error) {
    const message = error instanceof AstridAppendServiceError
      ? error.detail ?? error.message
      : error instanceof Error
      ? error.message
      : String(error);
    logger.error("timeline create via append service failed", { error: message });
    return {
      status: 500,
      body: { ok: false, error: "timeline insert failed", details: message },
    };
  }
}

interface CallVersionedRpcInput {
  logger: Logger;
  timelineId: string;
  timelineConfig: TimelineConfig;
  assetRegistry: AssetRegistry | null;
  expectedVersion: number;
  currentVersion: number;
}

async function callVersionedRpc(
  input: CallVersionedRpcInput,
): Promise<HandleTimelineImportResult> {
  const {
    logger,
    timelineId,
    timelineConfig,
    assetRegistry,
    expectedVersion,
    currentVersion,
  } = input;
  try {
    const configVersion = await appendTimelineConfigViaService({
      timelineId,
      expectedVersion,
      config: timelineConfig,
      assetRegistry,
      actor: { type: "agent", id: "timeline-import" },
      source: "supabase_config",
    });
    return {
      status: 200,
      body: { ok: true, config_version: configVersion, created: false },
    };
  } catch (error) {
    if (error instanceof AstridAppendServiceError && error.status === 409) {
      return {
        status: 409,
        body: { ok: false, error: "version_mismatch", current_version: currentVersion },
      };
    }
    const message = error instanceof AstridAppendServiceError
      ? error.detail ?? error.message
      : error instanceof Error
      ? error.message
      : String(error);
    logger.error("append service update failed", { error: message });
    return {
      status: 500,
      body: { ok: false, error: "rpc failed", details: message },
    };
  }
}
