import { createHash } from 'node:crypto';
import { describe, expect, it } from 'vitest';
import type { EditCommand, JSON, MediaSelection } from '@/integrations/runtime/timeline-commit-types.ts';
import { captureAutoBasis, executeAutoBirth, finishAutoCapture } from './autoCapture.ts';
import { AuthoredState, copy, type AuthoredBundle } from './clipMovePrimitives.ts';

// Exact Agent 80f5149631bb2b08c0569a2a53192e14442991e7 inputs. The twelve
// hashes compare COMPLETE native commands, records and after bundles, preserving
// array order and binary64 values. No moving handoff or Runtime release is used.
const originals = [
  {
    "schema_version": 1,
    "project_id": "project-1",
    "timeline_id": "film",
    "base_parent": {"revision_id":"parent-1","content_digest":"sha256:02bb61acb800f5abc184c4daf315217cbc01b02c2fd88780a2e4e7c6b7504f89"},
    "base_parent_payload": {"config":{"tracks":[{"id":"picture","kind":"visual"}],"clips":[{"id":"clip-a","track":"picture","asset":"picture","clipType":"media","at":1,"hold":2,"app":{"org.example":{"literal":"clip-a","clear":null}}},{"id":"clip-b","track":"picture","asset":"picture","clipType":"media","at":5,"hold":2,"app":{"org.example":{"literal":"clip-a","clear":null}}}],"output":{"fps":{"numerator":30000,"denominator":1001}},"opaque":{"timestamp":"authored timestamp","v":[null,false,0]}},"clips":[{"id":"clip-a","track":"picture","asset":"picture","clipType":"media","at":1,"hold":2,"app":{"org.example":{"literal":"clip-a","clear":null}}},{"id":"clip-b","track":"picture","asset":"picture","clipType":"media","at":5,"hold":2,"app":{"org.example":{"literal":"clip-a","clear":null}}}],"registry":{"assets":{"picture":{"media_id":"sha256:1111111111111111111111111111111111111111111111111111111111111111","type":"image"}}},"name":"Renamed Film","unknown":{"opaque":["parent-1",null]}},
    "base_placements": {"occ-a":{"occurrence_id":"occ-a","shot_id":"shot-placement-17545afbc02f243b9327cabff19dacf2c3bc6ee5e2abd3a4c4a0415124093e9f","placement":{"start_ms":8000,"track":"picture"},"duration_ms":10000,"source_offset":0,"speed":1,"track":"picture","unknown":{"literal":"chapter-shot"}},"occ-b":{"occurrence_id":"occ-b","shot_id":"shot-placement-5b5386eab3e8b66c027da5fec80cc34c2b8942db4b276a6b53f5bc4f3a4bb943","placement":{"start_ms":10000,"track":"picture"},"duration_ms":10000,"source_offset":0,"speed":1,"track":"picture","unknown":{"literal":"chapter-shot"}}},
    "parent": {"config":{"tracks":[{"id":"picture","kind":"visual"}],"clips":[{"id":"clip-a","track":"picture","asset":"picture","clipType":"media","at":1,"hold":2,"app":{"org.example":{"literal":"clip-a","clear":null}}},{"id":"clip-b","track":"picture","asset":"picture","clipType":"media","at":5,"hold":2,"app":{"org.example":{"literal":"clip-a","clear":null}}}],"output":{"fps":{"numerator":30000,"denominator":1001}},"opaque":{"timestamp":"authored timestamp","v":[null,false,0]}},"clips":[{"id":"clip-a","track":"picture","asset":"picture","clipType":"media","at":1,"hold":2,"app":{"org.example":{"literal":"clip-a","clear":null}}},{"id":"clip-b","track":"picture","asset":"picture","clipType":"media","at":5,"hold":2,"app":{"org.example":{"literal":"clip-a","clear":null}}}],"registry":{"assets":{"picture":{"media_id":"sha256:1111111111111111111111111111111111111111111111111111111111111111","type":"image"}}},"name":"Renamed Film","unknown":{"opaque":["parent-1",null]}},
    "placements": [{"occurrence_id":"occ-a","shot_id":"shot-placement-17545afbc02f243b9327cabff19dacf2c3bc6ee5e2abd3a4c4a0415124093e9f","placement":{"start_ms":8000,"track":"picture"},"duration_ms":10000,"source_offset":0,"speed":1,"track":"picture","unknown":{"literal":"chapter-shot"}},{"occurrence_id":"occ-b","shot_id":"shot-placement-5b5386eab3e8b66c027da5fec80cc34c2b8942db4b276a6b53f5bc4f3a4bb943","placement":{"start_ms":10000,"track":"picture"},"duration_ms":10000,"source_offset":0,"speed":1,"track":"picture","unknown":{"literal":"chapter-shot"}}],
    "shots": {"shot-placement-17545afbc02f243b9327cabff19dacf2c3bc6ee5e2abd3a4c4a0415124093e9f":{"shot_id":"shot-placement-17545afbc02f243b9327cabff19dacf2c3bc6ee5e2abd3a4c4a0415124093e9f","base_payload":{"name":"Chapter One","internal_timeline_revision_id":"internal-1","items":[{"item_id":"shot-item-placement-cb1bf5d05853ca0713af2d9450cfbb2f3d41bbda49e6b17c2d62b854e0b1c993","media_id":"sha256:1111111111111111111111111111111111111111111111111111111111111111","metadata":{"opaque_literal":"item-1"}}],"text_bindings":[{"slot":"narration","text":"A chapter"}],"metadata":{"chapter":true},"unknown":{"keep":null}},"payload":{"name":"Chapter One","internal_timeline_revision_id":"internal-1","items":[{"item_id":"shot-item-placement-cb1bf5d05853ca0713af2d9450cfbb2f3d41bbda49e6b17c2d62b854e0b1c993","media_id":"sha256:1111111111111111111111111111111111111111111111111111111111111111","metadata":{"opaque_literal":"item-1"}}],"text_bindings":[{"slot":"narration","text":"A chapter"}],"metadata":{"chapter":true},"unknown":{"keep":null}},"base_internal_timeline":{"tracks":[{"id":"picture","kind":"visual"}],"clips":[{"id":"clip-a","track":"picture","asset":"picture","clipType":"media","at":1,"hold":2,"app":{"org.example":{"literal":"clip-a","clear":null}}},{"id":"clip-b","track":"picture","asset":"picture","clipType":"media","at":5,"hold":2,"app":{"org.example":{"literal":"clip-a","clear":null}}}],"output":{"fps":{"numerator":30000,"denominator":1001}},"opaque":{"timestamp":"authored timestamp","v":[null,false,0]},"registry":{"assets":{"picture":{"media_id":"sha256:1111111111111111111111111111111111111111111111111111111111111111","type":"image"}}},"unknown":[1,2]},"internal_timeline":{"tracks":[{"id":"picture","kind":"visual"}],"clips":[{"id":"clip-a","track":"picture","asset":"picture","clipType":"media","at":1,"hold":2,"app":{"org.example":{"literal":"clip-a","clear":null}}},{"id":"clip-b","track":"picture","asset":"picture","clipType":"media","at":5,"hold":2,"app":{"org.example":{"literal":"clip-a","clear":null}}}],"output":{"fps":{"numerator":30000,"denominator":1001}},"opaque":{"timestamp":"authored timestamp","v":[null,false,0]},"registry":{"assets":{"picture":{"media_id":"sha256:1111111111111111111111111111111111111111111111111111111111111111","type":"image"}}},"unknown":[1,2]}},"shot-placement-5b5386eab3e8b66c027da5fec80cc34c2b8942db4b276a6b53f5bc4f3a4bb943":{"shot_id":"shot-placement-5b5386eab3e8b66c027da5fec80cc34c2b8942db4b276a6b53f5bc4f3a4bb943","base_payload":{"name":"Chapter One","internal_timeline_revision_id":"internal-1","items":[{"item_id":"shot-item-placement-2710e450613ad9d41bfea49b9df1e5d86eeca6be63c82986e5ca0d20677b339f","media_id":"sha256:1111111111111111111111111111111111111111111111111111111111111111","metadata":{"opaque_literal":"item-1"}}],"text_bindings":[{"slot":"narration","text":"A chapter"}],"metadata":{"chapter":true},"unknown":{"keep":null}},"payload":{"name":"Chapter One","internal_timeline_revision_id":"internal-1","items":[{"item_id":"shot-item-placement-2710e450613ad9d41bfea49b9df1e5d86eeca6be63c82986e5ca0d20677b339f","media_id":"sha256:1111111111111111111111111111111111111111111111111111111111111111","metadata":{"opaque_literal":"item-1"}}],"text_bindings":[{"slot":"narration","text":"A chapter"}],"metadata":{"chapter":true},"unknown":{"keep":null}},"base_internal_timeline":{"tracks":[{"id":"picture","kind":"visual"}],"clips":[{"id":"clip-a","track":"picture","asset":"picture","clipType":"media","at":1,"hold":2,"app":{"org.example":{"literal":"clip-a","clear":null}}},{"id":"clip-b","track":"picture","asset":"picture","clipType":"media","at":5,"hold":2,"app":{"org.example":{"literal":"clip-a","clear":null}}}],"output":{"fps":{"numerator":30000,"denominator":1001}},"opaque":{"timestamp":"authored timestamp","v":[null,false,0]},"registry":{"assets":{"picture":{"media_id":"sha256:1111111111111111111111111111111111111111111111111111111111111111","type":"image"}}},"unknown":[1,2]},"internal_timeline":{"tracks":[{"id":"picture","kind":"visual"}],"clips":[{"id":"clip-a","track":"picture","asset":"picture","clipType":"media","at":1,"hold":2,"app":{"org.example":{"literal":"clip-a","clear":null}}},{"id":"clip-b","track":"picture","asset":"picture","clipType":"media","at":5,"hold":2,"app":{"org.example":{"literal":"clip-a","clear":null}}}],"output":{"fps":{"numerator":30000,"denominator":1001}},"opaque":{"timestamp":"authored timestamp","v":[null,false,0]},"registry":{"assets":{"picture":{"media_id":"sha256:1111111111111111111111111111111111111111111111111111111111111111","type":"image"}}},"unknown":[1,2]}}},
    "source_mapping": {"placements":{"occ-a":{"occurrence_id":"occ-a","shot_id":"shot-placement-17545afbc02f243b9327cabff19dacf2c3bc6ee5e2abd3a4c4a0415124093e9f","placement":{"start_ms":8000,"track":"picture"},"duration_ms":10000,"source_offset":0,"speed":1,"track":"picture","unknown":{"literal":"chapter-shot"}},"occ-b":{"occurrence_id":"occ-b","shot_id":"shot-placement-5b5386eab3e8b66c027da5fec80cc34c2b8942db4b276a6b53f5bc4f3a4bb943","placement":{"start_ms":10000,"track":"picture"},"duration_ms":10000,"source_offset":0,"speed":1,"track":"picture","unknown":{"literal":"chapter-shot"}}},"shots":{"shot-placement-17545afbc02f243b9327cabff19dacf2c3bc6ee5e2abd3a4c4a0415124093e9f":{"shot_id":"chapter-shot","revision_id":"shot-1","content_digest":"sha256:f700f1f65d6111e008f10de355a74ab6b41b766f4ff4070bd62f97206a3f0775","internal_timeline_id":"chapter-1","internal_timeline_revision_id":"internal-1","internal_timeline_content_digest":"sha256:f579c1ef3548804d91bdaedcd7acdca9af674baf2f458b74bc6606ffd7cce502","item_id_map":{"item-1":"shot-item-placement-cb1bf5d05853ca0713af2d9450cfbb2f3d41bbda49e6b17c2d62b854e0b1c993"}},"shot-placement-5b5386eab3e8b66c027da5fec80cc34c2b8942db4b276a6b53f5bc4f3a4bb943":{"shot_id":"chapter-shot","revision_id":"shot-1","content_digest":"sha256:f700f1f65d6111e008f10de355a74ab6b41b766f4ff4070bd62f97206a3f0775","internal_timeline_id":"chapter-1","internal_timeline_revision_id":"internal-1","internal_timeline_content_digest":"sha256:f579c1ef3548804d91bdaedcd7acdca9af674baf2f458b74bc6606ffd7cce502","item_id_map":{"item-1":"shot-item-placement-2710e450613ad9d41bfea49b9df1e5d86eeca6be63c82986e5ca0d20677b339f"}}},"_runtime_document":{"schema_version":1,"project_id":"project-1","timeline_id":"film","parent_revision":{"revision_id":"parent-1","payload":{"config":{"tracks":[{"id":"picture","kind":"visual"}],"clips":[{"id":"clip-a","track":"picture","asset":"picture","clipType":"media","at":1,"hold":2,"app":{"org.example":{"literal":"clip-a","clear":null}}},{"id":"clip-b","track":"picture","asset":"picture","clipType":"media","at":5,"hold":2,"app":{"org.example":{"literal":"clip-a","clear":null}}}],"output":{"fps":{"numerator":30000,"denominator":1001}},"opaque":{"timestamp":"authored timestamp","v":[null,false,0]}},"clips":[{"id":"clip-a","track":"picture","asset":"picture","clipType":"media","at":1,"hold":2,"app":{"org.example":{"literal":"clip-a","clear":null}}},{"id":"clip-b","track":"picture","asset":"picture","clipType":"media","at":5,"hold":2,"app":{"org.example":{"literal":"clip-a","clear":null}}}],"registry":{"assets":{"picture":{"media_id":"sha256:1111111111111111111111111111111111111111111111111111111111111111","type":"image"}}},"occurrences":[{"occurrence_id":"occ-a","shot_id":"chapter-shot","shot_revision_id":"shot-1","placement":{"start_ms":8000,"track":"picture"},"duration_ms":10000,"source_offset":0,"speed":1,"track":"picture","unknown":{"literal":"chapter-shot"}},{"occurrence_id":"occ-b","shot_id":"chapter-shot","shot_revision_id":"shot-1","placement":{"start_ms":10000,"track":"picture"},"duration_ms":10000,"source_offset":0,"speed":1,"track":"picture","unknown":{"literal":"chapter-shot"}}],"name":"Renamed Film","unknown":{"opaque":["parent-1",null]}},"content_digest":"sha256:02bb61acb800f5abc184c4daf315217cbc01b02c2fd88780a2e4e7c6b7504f89"},"shot_revisions":[{"shot_id":"chapter-shot","revision_id":"shot-1","internal_timeline_revision_id":"internal-1","payload":{"name":"Chapter One","internal_timeline_revision_id":"internal-1","items":[{"item_id":"item-1","media_id":"sha256:1111111111111111111111111111111111111111111111111111111111111111","metadata":{"opaque_literal":"item-1"}}],"text_bindings":[{"slot":"narration","text":"A chapter"}],"metadata":{"chapter":true},"unknown":{"keep":null}},"content_digest":"sha256:f700f1f65d6111e008f10de355a74ab6b41b766f4ff4070bd62f97206a3f0775"}],"internal_timeline_revisions":[{"revision_id":"internal-1","timeline_id":"chapter-1","payload":{"tracks":[{"id":"picture","kind":"visual"}],"clips":[{"id":"clip-a","track":"picture","asset":"picture","clipType":"media","at":1,"hold":2,"app":{"org.example":{"literal":"clip-a","clear":null}}},{"id":"clip-b","track":"picture","asset":"picture","clipType":"media","at":5,"hold":2,"app":{"org.example":{"literal":"clip-a","clear":null}}}],"output":{"fps":{"numerator":30000,"denominator":1001}},"opaque":{"timestamp":"authored timestamp","v":[null,false,0]},"registry":{"assets":{"picture":{"media_id":"sha256:1111111111111111111111111111111111111111111111111111111111111111","type":"image"}}},"unknown":[1,2]},"content_digest":"sha256:f579c1ef3548804d91bdaedcd7acdca9af674baf2f458b74bc6606ffd7cce502"}],"dependency_manifest":{"shots":[{"shot_id":"chapter-shot","revision_id":"shot-1","internal_timeline_revision_id":"internal-1","content_digest":"sha256:f700f1f65d6111e008f10de355a74ab6b41b766f4ff4070bd62f97206a3f0775"}],"internal_timelines":[{"timeline_id":"chapter-1","revision_id":"internal-1","content_digest":"sha256:f579c1ef3548804d91bdaedcd7acdca9af674baf2f458b74bc6606ffd7cce502"}],"media":[{"media_id":"sha256:1111111111111111111111111111111111111111111111111111111111111111","content_digest":"sha256:1111111111111111111111111111111111111111111111111111111111111111"}],"documents":[]}}}
  },
  {
    "schema_version": 1,
    "project_id": "project-1",
    "timeline_id": "film",
    "base_parent": {"revision_id":"parent-1","content_digest":"sha256:86c97a97fb837467f83918e31ce27d76c59740c83fec38a22562ce4d213c249b"},
    "base_parent_payload": {"config":{"tracks":[{"id":"picture","kind":"visual"}],"clips":[{"id":"clip-a","track":"picture","asset":"picture","clipType":"media","at":1,"hold":2,"app":{"org.example":{"literal":"clip-a","clear":null}}},{"id":"clip-b","track":"picture","asset":"picture","clipType":"media","at":5,"hold":2,"app":{"org.example":{"literal":"clip-a","clear":null}}}],"output":{"fps":{"numerator":30000,"denominator":1001}},"opaque":{"timestamp":"authored timestamp","v":[null,false,0]}},"clips":[{"id":"clip-a","track":"picture","asset":"picture","clipType":"media","at":1,"hold":2,"app":{"org.example":{"literal":"clip-a","clear":null}}},{"id":"clip-b","track":"picture","asset":"picture","clipType":"media","at":5,"hold":2,"app":{"org.example":{"literal":"clip-a","clear":null}}}],"registry":{"assets":{"picture":{"media_id":"sha256:1111111111111111111111111111111111111111111111111111111111111111","type":"video"}}},"name":"Renamed Film","unknown":{"opaque":["parent-1",null]}},
    "base_placements": {"occ-a":{"occurrence_id":"occ-a","shot_id":"shot-placement-17545afbc02f243b9327cabff19dacf2c3bc6ee5e2abd3a4c4a0415124093e9f","placement":{"start_ms":8000,"track":"picture"},"duration_ms":10000,"source_offset":0,"speed":1,"track":"picture","unknown":{"literal":"chapter-shot"}},"occ-b":{"occurrence_id":"occ-b","shot_id":"shot-placement-5b5386eab3e8b66c027da5fec80cc34c2b8942db4b276a6b53f5bc4f3a4bb943","placement":{"start_ms":10000,"track":"picture"},"duration_ms":10000,"source_offset":0,"speed":1,"track":"picture","unknown":{"literal":"chapter-shot"}}},
    "parent": {"config":{"tracks":[{"id":"picture","kind":"visual"}],"clips":[{"id":"clip-a","track":"picture","asset":"picture","clipType":"media","at":1,"hold":2,"app":{"org.example":{"literal":"clip-a","clear":null}}},{"id":"clip-b","track":"picture","asset":"picture","clipType":"media","at":5,"hold":2,"app":{"org.example":{"literal":"clip-a","clear":null}}}],"output":{"fps":{"numerator":30000,"denominator":1001}},"opaque":{"timestamp":"authored timestamp","v":[null,false,0]}},"clips":[{"id":"clip-a","track":"picture","asset":"picture","clipType":"media","at":1,"hold":2,"app":{"org.example":{"literal":"clip-a","clear":null}}},{"id":"clip-b","track":"picture","asset":"picture","clipType":"media","at":5,"hold":2,"app":{"org.example":{"literal":"clip-a","clear":null}}}],"registry":{"assets":{"picture":{"media_id":"sha256:1111111111111111111111111111111111111111111111111111111111111111","type":"video"}}},"name":"Renamed Film","unknown":{"opaque":["parent-1",null]}},
    "placements": [{"occurrence_id":"occ-a","shot_id":"shot-placement-17545afbc02f243b9327cabff19dacf2c3bc6ee5e2abd3a4c4a0415124093e9f","placement":{"start_ms":8000,"track":"picture"},"duration_ms":10000,"source_offset":0,"speed":1,"track":"picture","unknown":{"literal":"chapter-shot"}},{"occurrence_id":"occ-b","shot_id":"shot-placement-5b5386eab3e8b66c027da5fec80cc34c2b8942db4b276a6b53f5bc4f3a4bb943","placement":{"start_ms":10000,"track":"picture"},"duration_ms":10000,"source_offset":0,"speed":1,"track":"picture","unknown":{"literal":"chapter-shot"}}],
    "shots": {"shot-placement-17545afbc02f243b9327cabff19dacf2c3bc6ee5e2abd3a4c4a0415124093e9f":{"shot_id":"shot-placement-17545afbc02f243b9327cabff19dacf2c3bc6ee5e2abd3a4c4a0415124093e9f","base_payload":{"name":"Chapter One","internal_timeline_revision_id":"internal-1","items":[{"item_id":"shot-item-placement-cb1bf5d05853ca0713af2d9450cfbb2f3d41bbda49e6b17c2d62b854e0b1c993","media_id":"sha256:1111111111111111111111111111111111111111111111111111111111111111","metadata":{"opaque_literal":"item-1"}}],"text_bindings":[{"slot":"narration","text":"A chapter"}],"metadata":{"chapter":true},"unknown":{"keep":null}},"payload":{"name":"Chapter One","internal_timeline_revision_id":"internal-1","items":[{"item_id":"shot-item-placement-cb1bf5d05853ca0713af2d9450cfbb2f3d41bbda49e6b17c2d62b854e0b1c993","media_id":"sha256:1111111111111111111111111111111111111111111111111111111111111111","metadata":{"opaque_literal":"item-1"}}],"text_bindings":[{"slot":"narration","text":"A chapter"}],"metadata":{"chapter":true},"unknown":{"keep":null}},"base_internal_timeline":{"tracks":[{"id":"picture","kind":"visual"}],"clips":[{"id":"clip-a","track":"picture","asset":"picture","clipType":"media","at":1,"hold":4,"app":{"org.example":{"literal":"clip-a","clear":null}},"from":2,"to":6,"speed":2},{"id":"clip-b","track":"picture","asset":"picture","clipType":"media","at":5,"hold":2,"app":{"org.example":{"literal":"clip-a","clear":null}}}],"output":{"fps":{"numerator":30000,"denominator":1001}},"opaque":{"timestamp":"authored timestamp","v":[null,false,0]},"registry":{"assets":{"picture":{"media_id":"sha256:1111111111111111111111111111111111111111111111111111111111111111","type":"video"}}},"unknown":[1,2]},"internal_timeline":{"tracks":[{"id":"picture","kind":"visual"}],"clips":[{"id":"clip-a","track":"picture","asset":"picture","clipType":"media","at":1,"hold":4,"app":{"org.example":{"literal":"clip-a","clear":null}},"from":2,"to":6,"speed":2},{"id":"clip-b","track":"picture","asset":"picture","clipType":"media","at":5,"hold":2,"app":{"org.example":{"literal":"clip-a","clear":null}}}],"output":{"fps":{"numerator":30000,"denominator":1001}},"opaque":{"timestamp":"authored timestamp","v":[null,false,0]},"registry":{"assets":{"picture":{"media_id":"sha256:1111111111111111111111111111111111111111111111111111111111111111","type":"video"}}},"unknown":[1,2]}},"shot-placement-5b5386eab3e8b66c027da5fec80cc34c2b8942db4b276a6b53f5bc4f3a4bb943":{"shot_id":"shot-placement-5b5386eab3e8b66c027da5fec80cc34c2b8942db4b276a6b53f5bc4f3a4bb943","base_payload":{"name":"Chapter One","internal_timeline_revision_id":"internal-1","items":[{"item_id":"shot-item-placement-2710e450613ad9d41bfea49b9df1e5d86eeca6be63c82986e5ca0d20677b339f","media_id":"sha256:1111111111111111111111111111111111111111111111111111111111111111","metadata":{"opaque_literal":"item-1"}}],"text_bindings":[{"slot":"narration","text":"A chapter"}],"metadata":{"chapter":true},"unknown":{"keep":null}},"payload":{"name":"Chapter One","internal_timeline_revision_id":"internal-1","items":[{"item_id":"shot-item-placement-2710e450613ad9d41bfea49b9df1e5d86eeca6be63c82986e5ca0d20677b339f","media_id":"sha256:1111111111111111111111111111111111111111111111111111111111111111","metadata":{"opaque_literal":"item-1"}}],"text_bindings":[{"slot":"narration","text":"A chapter"}],"metadata":{"chapter":true},"unknown":{"keep":null}},"base_internal_timeline":{"tracks":[{"id":"picture","kind":"visual"}],"clips":[{"id":"clip-a","track":"picture","asset":"picture","clipType":"media","at":1,"hold":4,"app":{"org.example":{"literal":"clip-a","clear":null}},"from":2,"to":6,"speed":2},{"id":"clip-b","track":"picture","asset":"picture","clipType":"media","at":5,"hold":2,"app":{"org.example":{"literal":"clip-a","clear":null}}}],"output":{"fps":{"numerator":30000,"denominator":1001}},"opaque":{"timestamp":"authored timestamp","v":[null,false,0]},"registry":{"assets":{"picture":{"media_id":"sha256:1111111111111111111111111111111111111111111111111111111111111111","type":"video"}}},"unknown":[1,2]},"internal_timeline":{"tracks":[{"id":"picture","kind":"visual"}],"clips":[{"id":"clip-a","track":"picture","asset":"picture","clipType":"media","at":1,"hold":4,"app":{"org.example":{"literal":"clip-a","clear":null}},"from":2,"to":6,"speed":2},{"id":"clip-b","track":"picture","asset":"picture","clipType":"media","at":5,"hold":2,"app":{"org.example":{"literal":"clip-a","clear":null}}}],"output":{"fps":{"numerator":30000,"denominator":1001}},"opaque":{"timestamp":"authored timestamp","v":[null,false,0]},"registry":{"assets":{"picture":{"media_id":"sha256:1111111111111111111111111111111111111111111111111111111111111111","type":"video"}}},"unknown":[1,2]}}},
    "source_mapping": {"placements":{"occ-a":{"occurrence_id":"occ-a","shot_id":"shot-placement-17545afbc02f243b9327cabff19dacf2c3bc6ee5e2abd3a4c4a0415124093e9f","placement":{"start_ms":8000,"track":"picture"},"duration_ms":10000,"source_offset":0,"speed":1,"track":"picture","unknown":{"literal":"chapter-shot"}},"occ-b":{"occurrence_id":"occ-b","shot_id":"shot-placement-5b5386eab3e8b66c027da5fec80cc34c2b8942db4b276a6b53f5bc4f3a4bb943","placement":{"start_ms":10000,"track":"picture"},"duration_ms":10000,"source_offset":0,"speed":1,"track":"picture","unknown":{"literal":"chapter-shot"}}},"shots":{"shot-placement-17545afbc02f243b9327cabff19dacf2c3bc6ee5e2abd3a4c4a0415124093e9f":{"shot_id":"chapter-shot","revision_id":"shot-1","content_digest":"sha256:f700f1f65d6111e008f10de355a74ab6b41b766f4ff4070bd62f97206a3f0775","internal_timeline_id":"chapter-1","internal_timeline_revision_id":"internal-1","internal_timeline_content_digest":"sha256:0693a443fc594c55a609396fbb0f92114b7a6bf1d880230818a76226c9648622","item_id_map":{"item-1":"shot-item-placement-cb1bf5d05853ca0713af2d9450cfbb2f3d41bbda49e6b17c2d62b854e0b1c993"}},"shot-placement-5b5386eab3e8b66c027da5fec80cc34c2b8942db4b276a6b53f5bc4f3a4bb943":{"shot_id":"chapter-shot","revision_id":"shot-1","content_digest":"sha256:f700f1f65d6111e008f10de355a74ab6b41b766f4ff4070bd62f97206a3f0775","internal_timeline_id":"chapter-1","internal_timeline_revision_id":"internal-1","internal_timeline_content_digest":"sha256:0693a443fc594c55a609396fbb0f92114b7a6bf1d880230818a76226c9648622","item_id_map":{"item-1":"shot-item-placement-2710e450613ad9d41bfea49b9df1e5d86eeca6be63c82986e5ca0d20677b339f"}}},"_runtime_document":{"schema_version":1,"project_id":"project-1","timeline_id":"film","parent_revision":{"revision_id":"parent-1","payload":{"config":{"tracks":[{"id":"picture","kind":"visual"}],"clips":[{"id":"clip-a","track":"picture","asset":"picture","clipType":"media","at":1,"hold":2,"app":{"org.example":{"literal":"clip-a","clear":null}}},{"id":"clip-b","track":"picture","asset":"picture","clipType":"media","at":5,"hold":2,"app":{"org.example":{"literal":"clip-a","clear":null}}}],"output":{"fps":{"numerator":30000,"denominator":1001}},"opaque":{"timestamp":"authored timestamp","v":[null,false,0]}},"clips":[{"id":"clip-a","track":"picture","asset":"picture","clipType":"media","at":1,"hold":2,"app":{"org.example":{"literal":"clip-a","clear":null}}},{"id":"clip-b","track":"picture","asset":"picture","clipType":"media","at":5,"hold":2,"app":{"org.example":{"literal":"clip-a","clear":null}}}],"registry":{"assets":{"picture":{"media_id":"sha256:1111111111111111111111111111111111111111111111111111111111111111","type":"video"}}},"occurrences":[{"occurrence_id":"occ-a","shot_id":"chapter-shot","shot_revision_id":"shot-1","placement":{"start_ms":8000,"track":"picture"},"duration_ms":10000,"source_offset":0,"speed":1,"track":"picture","unknown":{"literal":"chapter-shot"}},{"occurrence_id":"occ-b","shot_id":"chapter-shot","shot_revision_id":"shot-1","placement":{"start_ms":10000,"track":"picture"},"duration_ms":10000,"source_offset":0,"speed":1,"track":"picture","unknown":{"literal":"chapter-shot"}}],"name":"Renamed Film","unknown":{"opaque":["parent-1",null]}},"content_digest":"sha256:86c97a97fb837467f83918e31ce27d76c59740c83fec38a22562ce4d213c249b"},"shot_revisions":[{"shot_id":"chapter-shot","revision_id":"shot-1","internal_timeline_revision_id":"internal-1","payload":{"name":"Chapter One","internal_timeline_revision_id":"internal-1","items":[{"item_id":"item-1","media_id":"sha256:1111111111111111111111111111111111111111111111111111111111111111","metadata":{"opaque_literal":"item-1"}}],"text_bindings":[{"slot":"narration","text":"A chapter"}],"metadata":{"chapter":true},"unknown":{"keep":null}},"content_digest":"sha256:f700f1f65d6111e008f10de355a74ab6b41b766f4ff4070bd62f97206a3f0775"}],"internal_timeline_revisions":[{"revision_id":"internal-1","timeline_id":"chapter-1","payload":{"tracks":[{"id":"picture","kind":"visual"}],"clips":[{"id":"clip-a","track":"picture","asset":"picture","clipType":"media","at":1,"hold":4,"app":{"org.example":{"literal":"clip-a","clear":null}},"from":2,"to":6,"speed":2},{"id":"clip-b","track":"picture","asset":"picture","clipType":"media","at":5,"hold":2,"app":{"org.example":{"literal":"clip-a","clear":null}}}],"output":{"fps":{"numerator":30000,"denominator":1001}},"opaque":{"timestamp":"authored timestamp","v":[null,false,0]},"registry":{"assets":{"picture":{"media_id":"sha256:1111111111111111111111111111111111111111111111111111111111111111","type":"video"}}},"unknown":[1,2]},"content_digest":"sha256:0693a443fc594c55a609396fbb0f92114b7a6bf1d880230818a76226c9648622"}],"dependency_manifest":{"shots":[{"shot_id":"chapter-shot","revision_id":"shot-1","internal_timeline_revision_id":"internal-1","content_digest":"sha256:f700f1f65d6111e008f10de355a74ab6b41b766f4ff4070bd62f97206a3f0775"}],"internal_timelines":[{"timeline_id":"chapter-1","revision_id":"internal-1","content_digest":"sha256:0693a443fc594c55a609396fbb0f92114b7a6bf1d880230818a76226c9648622"}],"media":[{"media_id":"sha256:1111111111111111111111111111111111111111111111111111111111111111","content_digest":"sha256:1111111111111111111111111111111111111111111111111111111111111111"}],"documents":[]}}}
  },
] as unknown as AuthoredBundle[];
const goldens = [
  {"name":"completion-image-anchor","approval":{"autoApprove":true,"owner":"occurrence:occ-a","ownership":"occurrence","clipId":"placed","mode":"completion","anchor":"clip-a","preferredTrack":null,"fallbackAt":null,"fallbackTrack":null},"media":{"asset":"reserved-new","generation_id":"generation-new","variant_id":"variant-new","object_id":"sha256:2222222222222222222222222222222222222222222222222222222222222222","catalog_digest":"sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"},"verified":{"selection":{"asset":"reserved-new","generation_id":"generation-new","variant_id":"variant-new","object_id":"sha256:2222222222222222222222222222222222222222222222222222222222222222","catalog_digest":"sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"},"media_type":"image/fixture","size":123},"capture":{"owner":"occurrence:occ-a","clip":"placed","kind":"image","media":{"asset":"reserved-new","generation_id":"generation-new","variant_id":"variant-new","object_id":"sha256:2222222222222222222222222222222222222222222222222222222222222222","catalog_digest":"sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"},"anchor":{"id":"clip-a","state":"present"},"resolution":"anchor-after","lane":"picture","consumed":["clip-a"],"fps":{"numerator":30000,"denominator":1001},"start_frame":330,"on":11.011,"seconds":5},"commands":"69f80c68b553835f2a689db01ef7c22759960e0585b178100e1ed1f1a0da7341","records":"e81658b6c48156030b1467ffbd21393d589d1d99c182d99d86d9bde9f50bd0d9","after":"a3930d0845f76b8ae97260af83927299e90a7bdd9442c34ed232918e3536d679"},
  {"name":"completion-image-absent","approval":{"autoApprove":true,"owner":"occurrence:occ-a","ownership":"occurrence","clipId":"placed","mode":"completion","anchor":"gone","preferredTrack":null,"fallbackAt":null,"fallbackTrack":null},"media":{"asset":"reserved-new","generation_id":"generation-new","variant_id":"variant-new","object_id":"sha256:2222222222222222222222222222222222222222222222222222222222222222","catalog_digest":"sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"},"verified":{"selection":{"asset":"reserved-new","generation_id":"generation-new","variant_id":"variant-new","object_id":"sha256:2222222222222222222222222222222222222222222222222222222222222222","catalog_digest":"sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"},"media_type":"image/fixture","size":123},"capture":{"owner":"occurrence:occ-a","clip":"placed","kind":"image","media":{"asset":"reserved-new","generation_id":"generation-new","variant_id":"variant-new","object_id":"sha256:2222222222222222222222222222222222222222222222222222222222222222","catalog_digest":"sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"},"anchor":{"id":"gone","state":"absent"},"resolution":"lane-end","lane":"picture","consumed":["clip-a","clip-b"],"fps":{"numerator":30000,"denominator":1001},"start_frame":450,"on":15.015,"seconds":5},"commands":"ff667b82067a105b5dc582acf9064e2fb9c12bc8352e46868e2a167e8f4c16e5","records":"0a238b23958bd915fb251caea76df74edb311bda231af33b15b0584b327f3bc3","after":"21c6c2e30488ed9bda1528c965c22ffe597a5de763d729c7030e44e2dcd64e11"},
  {"name":"completion-video-anchor","approval":{"autoApprove":true,"owner":"occurrence:occ-a","ownership":"occurrence","clipId":"placed","mode":"completion","anchor":"clip-a","preferredTrack":null,"fallbackAt":null,"fallbackTrack":null},"media":{"asset":"reserved-new","generation_id":"generation-new","variant_id":"variant-new","object_id":"sha256:2222222222222222222222222222222222222222222222222222222222222222","catalog_digest":"sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"},"verified":{"selection":{"asset":"reserved-new","generation_id":"generation-new","variant_id":"variant-new","object_id":"sha256:2222222222222222222222222222222222222222222222222222222222222222","catalog_digest":"sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"},"media_type":"video/fixture","size":123,"duration_seconds":6},"capture":{"owner":"occurrence:occ-a","clip":"placed","kind":"video","media":{"asset":"reserved-new","generation_id":"generation-new","variant_id":"variant-new","object_id":"sha256:2222222222222222222222222222222222222222222222222222222222222222","catalog_digest":"sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"},"anchor":{"id":"clip-a","state":"present"},"resolution":"anchor-after","lane":"picture","consumed":["clip-a"],"fps":{"numerator":30000,"denominator":1001},"start_frame":330,"on":11.011,"seconds":5},"commands":"7ccc2af0ae48c71e8a117d1936de9cc235fbeec25ca0a5eaac03250c6484fcec","records":"23274d82f8b10e56e700d6d78804b993af0abb4334154aca86acb57b4a009907","after":"9acc036dd83d382aeece66f30dabdf0d786e9f71fc0f02553456b3eab35538ef"},
  {"name":"completion-video-absent","approval":{"autoApprove":true,"owner":"occurrence:occ-a","ownership":"occurrence","clipId":"placed","mode":"completion","anchor":null,"preferredTrack":null,"fallbackAt":null,"fallbackTrack":null},"media":{"asset":"reserved-new","generation_id":"generation-new","variant_id":"variant-new","object_id":"sha256:2222222222222222222222222222222222222222222222222222222222222222","catalog_digest":"sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"},"verified":{"selection":{"asset":"reserved-new","generation_id":"generation-new","variant_id":"variant-new","object_id":"sha256:2222222222222222222222222222222222222222222222222222222222222222","catalog_digest":"sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"},"media_type":"video/fixture","size":123,"duration_seconds":6},"capture":{"owner":"occurrence:occ-a","clip":"placed","kind":"video","media":{"asset":"reserved-new","generation_id":"generation-new","variant_id":"variant-new","object_id":"sha256:2222222222222222222222222222222222222222222222222222222222222222","catalog_digest":"sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"},"anchor":{"id":null,"state":"absent"},"resolution":"lane-end","lane":"picture","consumed":["clip-a","clip-b"],"fps":{"numerator":30000,"denominator":1001},"start_frame":450,"on":15.015,"seconds":5},"commands":"4698ab6b8289658e424b81edfbb3311822284929d08cb999704c3288a5abfd08","records":"544275cc52b9e866ff58f5e3b05d723020505fc31711fa3561b2ad1a58644544","after":"60d617a3230ac2cd379331f33b585dba3c6b78778f82a4b562fa58b15d6211e2"},
  {"name":"shared-image-append","approval":{"autoApprove":true,"owner":"occurrence:occ-a","ownership":"occurrence","clipId":"placed","mode":"shared","anchor":null,"frame":null},"media":{"asset":"reserved-new","generation_id":"generation-new","variant_id":"variant-new","object_id":"sha256:2222222222222222222222222222222222222222222222222222222222222222","catalog_digest":"sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"},"verified":{"selection":{"asset":"reserved-new","generation_id":"generation-new","variant_id":"variant-new","object_id":"sha256:2222222222222222222222222222222222222222222222222222222222222222","catalog_digest":"sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"},"media_type":"image/fixture","size":123},"capture":{"owner":"occurrence:occ-a","clip":"placed","kind":"image","media":{"asset":"reserved-new","generation_id":"generation-new","variant_id":"variant-new","object_id":"sha256:2222222222222222222222222222222222222222222222222222222222222222","catalog_digest":"sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"},"anchor":{"id":null,"state":"absent"},"lane":"picture","consumed":["clip-a","clip-b","clip-c"],"fps":{"numerator":30000,"denominator":1001},"resolution":"append","extent_frame":510,"start_frame":510,"on":17.017,"seconds":4},"commands":"22098f30c5cb572c968e624c52499560f86476a13062dccf7ff0a8ca8bc8e91c","records":"b8cefded1691748cc7a9796439aeaccb7d61efa48e96b942dd5c0f1fd55909eb","after":"4d7a9df050d0e4669be4c93fd4d71744936cd57a2fd61039c6d8ca1b0c6d0687"},
  {"name":"shared-video-append","approval":{"autoApprove":true,"owner":"occurrence:occ-a","ownership":"occurrence","clipId":"placed","mode":"shared","anchor":null,"frame":null},"media":{"asset":"reserved-new","generation_id":"generation-new","variant_id":"variant-new","object_id":"sha256:2222222222222222222222222222222222222222222222222222222222222222","catalog_digest":"sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"},"verified":{"selection":{"asset":"reserved-new","generation_id":"generation-new","variant_id":"variant-new","object_id":"sha256:2222222222222222222222222222222222222222222222222222222222222222","catalog_digest":"sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"},"media_type":"video/fixture","size":123,"duration_seconds":6},"capture":{"owner":"occurrence:occ-a","clip":"placed","kind":"video","media":{"asset":"reserved-new","generation_id":"generation-new","variant_id":"variant-new","object_id":"sha256:2222222222222222222222222222222222222222222222222222222222222222","catalog_digest":"sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"},"anchor":{"id":null,"state":"absent"},"lane":"picture","consumed":["clip-a","clip-b","clip-c"],"fps":{"numerator":30000,"denominator":1001},"resolution":"append","extent_frame":510,"start_frame":510,"on":17.017,"seconds":4},"commands":"28d1c2e4060c407e57fb6adecb211e79ee3be82df66cc0996bca6a2356954fed","records":"4cea2a9c2dc95f4b440d84f4cdbb76b5b7c2dab4c229d525e7aa3fab1da5e63e","after":"71c21d6fb561a546a3184df2c96abe331e0621bf0e1ee145c4a791842e8215eb"},
  {"name":"shared-image-shift","approval":{"autoApprove":true,"owner":"occurrence:occ-a","ownership":"occurrence","clipId":"placed","mode":"shared","anchor":null,"frame":390},"media":{"asset":"reserved-new","generation_id":"generation-new","variant_id":"variant-new","object_id":"sha256:2222222222222222222222222222222222222222222222222222222222222222","catalog_digest":"sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"},"verified":{"selection":{"asset":"reserved-new","generation_id":"generation-new","variant_id":"variant-new","object_id":"sha256:2222222222222222222222222222222222222222222222222222222222222222","catalog_digest":"sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"},"media_type":"image/fixture","size":123},"capture":{"owner":"occurrence:occ-a","clip":"placed","kind":"image","media":{"asset":"reserved-new","generation_id":"generation-new","variant_id":"variant-new","object_id":"sha256:2222222222222222222222222222222222222222222222222222222222222222","catalog_digest":"sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"},"anchor":{"id":null,"state":"absent"},"lane":"picture","consumed":["clip-a","clip-b","clip-c"],"fps":{"numerator":30000,"denominator":1001},"resolution":"explicit","requested_frame":390,"skipped":[390],"start_frame":391,"on":13.046366666666666,"seconds":4},"commands":"65d0df81240dc0e9dc5f2316c49ee890dc9446c7f1b44dc75e90d6a98d7d8fdc","records":"968c0bc669d7843b4b90345858669491c24fae3a9ec0d47c2b3ffafb2433b7f6","after":"96f1fda35b9fa6a6b0bdd838c4c08260c89761dd9e68709907d81aa478ed3423"},
  {"name":"shared-video-overlay-anchor","approval":{"autoApprove":true,"owner":"occurrence:occ-a","ownership":"occurrence","clipId":"placed","mode":"shared","anchor":"clip-c","frame":null},"media":{"asset":"reserved-new","generation_id":"generation-new","variant_id":"variant-new","object_id":"sha256:2222222222222222222222222222222222222222222222222222222222222222","catalog_digest":"sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"},"verified":{"selection":{"asset":"reserved-new","generation_id":"generation-new","variant_id":"variant-new","object_id":"sha256:2222222222222222222222222222222222222222222222222222222222222222","catalog_digest":"sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"},"media_type":"video/fixture","size":123,"duration_seconds":6},"capture":{"owner":"occurrence:occ-a","clip":"placed","kind":"video","media":{"asset":"reserved-new","generation_id":"generation-new","variant_id":"variant-new","object_id":"sha256:2222222222222222222222222222222222222222222222222222222222222222","catalog_digest":"sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"},"anchor":{"id":"clip-c","state":"present"},"lane":"overlay","consumed":["clip-a","clip-b","clip-c"],"fps":{"numerator":30000,"denominator":1001},"resolution":"append","extent_frame":510,"start_frame":510,"on":17.017,"seconds":4},"commands":"9e2bfb520835e69978adeff9d058db6e076b565db29c38908f8b69cebe1aed5c","records":"2d2eb1e3f428014cd3373f80bebee7c95c57c38949fa16f0454dcce45c8bfbbd","after":"89d6b425219c0778be0a4582ad1b1764ab2609b6f5ba9e002344f1e2e78c1362"},
  {"name":"image-saved","approval":{"autoApprove":true,"owner":"occurrence:occ-a","ownership":"occurrence","clipId":"placed","mode":"completion","anchor":"gone","preferredTrack":null,"fallbackAt":22.25,"fallbackTrack":"overlay"},"media":{"asset":"reserved-new","generation_id":"generation-new","variant_id":"variant-new","object_id":"sha256:2222222222222222222222222222222222222222222222222222222222222222","catalog_digest":"sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"},"verified":{"selection":{"asset":"reserved-new","generation_id":"generation-new","variant_id":"variant-new","object_id":"sha256:2222222222222222222222222222222222222222222222222222222222222222","catalog_digest":"sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"},"media_type":"image/fixture","size":123},"capture":{"owner":"occurrence:occ-a","clip":"placed","kind":"image","media":{"asset":"reserved-new","generation_id":"generation-new","variant_id":"variant-new","object_id":"sha256:2222222222222222222222222222222222222222222222222222222222222222","catalog_digest":"sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"},"anchor":{"id":"gone","state":"absent"},"resolution":"fallback-at","lane":"overlay","consumed":[],"fps":{"numerator":30000,"denominator":1001},"start_frame":667,"on":22.255566666666667,"seconds":5},"commands":"4f65517a6bf8c4bbacc6c1d73dc123dac150e28aa5d8555733a4f4c7d4e3c091","records":"6d5c96d653c8c5a732bacbb28e76e846064cce0e09f1a8c64a5210ed97b1a665","after":"9d043bac826ab518dc3fe92a773268a594e66895fad410695084a7301672186d"},
  {"name":"image-preferred","approval":{"autoApprove":true,"owner":"occurrence:occ-a","ownership":"occurrence","clipId":"placed","mode":"completion","anchor":"clip-a","preferredTrack":"overlay","fallbackAt":22.25,"fallbackTrack":"picture"},"media":{"asset":"reserved-new","generation_id":"generation-new","variant_id":"variant-new","object_id":"sha256:2222222222222222222222222222222222222222222222222222222222222222","catalog_digest":"sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"},"verified":{"selection":{"asset":"reserved-new","generation_id":"generation-new","variant_id":"variant-new","object_id":"sha256:2222222222222222222222222222222222222222222222222222222222222222","catalog_digest":"sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"},"media_type":"image/fixture","size":123},"capture":{"owner":"occurrence:occ-a","clip":"placed","kind":"image","media":{"asset":"reserved-new","generation_id":"generation-new","variant_id":"variant-new","object_id":"sha256:2222222222222222222222222222222222222222222222222222222222222222","catalog_digest":"sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"},"anchor":{"id":"clip-a","state":"present"},"resolution":"anchor-after","lane":"overlay","consumed":["clip-a"],"fps":{"numerator":30000,"denominator":1001},"start_frame":330,"on":11.011,"seconds":5},"commands":"b9b1b18ae726695410d59ebe61c171b4c80947d46e6e4294f4e0f6535101d6a1","records":"a5f2ae109417dfe2e8b24585ef0358519825d3fa31d250c85b3fd74a7444a8b4","after":"88ca5ae1430a9c8d42861e73e7988e42f6916c96f41c4e9f12c87f04593b5d4a"},
  {"name":"video-saved","approval":{"autoApprove":true,"owner":"occurrence:occ-a","ownership":"occurrence","clipId":"placed","mode":"completion","anchor":"gone","preferredTrack":null,"fallbackAt":22.25,"fallbackTrack":"overlay"},"media":{"asset":"reserved-new","generation_id":"generation-new","variant_id":"variant-new","object_id":"sha256:2222222222222222222222222222222222222222222222222222222222222222","catalog_digest":"sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"},"verified":{"selection":{"asset":"reserved-new","generation_id":"generation-new","variant_id":"variant-new","object_id":"sha256:2222222222222222222222222222222222222222222222222222222222222222","catalog_digest":"sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"},"media_type":"video/fixture","size":123,"duration_seconds":6},"capture":{"owner":"occurrence:occ-a","clip":"placed","kind":"video","media":{"asset":"reserved-new","generation_id":"generation-new","variant_id":"variant-new","object_id":"sha256:2222222222222222222222222222222222222222222222222222222222222222","catalog_digest":"sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"},"anchor":{"id":"gone","state":"absent"},"resolution":"fallback-at","lane":"overlay","consumed":[],"fps":{"numerator":30000,"denominator":1001},"start_frame":667,"on":22.255566666666667,"seconds":5},"commands":"eae04a8b37ea8b7ac9903b6b3530b22e25cd47c8e4a5a2eec98066d44ea993ba","records":"1d7ecc6548e38b39bfe9097c3212b79a267824bd075309fbcb6b484cb03874e1","after":"02a47edf5ac0df6598891d610a29f30ca93944e0ef57dd9760e59e9f03be37e9"},
  {"name":"video-preferred","approval":{"autoApprove":true,"owner":"occurrence:occ-a","ownership":"occurrence","clipId":"placed","mode":"completion","anchor":"clip-a","preferredTrack":"overlay","fallbackAt":22.25,"fallbackTrack":"picture"},"media":{"asset":"reserved-new","g…40918 tokens truncated…it env.reserve(box);
      const [locked] = await env.requester().recover();
      expect(locked).toMatchObject({ status: 'retry', message: 'Outbox is already claimed' });
      env.state.identity.actorId = 'another-actor';
      await expect(env.requester().resume(box)).rejects.toThrow('identity changed');
      expect(await env.requester().recover()).toEqual([]);
      env.state.identity = { realmId: 'other-realm', actorId: scope.actorId };
      expect(await env.requester().recover()).toEqual([]);
    });
    expect(env.calls).toEqual([]);
  });

  it('keeps missing capture and unbound owners visible for manual placement without auto activation', async () => {
    const env = environment();
    await env.storage().create(scope, async (box) => {
      expect((await env.requester(false).request(box, 'request', input)).status).toBe('manual');
      expect((await box.read()).intents).toEqual([]);
    });
    await env.storage().create(scope, async () => {});
    const results = await env.requester(false).recover();
    expect(results).toHaveLength(2);
    expect(results.map((v) => v.status)).toEqual(['manual', 'manual']);
    expect(env.capture).not.toHaveBeenCalled();
    expect(env.transmit).not.toHaveBeenCalled();
  });

  it.each(['approval', 'project', 'bytes', 'selector', 'unsaved'] as const)('refuses %s before task submission', async (failure) => {
    const env = environment();
    await env.storage().create(scope, async (box) => {
      const changed = structuredClone(input);
      if (failure === 'approval') Object.assign(changed, { autoApprove: false });
      if (failure === 'project') changed.request = preparePlacementTask({ ...JSON.parse(prepared.body), project: 'wrong-project' }, prepared.key);
      if (failure === 'bytes') changed.request.body += '\n';
      if (failure === 'selector') changed.output.variant_key = 'unapproved';
      if (failure === 'unsaved') await box.append({ fixture: 'unsaved' }, { head });
      await expect(env.requester().request(box, 'request', changed)).rejects.toThrow();
      expect(env.calls).toEqual([]);
    });
  });
});


