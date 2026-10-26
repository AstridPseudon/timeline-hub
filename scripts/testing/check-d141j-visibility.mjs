import { readFileSync } from 'node:fs';

const [artifactPath] = process.argv.slice(2);
if (!artifactPath) throw new Error('usage: check-d141j-visibility.mjs <artifact.json>');

const artifact = JSON.parse(readFileSync(artifactPath, 'utf8'));
const events = Array.isArray(artifact.events) ? artifact.events : [];
const event = (kind) => events.find((candidate) => candidate?.kind === kind);
const requireText = (value, label) => {
  if (typeof value !== 'string' || value.trim().length === 0) throw new Error(`${label} is empty`);
};
const requireIds = (value, label) => {
  if (!Array.isArray(value) || value.length === 0 || value.some((item) => typeof item !== 'string' || item.length === 0)) {
    throw new Error(`${label} is empty or malformed`);
  }
};
const requireAfter = (left, right, label) => {
  if (left < 0 || right < 0 || left >= right) throw new Error(`${label} is not ordered`);
};

if (artifact.schema !== 'timeline.app.d141j.visibility.v1') throw new Error('unexpected artifact schema');
requireText(artifact.expectedOccurrenceId, 'expectedOccurrenceId');
const accepted = event('accepted-canonical-read');
const active = event('active-occurrences-before-useShotGroups');
const grouped = event('useShotGroups-input-and-result');
const overlay = event('before-shot-group-overlay');
for (const [name, value] of [['accepted read', accepted], ['active occurrences', active], ['useShotGroups result', grouped], ['overlay boundary', overlay]]) {
  if (!value) throw new Error(`missing ${name} event`);
}

requireText(accepted.acceptedReadHeadRevisionId, 'acceptedReadHeadRevisionId');
requireText(accepted.projectId, 'accepted.projectId');
requireText(accepted.parentDocumentId, 'accepted.parentDocumentId');
requireIds(accepted.occurrenceIds, 'accepted occurrenceIds');
if (!accepted.occurrenceIds.includes(artifact.expectedOccurrenceId)) throw new Error('expected occurrence absent from accepted read');

requireIds(active.occurrenceIds, 'active occurrenceIds');
if (!active.occurrenceIds.includes(artifact.expectedOccurrenceId)) throw new Error('expected occurrence absent from active projection');
if (active.acceptedReadHeadRevisionId !== accepted.acceptedReadHeadRevisionId) throw new Error('accepted read head continuity is broken');
if (active.projectId !== accepted.projectId || active.parentDocumentId !== accepted.parentDocumentId) throw new Error('active projection identity changed');

requireIds(grouped.inputOccurrenceIds, 'useShotGroups input occurrenceIds');
requireIds(grouped.resultOccurrenceIds, 'useShotGroups result occurrenceIds');
requireIds(grouped.resultGroupKeys, 'useShotGroups result group keys');
if (grouped.resultGroupCount !== grouped.resultGroupKeys.length) throw new Error('useShotGroups result count mismatch');
if (!grouped.inputOccurrenceIds.includes(artifact.expectedOccurrenceId) || !grouped.resultOccurrenceIds.includes(artifact.expectedOccurrenceId)) {
  throw new Error('expected occurrence absent from useShotGroups input/result');
}

requireIds(overlay.canonicalOccurrenceIds, 'overlay canonical occurrenceIds');
requireIds(overlay.shotGroupOccurrenceIds, 'overlay shot-group occurrenceIds');
requireIds(overlay.shotGroupKeys, 'overlay shot-group keys');
if (overlay.shotGroupCount !== overlay.shotGroupKeys.length) throw new Error('overlay shot-group count mismatch');
if (!overlay.canonicalOccurrenceIds.includes(artifact.expectedOccurrenceId) || !overlay.shotGroupOccurrenceIds.includes(artifact.expectedOccurrenceId)) {
  throw new Error('expected occurrence absent before overlay');
}
if (JSON.stringify(overlay.shotGroupKeys) !== JSON.stringify(grouped.resultGroupKeys)) throw new Error('group result changed before overlay');

const acceptedIndex = events.indexOf(accepted);
const activeIndex = events.indexOf(active);
const groupedIndex = events.indexOf(grouped);
const overlayIndex = events.indexOf(overlay);
requireAfter(acceptedIndex, activeIndex, 'accepted read -> active projection');
requireAfter(activeIndex, groupedIndex, 'active projection -> useShotGroups');
requireAfter(groupedIndex, overlayIndex, 'useShotGroups -> overlay');

console.log(JSON.stringify({
  status: 'PASS',
  schema: artifact.schema,
  expectedOccurrenceId: artifact.expectedOccurrenceId,
  acceptedReadHeadRevisionId: accepted.acceptedReadHeadRevisionId,
  occurrenceCount: accepted.occurrenceIds.length,
  resultGroupCount: grouped.resultGroupCount,
  eventOrder: events.map(({ kind }) => kind),
}));
