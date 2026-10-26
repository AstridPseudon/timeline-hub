#!/usr/bin/env node
import { compose } from './pure-route-control.mjs';

const result = await compose();
const roles = Object.fromEntries(Object.entries(result.sourceManifest.tuple).map(([role, source]) => [role, {
  sha: source.sha,
  tree: source.tree,
  checkout: source.checkout,
  verified: source.verified === true,
  materialized: source.materialized ?? 'not asserted',
}]));
console.log(JSON.stringify({ status: 'PASS_SOURCE_BLOBS_AND_TUPLE', roles, candidate_source_qualification: result.sourceManifest.candidate.source_qualification }, null, 2));