describe('requester independent review counterexamples', () => {
  it('review fences task admission after the original owner claim is released and reclaimed', async () => {
    const env = environment();
    const started = deferred();
    const resumeIdentity = deferred();
    let checks = 0;
    const requester = createPlacementRequester({ client: env.client, outboxes: env.storage(),
      getRecoverableIdentity: async () => {
        checks += 1;
        // resume checks identity, then advance reads the owner and checks identity again.
        if (checks === 2) { started.resolve(); await resumeIdentity.promise; }
        return { ...env.state.identity };
      }, capture: env.capture, build: env.build, transmit: env.transmit });
    let late!: Promise<unknown>;
    let ownerId!: string;
    await env.storage().create(scope, async (box, id) => {
      ownerId = id;
      await env.reserve(box);
      late = requester.resume(box);
      await started.promise;
    });
    // A new legitimate claim now owns the same continuation; the old claim is inactive.
    await env.storage().recover(scope, ownerId, async (box) => {
      expect((await box.read()).generation).toBe(2);
      resumeIdentity.resolve();
      await late;
      const posted = env.calls.filter((call) => call.method === 'POST');
      const record = await box.read();
      console.info('REVIEW_STALE_CLAIM', JSON.stringify({ posted, generation: record.generation,
        locator: record.placementContinuations![0].taskLocator ?? null }));
      expect(posted).toEqual([]);
    });
  });

  it('review fences a commit acknowledgement when actor identity changes during transmission', async () => {
    const env = environment();
    const sent = deferred();
    const acknowledge = deferred();
    env.transmit.mockImplementationOnce(async () => {
      sent.resolve();
      await acknowledge.promise;
      return acceptance('A');
    });
    await env.storage().create(scope, async (box) => {
      const advancing = env.requester().request(box, 'request', input);
      await sent.promise;
      env.state.identity.actorId = 'different-actor';
      acknowledge.resolve();
      const result = await advancing;
      const record = await box.read();
      console.info('REVIEW_CHANGED_ACTOR_ACK', JSON.stringify({ status: result.status,
        actor: env.state.identity.actorId, intents: record.intents.length, pending: !!record.pending,
        accepted: record.placementContinuations![0].placement?.accepted ?? null }));
      expect(record.placementContinuations![0].placement?.accepted).toBeUndefined();
      expect(record.pending?.request).toBeDefined();
      expect(record.intents).toHaveLength(1);
    });
  });
});

