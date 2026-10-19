/** Consumer imports resolve through the published package exports and declarations. */
import {
  CONTRACT_VERSION, WorkspaceClient,
  type Health, type Handshake, type PreferenceResource, type MutationResult,
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
void [health, handshake, preference, mutation, mainReceiptFromCommit, commitReceiptFromMain, projectSequence];
