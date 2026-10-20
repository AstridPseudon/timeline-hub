export function gainDifferenceDb(actual: number, reference: number) {
  return 20 * Math.log10(actual / reference);
}

export function requireUnchangedGain(actual: number, reference: number) {
  const db = gainDifferenceDb(actual, reference);
  if (!Number.isFinite(actual) || actual <= 0 || !Number.isFinite(reference) || reference <= 0 || Math.abs(db) > 0.5) {
    throw new Error(`captured output gain mismatch: ${db.toFixed(3)} dB`);
  }
}
