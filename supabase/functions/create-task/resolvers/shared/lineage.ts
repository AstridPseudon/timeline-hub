type PayloadRecord = Record<string, unknown>;

export type TimelinePlacementIntent = "after_source" | "replace";

export type TimelinePlacement = {
  timeline_id: string;
  source_clip_id: string;
  target_track: string;
  insertion_time: number;
  intent: TimelinePlacementIntent;
};

export type PlacementIntent = {
  timeline_id: string;
  anchor_clip_id: string;
  anchor_generation_id?: string;
  anchor_variant_id?: string;
  relation: "after";
  preferred_track_id: string;
  fallback_at: number;
  fallback_track_id: string;
};

interface TaskLineageFields {
  shotId?: string;
  basedOn?: string;
  sourceVariantId?: string;
  createAsGeneration?: boolean;
  toolType?: string;
  markPrimaryWhenBasedOn?: boolean;
  timelinePlacement?: TimelinePlacement;
  placementIntent?: PlacementIntent;
}

export function setTaskLineageFields(
  payload: PayloadRecord,
  fields: TaskLineageFields,
): void {
  if (fields.shotId) payload["shot_id"] = fields.shotId;
  if (fields.basedOn) {
    payload["based_on"] = fields.basedOn;
    payload["parent_generation_id"] = fields.basedOn;
  }
  if (fields.sourceVariantId) payload["source_variant_id"] = fields.sourceVariantId;
  if (fields.createAsGeneration) payload["create_as_generation"] = true;
  if (fields.toolType) payload["tool_type"] = fields.toolType;
  if (fields.markPrimaryWhenBasedOn && fields.basedOn) payload["is_primary"] = true;
  if (fields.timelinePlacement) payload["timeline_placement"] = fields.timelinePlacement;
  if (fields.placementIntent) payload["placement_intent"] = fields.placementIntent;
}
