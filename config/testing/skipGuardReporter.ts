import type { Reporter, TestModule } from 'vitest/node';
import { classifySkips, formatSkipReport } from './skipRegistry.mjs';

/**
 * Fails the run on any skipped, todo or .skip'd test whose skip is not declared in skipRegistry.mjs,
 * and prints every skip by test name. Declared skips arrive through `skipWhen`, which calls ctx.skip(note).
 */
export default class SkipGuardReporter implements Reporter {
  onTestRunEnd(testModules: ReadonlyArray<TestModule>): void {
    const entries: Array<{ name: string; reason: string }> = [];
    for (const module of testModules) {
      for (const test of module.children.allTests('skipped')) {
        const result = test.result();
        entries.push({
          name: `${module.moduleId.replace(`${process.cwd()}/`, '')} > ${test.fullName}`,
          reason: result.state === 'skipped' ? (result.note ?? '') : '',
        });
      }
    }
    if (!entries.length) return;
    const report = classifySkips(entries);
    console.log(`\n${formatSkipReport(report)}`);
    if (report.undeclared.length) {
      console.error(`\n${report.undeclared.length} undeclared skip(s): declare each in config/testing/skipRegistry.mjs and use skipWhen, or remove it.`);
      process.exitCode = 1;
    }
  }
}
