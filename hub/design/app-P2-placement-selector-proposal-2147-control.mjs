import assert from 'node:assert/strict';

const occurrenceId = 'f2-occurrence';
const siblingOccurrenceId = 'f2-sibling-occurrence';
const targetRawId = 'f2-agent-clip';
const referenceRawId = 'f2-agent-clear-clip';
const sameBytes = 'public-fixture-bytes';

const mountedActions = [
  { actionId: `${occurrenceId}:${targetRawId}`, bytes: sameBytes },
  { actionId: `${occurrenceId}:${referenceRawId}`, bytes: sameBytes },
  { actionId: `${siblingOccurrenceId}:${targetRawId}`, bytes: sameBytes },
];

function mountedBySelector(selector) {
  const match = /^\.clip-action\[data-clip-id="([^"]+)"\]$/.exec(selector);
  assert.ok(match, `selector must be an exact clip-action identity: ${selector}`);
  return mountedActions.filter(({ actionId }) => actionId === match[1]);
}

const oldTargetSelector = `.clip-action[data-clip-id="${targetRawId}"]`;
const targetSelector = `.clip-action[data-clip-id="${occurrenceId}:${targetRawId}"]`;
const referenceSelector = `.clip-action[data-clip-id="${occurrenceId}:${referenceRawId}"]`;
const wrongOccurrenceSelector = `.clip-action[data-clip-id="${siblingOccurrenceId}:${targetRawId}"]`;

// Faithful old-selector RED: mounted child actions never expose raw IDs.
assert.equal(mountedBySelector(oldTargetSelector).length, 0);

// New selectors GREEN: the intended physical target and geometry reference each resolve once.
assert.deepEqual(mountedBySelector(targetSelector).map(({ actionId }) => actionId), [`${occurrenceId}:${targetRawId}`]);
assert.deepEqual(mountedBySelector(referenceSelector).map(({ actionId }) => actionId), [`${occurrenceId}:${referenceRawId}`]);

// Strict negatives: a wrong occurrence cannot retarget the target, and identical bytes do not weaken identity.
assert.deepEqual(mountedBySelector(wrongOccurrenceSelector).map(({ actionId }) => actionId), [`${siblingOccurrenceId}:${targetRawId}`]);
assert.equal(mountedBySelector(targetSelector).filter(({ bytes }) => bytes === sameBytes).length, 1);
assert.notEqual(mountedBySelector(targetSelector)[0].actionId, mountedBySelector(wrongOccurrenceSelector)[0].actionId);

console.log('PASS mounted action-ID selector control: old RED, target/reference GREEN, wrong-occurrence/sibling/same-bytes negatives GREEN');