describe('requester async lifecycle recovery', () => {
  it.each(['actorId', 'realmId'] as const)('retains capture success/refusal across %s changes and recovers the original approval', async (field) => {
    for (const refused of [false, true]) {
      const env = environment();
      const started = deferred();
      const complete = deferred();
      env.capture.mockImplementationOnce(async () => {
        started.resolve();
        await complete.promise;
        if (refused) throw new Error('late capture refusal');
        return { captured: 'before identity changed' };
      });
      let ownerId!: string;
      await env.storage().create(scope, async (box, id) => {
        ownerId = id;
        const advancing = env.requester().request(box, 'request', input);
        await started.promise;
        const original = await box.read();
        env.state.identity[field] = 'different';
        complete.resolve();
        expect((await advancing).status).toBe('retry');
        expect(await box.read()).toEqual(original);
        expect(original.placementContinuations![0]).toMatchObject({ input, mediaPin: pin });
        expect(original.intents).toEqual([]);
        expect(env.transmit).not.toHaveBeenCalled();
      });
      env.state.identity[field] = scope[field];
      expect(await env.requester().recover()).toMatchObject([{ ownerId, status: 'accepted' }]);
      expect(env.capture).toHaveBeenCalledTimes(2);
      expect(env.capture.mock.calls[1][0]).toMatchObject({ input, mediaPin: pin });
      expect(env.calls.filter((call) => call.method === 'POST')).toEqual([prepared]);
    }
  });

  it.each(['actorId', 'realmId'] as const)('keeps exact uncertain commit bytes/key for %s changes across every transmit outcome', async (field) => {
    for (const outcome of ['accepted', 'rejected', 'error'] as const) {
      const env = environment();
      const started = deferred();
      const complete = deferred();
      env.transmit.mockImplementationOnce(async () => {
        started.resolve();
        await complete.promise;
        if (outcome === 'error') throw new Error('late transport refusal');
        return outcome === 'accepted' ? acceptance('A') : { kind: 'rejected', error: { reason: 'late conflict' } };
      });
      await env.storage().create(scope, async (box) => {
        const advancing = env.requester().request(box, 'request', input);
        await started.promise;
        const original = await box.read();
        env.state.identity[field] = 'different';
        complete.resolve();
        expect((await advancing).status).toBe('retry');
        const retained = await box.read();
        expect(retained.pending?.request).toEqual(original.pending!.request);
        expect(retained.pending?.outcome?.kind).toBe('retry');
        expect(retained.intents).toEqual(original.intents);
        expect(retained.placementContinuations).toEqual(original.placementContinuations);
        expect(retained.placementContinuations![0].input).toEqual(input);
        expect(retained.placementContinuations![0].placement?.accepted).toBeUndefined();
        env.state.identity[field] = scope[field];
        expect(await env.requester().resume(box)).toMatchObject([{ status: 'accepted' }]);
        expect(env.transmit.mock.calls.map(([request]) => request)).toEqual([original.pending!.request, original.pending!.request]);
        expect(env.build).toHaveBeenCalledTimes(1);
        expect(env.capture).toHaveBeenCalledTimes(1);
        const accepted = await box.read();
        expect(await env.requester().resume(box)).toMatchObject([{ status: 'accepted' }]);
        expect(await box.read()).toEqual(accepted);
        expect(env.transmit).toHaveBeenCalledTimes(2);
      });
    }
  });

  it.each(['capture', 'transmit'] as const)('fences late %s after release or loss of the persisted generation', async (stage) => {
    for (const loss of ['release', 'supersede'] as const) {
      const env = environment();
      const started = deferred();
      const complete = deferred();
      let late!: Promise<{ status: string }>;
      let ownerId!: string;
      let original!: Awaited<ReturnType<ClaimedOutbox['read']>>;
      if (stage === 'capture') env.capture.mockImplementationOnce(async () => {
        started.resolve(); await complete.promise;
        return { obsolete: 'capture' };
      });
      else env.transmit.mockImplementationOnce(async () => {
        started.resolve(); await complete.promise;
        return acceptance('obsolete');
      });
      const reconcile = async (box: ClaimedOutbox) => {
        expect((await box.read()).generation).toBe(2);
        if (stage === 'transmit') {
          // A current generation accepts first; the old ACK must not overwrite it.
          expect(await env.requester().resume(box)).toMatchObject([{ status: 'accepted' }]);
          const accepted = await box.read();
          expect(accepted.placementContinuations![0].placement?.accepted?.head).toEqual({ revisionId: 'RA', publicationId: 'PA' });
          complete.resolve();
          expect((await late).status).toBe('retry');
          expect(await box.read()).toEqual(accepted);
          expect(env.transmit.mock.calls.map(([request]) => request)).toEqual([original.pending!.request, original.pending!.request]);
        } else {
          complete.resolve();
          expect((await late).status).toBe('retry');
          const retained = await box.read();
          expect(retained).toEqual({ ...original, generation: 2 });
          expect(retained.placementContinuations![0].conflict).toBeUndefined();
          expect(await env.requester().resume(box)).toMatchObject([{ status: 'accepted' }]);
          expect(env.capture.mock.calls[1][0]).toMatchObject({ input, mediaPin: pin });
        }
        expect(env.calls.filter((call) => call.method === 'POST')).toEqual([prepared]);
        const accepted = await box.read();
        expect(await env.requester().resume(box)).toMatchObject([{ status: 'accepted' }]);
        expect(await box.read()).toEqual(accepted);
      };
      await env.storage().create(scope, async (box, id) => {
        ownerId = id;
        late = env.requester().request(box, 'request', input);
        await started.promise;
        original = await box.read();
        if (loss === 'supersede') {
          // Simulate loss of browser exclusion: persisted generation still fences the active old callback.
          const competing = createCommitOutbox({ indexedDB: env.factory, exclusiveLock: async (_name, work) => work() });
          await competing.recover(scope, ownerId, reconcile);
        }
      });
      if (loss === 'release') await env.storage().recover(scope, ownerId, reconcile);
    }
  });

  it.each(['capture', 'transmit', 'refusal'] as const)('rechecks a released generation after awaited %s identity', async (stage) => {
    const env = environment();
    const checking = deferred();
    const complete = deferred();
    let pause = false;
    let ownerId!: string;
    let late!: Promise<unknown>;
    let original!: Awaited<ReturnType<ClaimedOutbox['read']>>;
    const requester = createPlacementRequester({ client: env.client, outboxes: env.storage(),
      getRecoverableIdentity: async () => {
        if (pause) { pause = false; checking.resolve(); await complete.promise; }
        return { ...env.state.identity };
      }, capture: env.capture, build: env.build, transmit: env.transmit });
    if (stage === 'capture') {
      const capture = env.capture.getMockImplementation()!;
      env.capture.mockImplementationOnce(async (saved) => { pause = true; return capture(saved); });
    } else if (stage === 'transmit') env.build.mockImplementationOnce((intent) => {
      pause = true;
      return { method: 'POST', path: `/v1/projects/${scope.projectId}/timelines/${scope.timelineId}/commit`, body: intent.payload };
    });
    else {
      env.state.admissionFailure = 403;
      const admit = env.client.admitTask.bind(env.client);
      vi.spyOn(env.client, 'admitTask').mockImplementationOnce(async (...args) => {
        try { return await admit(...args); } finally { pause = true; }
      });
    }
    await env.storage().create(scope, async (box, id) => {
      ownerId = id;
      late = requester.request(box, 'request', input);
      await checking.promise;
      original = await box.read();
    });
    await env.storage().recover(scope, ownerId, async (box) => {
      complete.resolve();
      await late;
      expect(await box.read()).toEqual({ ...original, generation: 2 });
      expect(env.transmit).not.toHaveBeenCalled();
      expect((await box.read()).placementContinuations![0].conflict).toBeUndefined();
      env.state.admissionFailure = 0;
      expect(await requester.resume(box)).toMatchObject([{ status: 'accepted' }]);
    });
  });

  it('keeps the first genuine refusal through duplicate recovery without rearming admission', async () => {
    const env = environment();
    env.state.readFailure = 403;
    await env.storage().create(scope, async (box) => {
      expect((await env.requester().request(box, 'request', input)).status).toBe('conflict');
      const original = await box.read();
      const conflict = original.placementContinuations![0].conflict;
      expect(conflict).toEqual({ reason: 'placement_refused', message: 'task_read_failed: task read failed' });
      expect(await box.recordPlacementConflict('request', { reason: 'later refusal' })).toEqual(original.placementContinuations![0]);
      const calls = env.calls.length;
      env.state.readFailure = 404;
      expect(await env.requester().resume(box)).toMatchObject([{ status: 'conflict' }]);
      expect(await box.read()).toEqual(original);
      expect(env.calls).toHaveLength(calls);
      expect(env.capture).not.toHaveBeenCalled();
      expect(env.transmit).not.toHaveBeenCalled();
    });
  });
});

