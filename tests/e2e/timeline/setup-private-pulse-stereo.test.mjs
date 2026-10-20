import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {join} from 'node:path';
import {test} from 'node:test';

const setup = join(import.meta.dirname, 'setup-private-pulse-stereo.sh');

test('pure and live controller setup boundaries stay explicit', () => {
  const source = readFileSync(setup, 'utf8');
  assert.match(source, /if \[\[ \$\{TAB_AUDIO_RUN:-0\} != 1 \]\]; then/);
  assert.match(source, /env -u TAB_AUDIO_RUN -u TAB_AUDIO_GRANT_PATH "\$NODE" "\$PRIVATE_CONTROLLER" --prepare/);
  assert.match(source, /"\$NODE" "\$BASE_CONTROLLER" --preflight/);
  assert.match(source, /"\$NODE" "\$BASE_CONTROLLER" --claim/);
  assert.match(source, /"\$NODE" "\$BASE_CONTROLLER" --postflight/);
  assert.match(source, /BASE_WORKER_STATE_ROOT=\/tmp\/claude-0\/[^\n]+\/workers\/vw-m3-stereo-owned-state-guard-fix/);
  for (const name of ['TAB_AUDIO_PREFLIGHT_PATH', 'TAB_AUDIO_RUN_MARKER', 'TAB_AUDIO_GRANT_PATH', 'PLAYWRIGHT_OUTPUT_DIR']) {
    assert.match(source, new RegExp(`assert_base_worker_path "\\$${name}"`));
  }
  assert.match(source, /PULSE_RUNTIME_DIR=\$\(mktemp -d \/tmp\/timeline-private-pulse-runtime-XXXXXX\)/);
  assert.match(source, /PULSE_SOCKET="\$PULSE_RUNTIME_DIR\/native"/);
});
