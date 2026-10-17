let gatewayAppUrl: string | null = null;

/**
 * The local Astrid app's address (`http://127.0.0.1:<app port>`) the gateway reported in its health answer, or null
 * when it did not (`gatewayHealth.ts`). Set by the boot gate on connecting; read where the hosted build points the
 * person to the local app. A module of its own, so a test that mocks `connection.ts` for the origin leaves it alone.
 */
export function setRuntimeAppUrl(url: string | null): void {
  gatewayAppUrl = url;
}

export function runtimeAppUrl(): string | null {
  return gatewayAppUrl;
}