describe('requester awaited identity refusals', () => {
  it.each(['actorId', 'realmId'] as const)('does not retain a capture/API refusal under a changed %s while identity is pending', async (field) => {
    for (const stage of ['capture', 'admission'] as const) {
      const env = environment();
      const checking = deferred();
      const complete = deferred();
      let pause = false;
      const requester = createPlacementRequester({ client: env.client, outboxes: env.storage(),
        getRecoverableIdentity: async () => {
          if (pause) { pause = false; checking.resolve(); await complete.promise; }
          return { ...env.state.identity };
        }, capture: env.capture, build: env.build, transmit: env.transmit });
      if (stage === 'capture') env.capture.mockImplementationOnce(async () => {
        pause = true;
        throw new Error('capture refused under original identity');
      });
      else {
        env.state.admissionFailure = 403;
        const admit = env.client.admitTask.bind(env.client);
        vi.spyOn(env.client, 'admitTask').mockImplementationOnce(async (...args) => {
          try { return await admit(...args); } finally { pause = true; }
        });
      }
      await env.storage().create(scope, async (box) => {
        const advancing = requester.request(box, 'request', input);
        await checking.promise;
        const original = await box.read();
        env.state.identity[field] = 'different';
        complete.resolve();
        expect((await advancing).status).toBe('retry');
        expect(await box.read()).toEqual(original);
        env.state.identity[field] = scope[field];
        env.state.admissionFailure = 0;
        expect(await requester.resume(box)).toMatchObject([{ status: 'accepted' }]);
        expect(env.calls.filter((call) => call.method === 'POST')).toEqual(stage === 'admission' ? [prepared, prepared] : [prepared]);
      });
    }
  });

  it('keeps an asynchronous identity-service refusal retryable even when authentication recovers immediately', async () => {
    const env = environment();
    const checking = deferred();
    const complete = deferred();
    let checks = 0;
    const requester = createPlacementRequester({ client: env.client, outboxes: env.storage(),
      getRecoverableIdentity: async () => {
        checks += 1;
        if (checks === 3) {
          checking.resolve();
          await complete.promise;
          // Use the actual generated API error: identity-service failure is not task rejection.
          const { ApiError } = await import('@/integrations/runtime/generated.ts');
          throw new ApiError(403, 'identity_unavailable', 'temporary authentication interruption');
        }
        return { ...env.state.identity };
      }, capture: env.capture, build: env.build, transmit: env.transmit });
    await env.storage().create(scope, async (box) => {
      const advancing = requester.request(box, 'request', input);
      await checking.promise;
      const original = await box.read();
      complete.resolve();
      expect((await advancing).status).toBe('retry');
      expect(await box.read()).toEqual(original);
      expect(env.calls).toEqual([]);
      expect(await requester.resume(box)).toMatchObject([{ status: 'accepted' }]);
      expect(env.calls.filter((call) => call.method === 'POST')).toEqual([prepared]);
    });
  });
});

