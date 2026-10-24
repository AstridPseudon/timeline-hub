import {readFileSync} from 'node:fs';
import {resolve} from 'node:path';
import {describe, expect, it} from 'vitest';
import type {ResolvedTimelineConfig} from '@/tools/video-editor/types/index.ts';
import {analyzeVisualSeams, timecode} from './visualSeamContract.ts';

type ExpectedFinding = {code: string; frame: number; clips: string[]};
type Case = {name: string; timeline: ResolvedTimelineConfig; expected: ExpectedFinding[]};

function sharedCases(): Case[] {
  const checkout = process.env.ASTRID_RUNTIME_CHECKOUT;
  expect(checkout, 'set ASTRID_RUNTIME_CHECKOUT to an Astrid Runtime checkout').toBeTruthy();
  const fixturePath = resolve(checkout!, 'conformance/fixtures/visual-seam-cases-v1.json');
  const fixture = JSON.parse(readFileSync(fixturePath, 'utf8')) as {schema_version: number; cases: Case[]};
  expect(fixture.schema_version).toBe(1);
  return fixture.cases;
}

describe('shared App and Runtime visual seam cases', () => {
  it('matches the shared expected findings', () => {
    const cases = sharedCases();
    expect(cases.length).toBeGreaterThanOrEqual(6);
    for (const testCase of cases) {
      const report = analyzeVisualSeams(testCase.timeline);
      const clips = new Map(testCase.timeline.clips.map((clip) => [clip.id, clip]));
      const expectedLines = testCase.expected.map((expected) => {
        const kind = expected.code === 'boundary/overlap' ? 'overlap'
          : expected.code === 'boundary/gap' ? 'gap' : undefined;
        expect(kind, `${testCase.name}: unknown expected code ${expected.code}`).toBeDefined();
        const participants = expected.clips.map((id) => clips.get(id));
        expect(participants.every(Boolean), `${testCase.name}: missing expected clip`).toBe(true);
        const labels = participants.map((clip) => clip!.label ?? clip!.text?.content ?? 'Unlabeled clip');
        const track = testCase.timeline.tracks.find((row) => row.id === participants[0]!.track);
        const trackLabel = track?.label ?? participants[0]!.track;
        const detail = kind === 'overlap'
          ? `Two full-screen clips overlap on ${trackLabel}: '${labels[0]}' and '${labels[1]}'`
          : `Gap on ${trackLabel} between '${labels[0]}' and '${labels[1]}'`;
        return `${timecode(expected.frame / testCase.timeline.output.fps)} · ${detail}`;
      });
      expect(report.structuralIssues, testCase.name).toEqual(expectedLines);
      expect(report.boundaries.filter(boundary => boundary.structuralIssues.length > 0).map(boundary => boundary.frame), testCase.name)
        .toEqual(testCase.expected.map(finding => finding.frame));
    }
  });
});
