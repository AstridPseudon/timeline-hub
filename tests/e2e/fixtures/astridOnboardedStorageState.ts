/** Reusable first-run state for browser suites that exercise post-onboarding product flows. */
export function astridOnboardedStorageState(baseURL: string) {
  return {
    cookies: [],
    origins: [
      {
        origin: new URL(baseURL).origin,
        localStorage: [{ name: 'astrid-setup-complete', value: 'true' }],
      },
    ],
  };
}