describe('requester admission generation recovery', () => {
  it('admits the exact original approval only from the reclaimed generation', async () => {
    const env = environment();
    const checking = deferred();
    const complete = deferred();
    let checks = 0;
    const requester = createPlacementRequester({ client: env.client, outboxes: env.storage(),
      getRecoverableIdentity: async () => {
        checks += 1;
        if (checks === 2) { checking.resolve(); await complete.promise; }
        return { ...env.state.identity };
      }, capture: env.capture, build: env.build, transmit: env.transmit });
    let ownerId!: string;
    let late!: Promise<unknown>;
    await env.storage().create(scope, async (box, id) => {
      ownerId = id;
      await env.reserve(box);
      late = requester.resume(box);
      await checking.promise;
    });
    await env.storage().recover(scope, ownerId, async (box) => {
      const original = await box.read();
      complete.resolve();
      await late;
      expect(env.calls).toEqual([]);
      expect(await box.read()).toEqual(original);
      expect(await requester.resume(box)).toMatchObject([{ status: 'accepted' }]);
      expect(env.calls.filter((call) => call.method === 'POST')).toEqual([prepared]);
      expect(env.capture.mock.calls[0][0]).toMatchObject({ input, mediaPin: pin });
      expect((await box.read()).generation).toBe(2);
    });
  });
});

