import type { TimelinePlacement } from "../create-task/resolvers/shared/lineage.ts";

export type { AgentSessionStatus } from "../../../src/tools/video-editor/types/agent-session.ts";

// Shared payload contracts used by task lineage and the legacy edge harness.
export type SelectedClipPayload = {
  clip_id: string;
  url: string;
  media_type: "image" | "video";
  is_timeline_backed?: boolean;
  generation_id?: string;
  variant_id?: string;
  prompt?: string;
  shot_id?: string;
  shot_name?: string;
  shot_selection_clip_count?: number;
  track_id?: string;
  at?: number;
  duration?: number;
  timeline_placement?: TimelinePlacement;
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
