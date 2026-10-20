/** Consumer imports resolve through the published package exports and declarations. */
import {
  CONTRACT_VERSION, WorkspaceClient, OperationHost, OperationHandle, OperationRetiredError,
  type OperationIdentity, type OperationConnection,
  type Health, type Handshake, type PreferenceResource, type MutationResult, type TrackSetArgs,
  type MutationReceipt as MainMutationReceipt,
} from "@astrid/runtime-client";
import type { MutationReceipt as CommitMutationReceipt } from "../src/timeline-commit-types.js";

const version: string = CONTRACT_VERSION;
const client = new WorkspaceClient("http://runtime.invalid");
const health: Promise<Health> = client.health();
const handshake: Promise<Handshake> = client.handshake("consumer", version, []);
const preference: Promise<PreferenceResource> = client.getPreferences("user");
const mutation: Promise<MutationResult<unknown>> = client.createProject("consumer", "key");
declare const commitReceipt: CommitMutationReceipt;
declare const mainReceipt: MainMutationReceipt;
const mainReceiptFromCommit: MainMutationReceipt = commitReceipt;
const commitReceiptFromMain: CommitMutationReceipt = mainReceipt;
const projectSequence: [number, number] = commitReceipt.project_seq;
const labeledTrack: TrackSetArgs = { values: { label: "Picture" }, clear: [] };
const clearedTrack: TrackSetArgs = { values: {}, clear: ["label"] };
const connection: OperationConnection = { baseUrl: "http://runtime.invalid", token: "owned-credential" };
const host = new OperationHost();
const handle: OperationHandle = host.bind(connection);
const operationIdentity: Promise<OperationIdentity> = handle.negotiate("consumer", version, []);
const current: boolean = handle.isCurrentIdentity({ actorId: "actor", realmId: "realm" });
const recovery: Promise<OperationIdentity> = handle.getRecoverableIdentity();
const operationClient: WorkspaceClient = handle.client;
const retiredError: Error = new OperationRetiredError();
handle.retire();
host.dispose();

// @ts-expect-error Both shared fields are required.
const missingTrackFields: TrackSetArgs = {};
// @ts-expect-error Label setting still requires the clear field.
const missingTrackClear: TrackSetArgs = { values: { label: "Picture" } };
// @ts-expect-error Explicit clear still requires the values field.
const missingTrackValues: TrackSetArgs = { clear: ["label"] };
// @ts-expect-error Track labels must be strings.
const invalidTrackLabel: TrackSetArgs = { values: { label: false }, clear: [] };
// @ts-expect-error Track clears only accept the label field.
const invalidTrackClear: TrackSetArgs = { values: {}, clear: ["volume"] };

void [
  health, handshake, preference, mutation, mainReceiptFromCommit, commitReceiptFromMain,
  projectSequence, labeledTrack, clearedTrack, missingTrackFields, missingTrackClear,
  missingTrackValues, invalidTrackLabel, invalidTrackClear,
  operationIdentity, current, recovery, operationClient, retiredError,
];
