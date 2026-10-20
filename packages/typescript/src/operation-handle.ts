import { PROTOCOL, WorkspaceClient } from "./generated.js";
import type { HeadersLike, Transport } from "./generated.js";

export interface OperationIdentity {
  actorId: string;
  realmId: string;
}

export interface OperationConnection {
  baseUrl: string;
  token: string;
}

export class OperationRetiredError extends Error {
  constructor() {
    super("Runtime operation lifetime is retired");
    this.name = "OperationRetiredError";
  }
}

/** Direct credential owner only: a proxy that reselects credentials is unsupported. */
export class OperationHandle {
  readonly client: WorkspaceClient;
  private retired = false;
  private identity?: OperationIdentity;
  private negotiation?: Promise<OperationIdentity>;

  constructor({ baseUrl, token }: OperationConnection) {
    if (!baseUrl.trim() || !token.trim()) throw new Error("Runtime base and owned credential are required");
    const base = baseUrl.replace(/\/$/, "");
    const dispatch = globalThis.fetch.bind(globalThis);
    const transport: Transport = async (method, path, headers, body) => {
      this.assertActive();
      try {
        // No await between the lifetime check and the captured transport dispatch.
        const response = await dispatch(`${base}${path}`, {
          method, headers, body: body as BodyInit | undefined, credentials: "omit", redirect: "error",
        });
        this.assertActive();
        if (response.status === 401 || response.status === 403 || response.status >= 500) this.retire();
        const bytes = new Uint8Array(await response.arrayBuffer());
        this.assertActive();
        const responseHeaders: HeadersLike = {};
        response.headers.forEach((value, key) => { responseHeaders[key] = value; });
        return { status: response.status, headers: responseHeaders, body: bytes };
      } catch (error) {
        this.retire();
        throw error;
      }
    };
    this.client = new WorkspaceClient(base, token, transport);
  }

  private assertActive(): void {
    if (this.retired) throw new OperationRetiredError();
  }

  readonly retire = (): void => {
    this.retired = true;
  };

  /** Local owned lifetime, never a claim that remote revocation is observable synchronously. */
  readonly isCurrentIdentity = (expected: OperationIdentity): boolean => {
    return !this.retired && !!this.identity
      && !!expected.actorId && !!expected.realmId
      && expected.actorId === this.identity.actorId && expected.realmId === this.identity.realmId;
  };

  async negotiate(clientName: string, clientVersion: string, requestedScopes: string[]): Promise<OperationIdentity> {
    this.assertActive();
    if (this.negotiation) throw new Error("Runtime renegotiation requires a new operation binding");
    this.negotiation = this.open(clientName, clientVersion, [...requestedScopes]);
    const identity = await this.negotiation;
    this.assertActive();
    return { ...identity };
  }

  private async open(clientName: string, clientVersion: string, requestedScopes: string[]): Promise<OperationIdentity> {
    try {
      const health = await this.client.health();
      const handshake = await this.client.handshake(clientName, clientVersion, requestedScopes);
      const realm = await this.client.getRealm();
      this.assertActive();
      if (health.status !== "ok" || health.protocol !== PROTOCOL || handshake.protocol !== PROTOCOL
        || !health.schema_digest || health.schema_digest !== handshake.schema_digest
        || !handshake.actor_id?.trim() || !handshake.realm_id?.trim()
        || realm.realm_id !== handshake.realm_id
        || requestedScopes.some(scope => !handshake.scopes.includes(scope))) {
        throw new Error("Runtime operation negotiation did not establish the requested identity and scopes");
      }
      this.identity = { actorId: handshake.actor_id, realmId: handshake.realm_id };
      return this.identity;
    } catch (error) {
      this.retire();
      throw error;
    }
  }

  readonly getRecoverableIdentity = async (): Promise<OperationIdentity> => {
    this.assertActive();
    if (!this.negotiation) throw new Error("Runtime operation has not negotiated");
    const identity = await this.negotiation;
    this.assertActive();
    return { ...identity };
  };
}

/** The connector calls bind BEFORE switching base, credential, transport or reconnecting. */
export class OperationHost {
  private current?: OperationHandle;
  private disposed = false;

  bind(connection: OperationConnection): OperationHandle {
    this.current?.retire();
    this.current = undefined;
    if (this.disposed) throw new OperationRetiredError();
    const handle = new OperationHandle(connection);
    this.current = handle;
    return handle;
  }

  dispose(): void {
    this.disposed = true;
    this.current?.retire();
    this.current = undefined;
  }
}
