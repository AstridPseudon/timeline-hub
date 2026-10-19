import type { DeferredSupabaseClient } from '@/integrations/supabase/deferredRuntime';
import { initAuthStateManager } from '@/integrations/supabase/auth/AuthStateManager';
import { initializeReconnectScheduler } from '@/integrations/supabase/support/reconnect/ReconnectScheduler';
import { maybeAutoLogin } from '@/integrations/supabase/support/dev/autoLogin';

export function initializeSupabaseRuntime(
  client: DeferredSupabaseClient,
): void {
  // Shared runtime wiring after client construction.
  const reconnectScheduler = initializeReconnectScheduler();
  initAuthStateManager(client, reconnectScheduler);
  maybeAutoLogin(client);
}
