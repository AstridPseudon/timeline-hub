import { bridgeCapabilityUnavailable } from '@/integrations/astrid/capability.ts';

/**
 * Relational shot routes have no Runtime path. Keep this assertion at the
 * operation boundary so callers fail before any shot repository call or
 * optimistic cache effect can run.
 */
export function assertDeferredCloudShotOperation(operation: string): void {
  throw bridgeCapabilityUnavailable(
    operation,
    'Use an Astrid pack command after shot routes are installed.',
  );
}
