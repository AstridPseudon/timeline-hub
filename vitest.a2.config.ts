import base from './config/testing/vitest.config.ts';

export default {
  ...base,
  test: {
    ...base.test,
    include: ['.a2-mounted-probe.test.tsx'],
  },
};
