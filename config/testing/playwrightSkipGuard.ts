import type { FullResult, Reporter, TestCase, TestResult } from '@playwright/test/reporter';
import { classifySkips, formatSkipReport } from './skipRegistry.mjs';

/**
 * Prints every skipped test by name and fails the run on any skip, fixme or expected-failure marker
 * whose reason is not declared in skipRegistry.mjs. Declared skips come from tests/e2e/support/declaredSkip.ts.
 * A test that did not run because an earlier serial test failed is also "skipped"; those are only listed,
 * since the run has already failed.
 */
export default class PlaywrightSkipGuard implements Reporter {
  private readonly entries: Array<{ name: string; reason: string }> = [];

  printsToStdio(): boolean {
    return false;
  }

  onTestEnd(test: TestCase, result: TestResult): void {
    const marker = test.annotations.find((annotation) => annotation.type === 'skip' || annotation.type === 'fixme');
    if (result.status === 'skipped' || marker) {
      this.entries.push({ name: test.titlePath().filter(Boolean).join(' > '), reason: marker?.description ?? '' });
    }
  }

  async onEnd(result: FullResult): Promise<{ status: FullResult['status'] } | undefined> {
    if (!this.entries.length) return undefined;
    const report = classifySkips(this.entries);
    console.log(`\n${formatSkipReport(report)}`);
    if (report.undeclared.length && result.status === 'passed') {
      console.error(`\n${report.undeclared.length} undeclared skip(s): declare each in config/testing/skipRegistry.mjs and use tests/e2e/support/declaredSkip.ts.`);
      return { status: 'failed' };
    }
    return undefined;
  }
}
