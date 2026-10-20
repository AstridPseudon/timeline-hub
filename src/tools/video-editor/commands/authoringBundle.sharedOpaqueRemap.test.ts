// @vitest-environment node
import { createHash } from 'node:crypto';
import { readFileSync } from 'node:fs';
import { describe, expect, it } from 'vitest';
import { remapItemsForTest } from './authoringBundle.ts';
import { type JSON } from '@/integrations/runtime/timeline-commit-types.ts';

type RawNumber = { readonly kind: 'number'; readonly raw: string };
type RawValue = RawNumber | null | boolean | string | RawValue[] | { [key: string]: RawValue };
type JSONRecord = { [key: string]: JSON };
type FixtureCase = { name: string; item_ids: JSONRecord; payload: JSONRecord; expected: JSONRecord };
type Fixture = { schema: string; cases: FixtureCase[] };

const fixtureText = readFileSync(new URL('./fixtures/corpus/opaque_remap.json', import.meta.url), 'utf8');
const fixture = JSON.parse(fixtureText) as unknown as Fixture;

// JSON.parse intentionally collapses 0 and 0.0. Keep the source number token
// beside the parsed value so the comparison remains Agent-canonical and byte exact.
function parseRawJson(text: string): RawValue {
  let cursor = 0;

  const whitespace = () => {
    while (/\s/.test(text[cursor] ?? '')) cursor += 1;
  };
  const string = (): string => {
    const start = cursor;
    cursor += 1;
    while (cursor < text.length) {
      if (text[cursor] === '\\') cursor += 2;
      else if (text[cursor++] === '"') return JSON.parse(text.slice(start, cursor)) as string;
    }
    throw new Error('unterminated JSON string');
  };
  const value = (): RawValue => {
    whitespace();
    const character = text[cursor];
    if (character === '"') return string();
    if (character === '{') {
      cursor += 1;
      const result: { [key: string]: RawValue } = {};
      whitespace();
      if (text[cursor] === '}') { cursor += 1; return result; }
      while (true) {
        whitespace();
        const key = string();
        whitespace();
        if (text[cursor++] !== ':') throw new Error('missing JSON object colon');
        result[key] = value();
        whitespace();
        if (text[cursor] === '}') { cursor += 1; return result; }
        if (text[cursor++] !== ',') throw new Error('missing JSON object comma');
      }
    }
    if (character === '[') {
      cursor += 1;
      const result: RawValue[] = [];
      whitespace();
      if (text[cursor] === ']') { cursor += 1; return result; }
      while (true) {
        result.push(value());
        whitespace();
        if (text[cursor] === ']') { cursor += 1; return result; }
        if (text[cursor++] !== ',') throw new Error('missing JSON array comma');
      }
    }
    for (const [literal, parsed] of [['true', true], ['false', false], ['null', null] ] as const) {
      if (text.startsWith(literal, cursor)) {
        cursor += literal.length;
        return parsed;
      }
    }
    const number = text.slice(cursor).match(/^-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?/u)?.[0];
    if (!number) throw new Error(`invalid JSON at ${cursor}`);
    cursor += number.length;
    return { kind: 'number', raw: number };
  };

  const result = value();
  whitespace();
  if (cursor !== text.length) throw new Error(`trailing JSON at ${cursor}`);
  return result;
}

function isRawNumber(value: RawValue): value is RawNumber {
  return value !== null && typeof value === 'object' && !Array.isArray(value) && value.kind === 'number';
}

function compareCodePoints(left: string, right: string): number {
  const a = Array.from(left, (character) => character.codePointAt(0)!);
  const b = Array.from(right, (character) => character.codePointAt(0)!);
  for (let index = 0; index < Math.min(a.length, b.length); index += 1) {
    if (a[index] !== b[index]) return a[index] - b[index];
  }
  return a.length - b.length;
}

function canonical(value: unknown, shape: RawValue): string {
  if (isRawNumber(shape)) {
    expect(typeof value).toBe('number');
    return shape.raw;
  }
  if (Array.isArray(shape)) {
    expect(Array.isArray(value)).toBe(true);
    return `[${shape.map((entry, index) => canonical((value as unknown[])[index], entry)).join(',')}]`;
  }
  if (shape !== null && typeof shape === 'object') {
    expect(value !== null && typeof value === 'object' && !Array.isArray(value)).toBe(true);
    const record = value as Record<string, unknown>;
    const keys = Object.keys(shape).sort(compareCodePoints);
    return `{${keys.map((key) => `${JSON.stringify(key)}:${canonical(record[key], shape[key])}`).join(',')}}`;
  }
  expect(typeof value).toBe(typeof shape);
  return JSON.stringify(value);
}

function rawCase(fixtureShape: RawValue, index: number): { payload: RawValue; expected: RawValue } {
  const cases = (fixtureShape as { cases: RawValue[] }).cases;
  const entry = cases[index] as { payload: RawValue; expected: RawValue };
  return entry;
}

describe('Agent shared opaque remap corpus', () => {
  it('matches native canonical output and preserves input for every published case', () => {
    expect(Buffer.byteLength(fixtureText)).toBe(5866);
    expect(createHash('sha256').update(fixtureText).digest('hex'))
      .toBe('49228930598f19ca3055cb442af9519ef2f8d4b6a2a98c799d4a78baa55c8e66');
    expect(fixture.schema).toBe('opaque-remap/v1');

    const rawFixture = parseRawJson(fixtureText);
    for (const [index, testCase] of fixture.cases.entries()) {
      const source = structuredClone(testCase.payload);
      const before = canonical(source, rawCase(rawFixture, index).payload);
      const result = remapItemsForTest(source, testCase.item_ids as Record<string, string>);
      const shape = rawCase(rawFixture, index);
      expect(canonical(result, shape.payload), testCase.name)
        .toBe(canonical(testCase.expected, shape.expected));
      expect(canonical(source, shape.payload), `${testCase.name} input mutation`)
        .toBe(before);
    }
  });

  it('keeps prototype-looking keys as ordinary opaque own data', () => {
    const payload = JSON.parse(
      '{"items":[{"item_id":"item-1","__proto__":{"item_id":"item-1"},"constructor":"item-1","prototype":"item-1","metadata":{"source_item_id":"item-1","__proto__":{"constructor":"item-1"}}}],"__proto__":{"constructor":{"prototype":"item-1"}},"constructor":"item-1","prototype":"item-1"}',
    ) as JSONRecord;
    const result = remapItemsForTest(payload, { 'item-1': 'item-9' });
    const item = (result.items as JSONRecord[])[0];

    expect(Object.hasOwn(result, '__proto__')).toBe(true);
    expect(Object.hasOwn(result, 'constructor')).toBe(true);
    expect(Object.hasOwn(result, 'prototype')).toBe(true);
    expect(Object.hasOwn(item, '__proto__')).toBe(true);
    expect(Object.hasOwn(item, 'constructor')).toBe(true);
    expect(Object.hasOwn(item, 'prototype')).toBe(true);
    expect(item.item_id).toBe('item-9');
    expect(item.constructor).toBe('item-1');
    expect(item.prototype).toBe('item-1');
    expect((item.metadata as JSONRecord).source_item_id).toBe('item-9');
    expect((item.metadata as JSONRecord).__proto__).toEqual({ constructor: 'item-1' });
    expect(result.__proto__).toEqual({ constructor: { prototype: 'item-1' } });
    expect(result.constructor).toBe('item-1');
    expect(result.prototype).toBe('item-1');
  });
});