describe('composed requester fences with dependent recovery', () => {
  const payloads = ['B', 'C', 'timeline.inverse'].map((op) => ({ op,
    guards: { original: op }, bindings: ['original-anchor'], createdIds: [`allocated-${op}`] }));

  async function queueDependents(box: ClaimedOutbox) {
    const original = await box.read();
    let previous = original.pending!.intentId;
    for (const payload of payloads) previous = await box.append(payload, { after: previous });
    return box.read();
  }

  async function recoverChain(env: ReturnType<typeof environment>, ownerId: string,
    saved: Awaited<ReturnType<ClaimedOutbox['read']>>) {
    env.state.identity = { realmId: scope.realmId, actorId: scope.actorId };
    env.build.mockClear();
    let linked!: NonNullable<typeof saved.placementContinuations>[number];
    await env.storage().recover(scope, ownerId, async (box) => {
      const before = await box.read();
      expect(before.pending!.request).toEqual(saved.pending!.request);
      expect(before.intents).toEqual(saved.intents);
      expect(await env.requester().resume(box)).toMatchObject([{ status: 'accepted' }]);
      expect(env.transmit.mock.lastCall![0]).toEqual(saved.pending!.request);
      expect(env.build).not.toHaveBeenCalled();
      const after = await box.read();
      linked = after.placementContinuations![0];
      expect(linked.input).toEqual(input);
      expect(linked.placement?.accepted).toMatchObject({ intentId: saved.pending!.intentId,
        head: { revisionId: 'RA', publicationId: 'PA' } });
      expect(after.intents).toEqual(saved.intents.slice(1).map((intent, index) => index === 0
        ? { ...intent, readyBase: { revisionId: 'RA', publicationId: 'PA' } } : intent));
      expect(after.pending).toBeUndefined();
    });
    let base = { revisionId: 'RA', publicationId: 'PA' };
    const keys = new Set([saved.pending!.request.key]);
    for (const [index, payload] of payloads.entries()) {
      let pending!: OutboxRequest;
      let retained!: Awaited<ReturnType<ClaimedOutbox['read']>>;
      await env.storage().recover(scope, ownerId, async (box) => {
        await box.dispatch(env.build, async (request) => {
          pending = request;
          expect(JSON.parse(request.body)).toEqual({ fixture: payload, base });
          expect(keys.has(request.key)).toBe(false);
          keys.add(request.key);
          throw new Error('dependent ACK lost');
        });
        retained = await box.read();
        expect(retained.intents[0]).toEqual({ ...saved.intents[index + 1], readyBase: base });
        expect(retained.pending!.request).toEqual(pending);
      });
      const outcome = acceptance(payload.op);
      if (outcome.kind !== 'accepted') throw new Error('Expected acceptance fixture');
      await env.storage().recover(scope, ownerId, async (box) => {
        const mustNotBuild = vi.fn(() => { throw new Error('Exact pending retry cannot rebuild'); });
        const after = await box.dispatch(mustNotBuild, async (request) => {
          expect(request).toEqual(pending);
          return outcome;
        });
        expect(mustNotBuild).not.toHaveBeenCalled();
        expect(after.intents).toEqual(retained.intents.slice(1).map((intent, next) => next === 0
          ? { ...intent, readyBase: outcome.head } : intent));
        expect(after.placementContinuations).toEqual([linked]);
        expect(after.pending).toBeUndefined();
        const stable = await box.read();
        expect(await env.requester().resume(box)).toMatchObject([{ status: 'accepted' }]);
        expect(await box.read()).toEqual(stable);
      });
      base = outcome.head;
    }
    expect(env.calls.filter((call) => call.method === 'POST')).toEqual([prepared]);
    expect(await env.requester().recover()).toMatchObject([{ status: 'accepted' }]);
    expect(env.transmit).toHaveBeenCalledTimes(2);
  }

  it.each(['success', 'refusal'] as const)('recovers A/B/C/inverse after late capture %s, actor change and owner release', async (settlement) => {
    const env = environment();
    const started = deferred();
    const complete = deferred();
    env.capture.mockImplementationOnce(async () => {
      started.resolve();
      await complete.promise;
      if (settlement === 'refusal') throw new Error('obsolete semantic refusal');
      return { obsolete: 'capture payload' };
    });
    env.transmit.mockRejectedValueOnce(new Error('A ACK lost'));
    let ownerId!: string;
    let late!: ReturnType<ReturnType<typeof env.requester>['request']>;
    let original!: Awaited<ReturnType<ClaimedOutbox['read']>>;
    await env.storage().create(scope, async (box, id) => {
      ownerId = id;
      late = env.requester().request(box, 'request', input);
      await started.promise;
      original = await box.read();
      env.state.identity.actorId = 'another-actor';
    });
    let saved!: typeof original;
    await env.storage().recover(scope, ownerId, async (box) => {
      complete.resolve();
      expect((await late).status).toBe('retry');
      expect(await box.read()).toEqual({ ...original, generation: 2 });
      expect(original.placementContinuations![0]).toMatchObject({ input, mediaPin: pin });
      expect(original.placementContinuations![0].placement).toBeUndefined();
      expect(original.placementContinuations![0].conflict).toBeUndefined();
      expect(env.transmit).not.toHaveBeenCalled();
      env.state.identity.actorId = scope.actorId;
      expect(await env.requester().resume(box)).toMatchObject([{ status: 'retry' }]);
      saved = await queueDependents(box);
    });
    await recoverChain(env, ownerId, saved);
    expect(env.capture).toHaveBeenCalledTimes(2);
    expect(env.capture.mock.calls[1][0]).toMatchObject({ input, mediaPin: pin });
  });

  it.each(['accepted', 'rejected', 'error'] as const)('retains A/B/C/inverse across late %s ACK, actor change and owner release', async (settlement) => {
    const env = environment();
    const started = deferred();
    const complete = deferred();
    env.transmit.mockImplementationOnce(async () => {
      started.resolve();
      await complete.promise;
      if (settlement === 'error') throw new Error('obsolete transport refusal');
      return settlement === 'accepted' ? acceptance('obsolete')
        : { kind: 'rejected', error: { reason: 'obsolete permanent conflict' } };
    });
    let ownerId!: string;
    let late!: ReturnType<ReturnType<typeof env.requester>['request']>;
    let saved!: Awaited<ReturnType<ClaimedOutbox['read']>>;
    await env.storage().create(scope, async (box, id) => {
      ownerId = id;
      late = env.requester().request(box, 'request', input);
      await started.promise;
      saved = await queueDependents(box);
      env.state.identity.actorId = 'another-actor';
    });
    await env.storage().recover(scope, ownerId, async (box) => {
      complete.resolve();
      expect((await late).status).toBe('retry');
      expect(await box.read()).toEqual({ ...saved, generation: 2 });
      expect(saved.intents.map((intent) => intent.conflict)).toEqual([undefined, undefined, undefined, undefined]);
      expect(saved.intents.slice(1).map((intent) => intent.readyBase)).toEqual([undefined, undefined, undefined]);
      expect(saved.placementContinuations![0].placement?.accepted).toBeUndefined();
    });
    await recoverChain(env, ownerId, saved);
    expect(env.capture).toHaveBeenCalledTimes(1);
  });
});

