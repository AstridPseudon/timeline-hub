// The only way a node:test test skips. `{ skip: declaredSkip('macos-lockf-broker', cond) }` or, inside a test,
// `if (declaredSkipIf(t, 'symlink-creation-permitted', cond)) return;`. `name` must be declared in
// config/testing/skipRegistry.mjs; scripts/quality/node-skip-guard-reporter.mjs fails the run on any other skip.
import { declaredTag } from '../../config/testing/skipRegistry.mjs';

/** The `skip` option value: the tagged reason when `condition` holds, else false. */
export function declaredSkip(name, condition) {
  return condition ? declaredTag(name) : false;
}

/** Skips the running test `t` with the tagged reason when `condition` holds; returns whether it skipped. */
export function declaredSkipIf(t, name, condition) {
  if (!condition) return false;
  t.skip(declaredTag(name));
  return true;
}
