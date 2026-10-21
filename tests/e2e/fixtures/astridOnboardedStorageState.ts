/** Reusable first-run state for browser suites that exercise post-onboarding product flows. */
export function astridOnboardedStorageState(baseURL: string, { editorTourSeen = true } = {}) {
  return {
    cookies: [],
    origins: [
      {
        origin: new URL(baseURL).origin,
        localStorage: [
          { name: 'astrid-setup-complete', value: 'true' },
          // Suites that open the editor are not about the first-run tour, whose shield would block them.
          ...(editorTourSeen ? [{ name: 'astrid-editor-tour-v1', value: '1' }] : []),
        ],
      },
    ],
  };
}