// The read wrapper only delays delivery of a real successful, generation-checked IDB read.
describe('independent residual fence counterexamples', () => {
  it.each(['actorId', 'realmId'] as const)('does not POST after %s changes during the final authorization read', async (field) => {
    const env = environment();
    const reading = deferred(), complete = deferred();
    let checks = 0;
    let pauseRead = false;
    const dispatchIdentities: unknown[] = [];
    const admit = env.client.admitTask.bind(env.client);
    vi.spyOn(env.client, 'admitTask').mockImplementation(async (...args) => {
      dispatchIdentities.push({ ...env.state.identity });
      return admit(...args);
    });
    const requester = createPlacementRequester({ client: env.client, outboxes: env.storage(),
      getRecoverableIdentity: async () => {
        checks += 1;
        if (checks === 3) pauseRead = true; // resume, advance, then POST authorization
        return { ...env.state.identity };
      }, capture: env.capture, build: env.build, transmit: env.transmit });
    await env.storage().create(scope, async (box) => {
      await env.reserve(box);
      const read = box.read.bind(box);
      vi.spyOn(box, 'read').mockImplementation(async () => {
        const record = await read();
        if (pauseRead) { pauseRead = false; reading.resolve(); await complete.promise; }
        return record;
      });
      const advancing = requester.resume(box);
      await reading.promise;
      env.state.identity = { ...env.state.identity, [field]: 'different' };
      complete.resolve();
      const result = await advancing;
      const retained = await read();
      console.info('RESIDUAL_POST', JSON.stringify({ field, result: result[0].status, dispatchIdentities,
        posted: env.calls.filter((c) => c.method === 'POST'), retained: retained.placementContinuations }));
      // Recovery is possible under the original identity, with exactly the original body/key/IDs.
      env.state.identity = { realmId: scope.realmId, actorId: scope.actorId };
      expect(await requester.resume(box)).toMatchObject([{ status: 'accepted' }]);
      expect(env.calls.filter((c) => c.method === 'POST')).toEqual([prepared]);
      expect(env.capture.mock.calls[0][0]).toMatchObject({ input, mediaPin: pin });
      expect(dispatchIdentities).toEqual([{ realmId: scope.realmId, actorId: scope.actorId }]);
      // Safety expectation: the late old-identity authorization should have prevented this POST.
      expect(env.calls.filter((c) => c.method === 'POST').slice(0, -1)).toEqual([]);
    });
  });

  it.each([{field:'actorId', refusal:false}, {field:'realmId', refusal:false}, {field:'actorId', refusal:true}, {field:'realmId', refusal:true}] as const)('does not change capture storage at $field refusal=$refusal during the post-capture read', async ({field, refusal}) => {
      const env = environment();
      const reading = deferred(), complete = deferred();
      let pauseRead = false, arm = false;
      const capture = env.capture.getMockImplementation()!;
      env.capture.mockImplementationOnce(async (saved) => {
        arm = true;
        if (refusal) throw new Error('original semantic capture refused');
        return capture(saved);
      });
      const requester = createPlacementRequester({ client: env.client, outboxes: env.storage(),
        getRecoverableIdentity: async () => {
          if (arm) { arm = false; pauseRead = true; }
          return { ...env.state.identity };
        }, capture: env.capture, build: env.build, transmit: env.transmit });
      await env.storage().create(scope, async (box) => {
        const read = box.read.bind(box);
        vi.spyOn(box, 'read').mockImplementation(async () => {
          const record = await read();
          if (pauseRead) { pauseRead = false; reading.resolve(); await complete.promise; }
          return record;
        });
        const advancing = requester.request(box, 'request', input);
        await reading.promise;
        const before = await read();
        env.state.identity = { ...env.state.identity, [field]: 'different' };
        complete.resolve();
        const result = await advancing;
        const after = await read();
        console.info('RESIDUAL_CAPTURE', JSON.stringify({ field, refusal, status: result.status,
          before: before.placementContinuations, after: after.placementContinuations, intents: after.intents }));
        expect(env.transmit).not.toHaveBeenCalled();
        expect(after.placementContinuations![0].input).toEqual(input);
        env.state.identity = { realmId: scope.realmId, actorId: scope.actorId };
        if (!refusal) {
          expect(await requester.resume(box)).toMatchObject([{ status: 'accepted' }]);
          expect(env.capture).toHaveBeenCalledTimes(2);
        } else {
          expect(await requester.resume(box)).toMatchObject([{ status: 'accepted' }]);
          expect(env.capture).toHaveBeenCalledTimes(2);
        }
        expect(after.placementContinuations).toEqual(before.placementContinuations);
      });
  });

  it.each([{field:'actorId', kind:'accepted'}, {field:'realmId', kind:'accepted'}, {field:'actorId', kind:'rejected'}, {field:'realmId', kind:'rejected'}] as const)('does not consume $kind at $field change during the final transmit read', async ({field, kind}) => {
      const env = environment();
      const reading = deferred(), complete = deferred();
      let pauseRead = false, arm = false;
      env.transmit.mockImplementationOnce(async () => {
        arm = true;
        return kind === 'accepted' ? acceptance('A') : { kind: 'rejected', error: { reason: 'original conflict' } };
      });
      const requester = createPlacementRequester({ client: env.client, outboxes: env.storage(),
        getRecoverableIdentity: async () => {
          if (arm) { arm = false; pauseRead = true; }
          return { ...env.state.identity };
        }, capture: env.capture, build: env.build, transmit: env.transmit });
      await env.storage().create(scope, async (box) => {
        const read = box.read.bind(box);
        vi.spyOn(box, 'read').mockImplementation(async () => {
          const record = await read();
          if (pauseRead) { pauseRead = false; reading.resolve(); await complete.promise; }
          return record;
        });
        const advancing = requester.request(box, 'request', input);
        await reading.promise;
        const before = await read();
        env.state.identity = { ...env.state.identity, [field]: 'different' };
        complete.resolve();
        const result = await advancing;
        const after = await read();
        console.info('RESIDUAL_ACK', JSON.stringify({ field, kind, status: result.status, before, after }));
        expect(before.pending!.request).toEqual(env.transmit.mock.calls[0][0]);
        env.state.identity = { realmId: scope.realmId, actorId: scope.actorId };
        expect(await requester.resume(box)).toMatchObject([{ status: 'accepted' }]);
        expect(env.transmit.mock.calls.map(([request]) => request)).toEqual([before.pending!.request, before.pending!.request]);
        expect(env.capture).toHaveBeenCalledTimes(1);
        expect(env.build).toHaveBeenCalledTimes(1);
        expect(after.pending?.request).toEqual(before.pending!.request);
        expect(after.intents).toEqual(before.intents);
      });
  });

  it.each(['actorId', 'realmId'] as const)('does not persist API refusal after %s changes during the refusal authorization read', async (field) => {
    const env = environment();
    const reading = deferred(), complete = deferred();
    let pauseRead = false, arm = false;
    env.state.admissionFailure = 403;
    const admit = env.client.admitTask.bind(env.client);
    vi.spyOn(env.client, 'admitTask').mockImplementationOnce(async (...args) => {
      try { return await admit(...args); } finally { arm = true; }
    });
    const requester = createPlacementRequester({ client: env.client, outboxes: env.storage(),
      getRecoverableIdentity: async () => {
        if (arm) { arm = false; pauseRead = true; }
        return { ...env.state.identity };
      }, capture: env.capture, build: env.build, transmit: env.transmit });
    await env.storage().create(scope, async (box) => {
      const read = box.read.bind(box);
      vi.spyOn(box, 'read').mockImplementation(async () => {
        const record = await read();
        if (pauseRead) { pauseRead = false; reading.resolve(); await complete.promise; }
        return record;
      });
      const advancing = requester.request(box, 'request', input);
      await reading.promise;
      const before = await read();
      env.state.identity = { ...env.state.identity, [field]: 'different' };
      complete.resolve();
      const result = await advancing;
      const after = await read();
      console.info('RESIDUAL_REFUSAL', JSON.stringify({ field, status: result.status,
        before: before.placementContinuations, after: after.placementContinuations }));
      env.state.identity = { realmId: scope.realmId, actorId: scope.actorId };
      env.state.admissionFailure = 0;
      expect(await requester.resume(box)).toMatchObject([{ status: 'accepted' }]);
      expect(env.calls.filter((c) => c.method === 'POST')).toEqual([prepared, prepared]);
      expect(env.capture).toHaveBeenCalledTimes(1);
      expect(after.placementContinuations).toEqual(before.placementContinuations);
    });
  });
});

