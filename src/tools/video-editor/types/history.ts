import type {
  TimelineCommandHistoryMetadata,
  TimelineCommandTransaction,
} from '@/tools/video-editor/commands/index.ts';
import type { AssetRegistry, TimelineConfig } from './index.ts';

export type UndoSnapshot = {
  config: TimelineConfig;
  registry?: AssetRegistry;
  signature: string;
};

export type UndoEntry = {
  imageRestore?: {
    target: import('../data/shotCompositionAdapter.ts').CanonicalShotCompositionHistoryEntry;
    opposite: import('../data/shotCompositionAdapter.ts').CanonicalShotCompositionHistoryEntry;
    expectedHead: string;
    expectedPublicationId?: string | null;
    request?: import('../data/shotCompositionAdapter.ts').ShotCompositionHistoryRestoreRequest;
  };
  /** In-memory ownership only; an unacknowledged native edit has no snapshot save fallback. */
  nativeRegistration?: {
    owner: import('../lib/timeline-data.ts').TimelineData;
    inverse?: import('@/integrations/runtime/generated.ts').EditCommand;
    /** W64/W27 original admitted ordered parent transaction; Redo uses the current head. */
    paramsReplay?: import('@/integrations/runtime/generated.ts').EditCommand[];
    /** Exact inspector batch; Redo replays it through the current-head scheduler. */
    transitionReplay?: import('@/integrations/runtime/generated.ts').EditCommand[];
    /** Exact original selected-media add only; Redo repeats authority validation. */
    mediaReplay?: import('@/integrations/runtime/generated.ts').EditCommand;
    /** W48 Redo replays the admitted captured-order command at the current revision. */
    reorderReplay?: import('@/integrations/runtime/generated.ts').EditCommand;
  };
  snapshot: UndoSnapshot;
  timestamp: string;
  label?: string;
  transactionId?: string;
  command?: {
    history: TimelineCommandHistoryMetadata;
    undoTransaction: TimelineCommandTransaction;
    redoTransaction: TimelineCommandTransaction;
  };
};

export type CheckpointTriggerType =
  | 'session_boundary'
  | 'edit_distance'
  | 'semantic'
  | 'manual';

export type Checkpoint = {
  id: string;
  timelineId: string;
  config: TimelineConfig;
  createdAt: string;
  triggerType: CheckpointTriggerType;
  label: string;
  editsSinceLastCheckpoint: number;
  /** Missing on legacy config-only local recovery material. */
  binding?: CheckpointBinding;
};

export type CheckpointBinding =
  | { kind: 'clean'; image: import('../data/shotCompositionAdapter.ts').CanonicalShotCompositionHistoryEntry }
  | { kind: 'dirty'; base: import('../data/DataProvider.ts').TimelineHeadRevision;
      commands: import('@/integrations/runtime/generated.ts').EditCommand[];
      scope: import('@/integrations/runtime/generated.ts').CommitRequest['scope'];
      source: { via: 'app' }; registry: AssetRegistry };
