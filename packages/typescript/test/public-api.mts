/** Consumer imports resolve through the published package exports and declarations. */
import {
  CONTRACT_VERSION, WorkspaceClient,
  type Health, type Handshake, type PreferenceResource, type MutationResult, type ServiceStatus,
} from "@astrid/runtime-client";

const version: string = CONTRACT_VERSION;
const client = new WorkspaceClient("http://runtime.invalid");
const health: Promise<Health> = client.health();
const handshake: Promise<Handshake> = client.handshake("consumer", version, []);
const preference: Promise<PreferenceResource> = client.getPreferences("user");
const mutation: Promise<MutationResult<unknown>> = client.createProject("consumer", "key");
const service: ServiceStatus = { name: "example", state: "starting", last_exit: null, restart_count: 0 };
void [health, handshake, preference, mutation, service];