describe('independent claim and microtask handoffs', () => {
  it('never POSTs from a claim released by a promise reaction to the final read', async () => {
    const env = environment();
    const release = deferred();
    const held = new Set<string>();
    let ownerReleased = false;
    const storage = createCommitOutbox({ indexedDB: env.factory, exclusiveLock: async (name, work) => {
      if (held.has(name)) throw new Error('Outbox is already claimed');
      held.add(name);
      try { return await work(); } finally { held.delete(name); ownerReleased = true; }
    } });
    let checks = 0, handoff = false, claimReturned = false;
    let late!: ReturnType<ReturnType<typeof createPlacementRequester>['resume']>;
    let ownerId!: string;
    const posts: unknown[] = [];
    const admit = env.client.admitTask.bind(env.client);
    vi.spyOn(env.client, 'admitTask').mockImplementation(async (...args) => {
      posts.push({ claimReturned, ownerReleased, identity: { ...env.state.identity } });
      return admit(...args);
    });
    const requester = createPlacementRequester({ client: env.client, outboxes: storage,
      getRecoverableIdentity: async () => {
        checks += 1;
        if (checks === 3) handoff = true;
        return { ...env.state.identity };
      }, capture: env.capture, build: env.build, transmit: env.transmit });
    await storage.create(scope, async (box, id) => {
      ownerId = id;
      await env.reserve(box);
      const read = box.read.bind(box);
      vi.spyOn(box, 'read').mockImplementation(() => {
        const pending = read();
        if (!handoff) return pending;
        handoff = false;
        return pending.then((record) => {
          release.resolve(); // ordinary promise reaction releases the claim callback
          return Promise.resolve(record);
        });
      });
      late = requester.resume(box);
      await release.promise;
      claimReturned = true;
    });
    const result = await late;
    await storage.recover(scope, ownerId, async (box) => {
      console.info('MICROTASK_POST', JSON.stringify({ posts, result, saved: await box.read() }));
      expect((await box.read()).placementContinuations![0].taskLocator).toBeUndefined();
      expect(await requester.resume(box)).toMatchObject([{ status: 'accepted' }]);
    });
    expect(posts.slice(0, -1)).toEqual([]);
  });

  it.each(['capture', 'transmit', 'refusal'] as const)('does not mutate %s after a promise reaction releases the claim following its final read', async (stage) => {
    const env = environment();
    const release = deferred();
    let arm = false, handoff = false;
    let late!: Promise<unknown>;
    let ownerId!: string;
    let before!: Awaited<ReturnType<ClaimedOutbox['read']>>;
    const requester = createPlacementRequester({ client: env.client, outboxes: env.storage(),
      getRecoverableIdentity: async () => {
        if (arm) { arm = false; handoff = true; }
        return { ...env.state.identity };
      }, capture: env.capture, build: env.build, transmit: env.transmit });
    if (stage === 'capture') {
      const capture = env.capture.getMockImplementation()!;
      env.capture.mockImplementationOnce(async (saved) => { arm = true; return capture(saved); });
    } else if (stage === 'transmit') env.transmit.mockImplementationOnce(async () => { arm = true; return acceptance('A'); });
    else {
      env.state.admissionFailure = 403;
      const admit = env.client.admitTask.bind(env.client);
      vi.spyOn(env.client, 'admitTask').mockImplementationOnce(async (...args) => {
        try { return await admit(...args); } finally { arm = true; }
      });
    }
    await env.storage().create(scope, async (box, id) => {
      ownerId = id;
      const read = box.read.bind(box);
      vi.spyOn(box, 'read').mockImplementation(() => {
        const pending = read();
        if (!handoff) return pending;
        handoff = false;
        return pending.then((record) => {
          before = record;
          release.resolve();
          return record;
        });
      });
      late = requester.request(box, 'request', input);
      await release.promise;
    });
    await late;
    await env.storage().recover(scope, ownerId, async (box) => {
      const after = await box.read();
      console.info('MICROTASK_MUTATION', JSON.stringify({ stage, before, after }));
      expect(after).toEqual({ ...before, generation: 2 });
      env.state.admissionFailure = 0;
      expect(await requester.resume(box)).toMatchObject([{ status: 'accepted' }]);
      if (stage === 'transmit') {
        expect(env.transmit.mock.calls.map(([request]) => request)).toEqual([before.pending!.request, before.pending!.request]);
        expect(env.build).toHaveBeenCalledTimes(1);
        expect(env.capture).toHaveBeenCalledTimes(1);
      }
    });
  });
});

describe('requester checks at the mutation and callback boundaries', () => {
  it.each(['actorId', 'realmId'] as const)('revalidates %s in the actual storage callback', async (field) => {
    for (const stage of ['locator', 'capture', 'capture-refusal', 'accepted', 'rejected', 'api-refusal'] as const) {
      const env = environment();
      let arm = false, delayWrite = false;
      const requester = createPlacementRequester({ client: env.client, outboxes: env.storage(),
        getRecoverableIdentity: async () => {
          if (arm) { arm = false; delayWrite = true; }
          return { ...env.state.identity };
        }, capture: env.capture, build: env.build, transmit: env.transmit });
      if (stage === 'locator' || stage === 'api-refusal') {
        if (stage === 'api-refusal') env.state.admissionFailure = 403;
        const admit = env.client.admitTask.bind(env.client);
        vi.spyOn(env.client, 'admitTask').mockImplementationOnce(async (...args) => {
          try { return await admit(...args); } finally { arm = true; }
        });
      } else if (stage === 'capture' || stage === 'capture-refusal') {
        const capture = env.capture.getMockImplementation()!;
        env.capture.mockImplementationOnce(async (saved) => {
          arm = true;
          if (stage === 'capture-refusal') throw new Error('Original semantic refusal');
          return capture(saved);
        });
      } else env.transmit.mockImplementationOnce(async () => {
        arm = true;
        return stage === 'accepted' ? acceptance('A') : { kind: 'rejected', error: { reason: 'original conflict' } };
      });
      await env.storage().create(scope, async (box) => {
        let before!: Awaited<ReturnType<ClaimedOutbox['read']>>;
        const read = box.read.bind(box);
        vi.spyOn(box, 'read').mockImplementation(async () => {
          const record = await read();
          if (delayWrite) {
            delayWrite = false;
            before = record;
            // Run before the real mutation's get-success handler, after every authorization read.
            env.fault.beforeWrite = () => { env.state.identity = { ...env.state.identity, [field]: 'different' }; };
          }
          return record;
        });
        expect((await requester.request(box, 'request', input)).status).toBe('retry');
        expect(await read()).toEqual(before);
        expect(before.placementContinuations![0].input).toEqual(input);
        if (stage === 'accepted' || stage === 'rejected') expect(before.pending!.request).toEqual(env.transmit.mock.calls[0][0]);
        env.state.identity = { realmId: scope.realmId, actorId: scope.actorId };
        env.state.admissionFailure = 0;
        expect(await requester.resume(box)).toMatchObject([{ status: 'accepted' }]);
        if (stage === 'accepted' || stage === 'rejected') {
          expect(env.transmit.mock.calls.map(([request]) => request)).toEqual([before.pending!.request, before.pending!.request]);
          expect(env.build).toHaveBeenCalledTimes(1);
        }
        expect(env.capture.mock.lastCall![0]).toMatchObject({ input, mediaPin: pin });
        expect(env.calls.filter((call) => call.method === 'POST')).toEqual(
          stage === 'locator' || stage === 'api-refusal' ? [prepared, prepared] : [prepared]);
      });
    }
  });

  it.each(['capture', 'transmit'] as const)('never invokes %s after its final read releases the claim in a promise reaction', async (stage) => {
    const env = environment();
    const release = deferred();
    let arm = false, handoff = false, ownerId = '';
    let late!: Promise<unknown>;
    const requester = createPlacementRequester({ client: env.client, outboxes: env.storage(),
      getRecoverableIdentity: async () => {
        if (arm) { arm = false; handoff = true; }
        return { ...env.state.identity };
      }, capture: env.capture, build: env.build, transmit: env.transmit });
    await env.storage().create(scope, async (box, id) => {
      ownerId = id;
      if (stage === 'capture') {
        const capture = box.capturePlacement.bind(box);
        vi.spyOn(box, 'capturePlacement').mockImplementation((...args) => { arm = true; return capture(...args); });
      } else {
        const build = env.build.getMockImplementation()!;
        env.build.mockImplementationOnce((...args) => { arm = true; return build(...args); });
      }
      const read = box.read.bind(box);
      vi.spyOn(box, 'read').mockImplementation(() => {
        const pending = read();
        if (!handoff) return pending;
        handoff = false;
        return pending.then((record) => {
          release.resolve();
          return Promise.resolve(record);
        });
      });
      late = requester.request(box, 'request', input);
      await release.promise;
    });
    await late;
    expect(env.transmit).not.toHaveBeenCalled();
    if (stage === 'capture') expect(env.capture).not.toHaveBeenCalled();
    await env.storage().recover(scope, ownerId, async (box) => {
      const before = await box.read();
      expect(before.generation).toBe(2);
      expect(before.placementContinuations![0].conflict).toBeUndefined();
      expect(await requester.resume(box)).toMatchObject([{ status: 'accepted' }]);
      if (stage === 'transmit') {
        expect(env.transmit.mock.lastCall![0]).toEqual(before.pending!.request);
        expect(env.build).toHaveBeenCalledTimes(1);
      }
      expect(env.capture).toHaveBeenCalledTimes(1);
      expect(env.calls.filter((call) => call.method === 'POST')).toEqual([prepared]);
    });
  });

  it('leaves the helper inactive when the authenticated host lifecycle binding is missing', async () => {
    const env = environment();
    const { admitTask, getTask, listManagedOutputs, getProjectMediaSelection } = env.client;
    const requester = createPlacementRequester({ client: {
      admitTask: admitTask.bind(env.client), getTask: getTask.bind(env.client),
      listManagedOutputs: listManagedOutputs.bind(env.client), getProjectMediaSelection: getProjectMediaSelection.bind(env.client),
    }, outboxes: env.storage(), getRecoverableIdentity: async () => ({ ...env.state.identity }), capture: env.capture,
    build: env.build, transmit: env.transmit });
    await env.storage().create(scope, async (box) => {
      const before = await box.read();
      await expect(requester.request(box, 'request', input)).rejects.toThrow('identity lifecycle binding is unavailable');
      expect(await box.read()).toEqual(before);
      await env.reserve(box);
    });
    expect(await requester.recover()).toMatchObject([{ status: 'retry', message: 'Authenticated requester identity lifecycle binding is unavailable' }]);
    expect(env.calls).toEqual([]);
    expect(env.capture).not.toHaveBeenCalled();
    expect(env.transmit).not.toHaveBeenCalled();
  });

  it('rejects an asynchronous host check instead of treating its promise as live identity', async () => {
    const env = environment();
    Object.assign(env.client, { isCurrentIdentity: async () => true });
    await env.storage().create(scope, async (box) => {
      const before = await box.read();
      await expect(env.requester().request(box, 'request', input)).rejects.toThrow('identity changed or is unavailable');
      expect(await box.read()).toEqual(before);
      expect(env.calls).toEqual([]);
    });
  });

  it('honors host invalidation even when the actor and realm strings are unchanged', async () => {
    const env = environment();
    const checking = deferred(), complete = deferred();
    let invalidated = false, arm = false;
    const isCurrent = env.client.isCurrentIdentity.bind(env.client);
    env.client.isCurrentIdentity = (identity) => !invalidated && isCurrent(identity);
    env.transmit.mockImplementationOnce(async () => { arm = true; return acceptance('A'); });
    const requester = createPlacementRequester({ client: env.client, outboxes: env.storage(),
      getRecoverableIdentity: async () => {
        if (arm) { arm = false; checking.resolve(); await complete.promise; }
        return { ...env.state.identity };
      }, capture: env.capture, build: env.build, transmit: env.transmit });
    await env.storage().create(scope, async (box) => {
      const advancing = requester.request(box, 'request', input);
      await checking.promise;
      const before = await box.read();
      invalidated = true;
      complete.resolve();
      expect((await advancing).status).toBe('retry');
      const retained = await box.read();
      expect(retained.pending!.request).toEqual(before.pending!.request);
      expect(retained.intents).toEqual(before.intents);
      expect(retained.placementContinuations).toEqual(before.placementContinuations);
      invalidated = false; // explicit authenticated host recovery, with the original identity
      expect(await requester.resume(box)).toMatchObject([{ status: 'accepted' }]);
      expect(env.transmit.mock.calls.map(([request]) => request)).toEqual([before.pending!.request, before.pending!.request]);
    });
  });
});
