import { it } from 'node:test';
import { declaredSkip } from '../../../../scripts/quality/declared-skip.mjs';
it('mac only', { skip: declaredSkip('macos-lockf-broker', true) }, () => {});
