/** Astrid metadata adapter; OMP owns registries and model-role persistence. */
import { writeFileSync } from "node:fs";
import { Settings } from "@oh-my-pi/pi-coding-agent/config/settings";
import {
	getModelMatchPreferences,
	pickDefaultAvailableModel,
	resolveAllowedModels,
	resolveModelRoleValue,
} from "@oh-my-pi/pi-coding-agent/config/model-resolver";
import { getOAuthProviders } from "@oh-my-pi/pi-ai/oauth";

type ListedModel = { id: string; name: string; selector: string };
type ListedProvider = { id: string; name: string; signedIn: boolean; models: ListedModel[] };
type Snapshot = {
	schemaVersion: 1;
	currentModel: string | null;
	providers: ListedProvider[];
	_catalogModel: string | null;
	_hiddenProviderIds: string[];
};

function fail(path: string, message: string): void {
	writeFileSync(path, JSON.stringify({ error: message }));
	process.exitCode = 1;
}

async function makeSnapshot(ctx: any, settings: any): Promise<Snapshot> {
	const registry = ctx.modelRegistry;
	const allModels = registry.getAll();
	const enabledModels = await resolveAllowedModels(registry, settings, getModelMatchPreferences(settings));
	const oauthProviders = getOAuthProviders();
	const oauthById = new Map(oauthProviders.map((provider: any) => [provider.id, provider]));
	const disabled = new Set<string>(settings.get("disabledProviders") ?? []);
	const hiddenProviderIds = new Set(disabled);
	for (const oauth of oauthProviders as any[]) {
		if (oauth.storeCredentialsAs && disabled.has(oauth.storeCredentialsAs)) hiddenProviderIds.add(oauth.id);
	}
	const providerIds = new Set<string>([
		...allModels.map((model: any) => model.provider),
		...registry.getDiscoverableProviders(),
		...oauthProviders.map((provider: any) => provider.id),
	]);
	const providers: ListedProvider[] = [...providerIds]
		.filter(id => {
			const oauth = oauthById.get(id) as any;
			return !disabled.has(id) && !(oauth?.storeCredentialsAs && disabled.has(oauth.storeCredentialsAs));
		})
		.sort((a, b) => a.localeCompare(b))
		.map(id => {
			const oauth = (oauthById.get(id) ?? oauthProviders.find((provider: any) => provider.storeCredentialsAs === id)) as any;
			const models = enabledModels
				.filter((model: any) => model.provider === id)
				.map((model: any) => ({ id: model.id, name: model.name, selector: `${model.provider}/${model.id}` }))
			.sort((a: ListedModel, b: ListedModel) => a.id.localeCompare(b.id));
			const hasAuth = registry.authStorage.hasAuth(id) || oauthProviders.some((provider: any) =>
				(provider.id === id || provider.storeCredentialsAs === id) &&
				registry.authStorage.hasAuth(provider.storeCredentialsAs ?? provider.id),
			);
			return { id, name: oauth?.name ?? id, signedIn: hasAuth, models };
		});

	const preferences = getModelMatchPreferences(settings);
	const defaultRole = settings.getModelRole("default");
	const resolvedDefault = defaultRole
		? resolveModelRoleValue(defaultRole, enabledModels, { settings, matchPreferences: preferences }).model
		: undefined;
	const fallback = resolvedDefault
		? undefined
		: pickDefaultAvailableModel(enabledModels.filter((model: any) => registry.hasConfiguredAuth(model)));
	const selected = resolvedDefault ?? fallback;
	return {
		schemaVersion: 1,
		currentModel: selected ? `${selected.provider}/${selected.id}` : null,
		providers,
		_catalogModel: allModels[0] ? `${allModels[0].provider}/${allModels[0].id}` : null,
		_hiddenProviderIds: [...hiddenProviderIds].sort((a, b) => a.localeCompare(b)),
	};
}

export default function register(pi: any): void {
	pi.on("session_shutdown", async (_event: unknown, ctx: any) => {
		const resultPath = process.env.ASTRID_OMP_MODELS_RESULT;
		if (!resultPath) throw new Error("ASTRID_OMP_MODELS_RESULT is required");

		const requestedRaw = process.env.ASTRID_OMP_MODEL_SELECTION;
		const settingsForRead = await Settings.loadReadOnly({ cwd: ctx.cwd });
		if (requestedRaw === undefined) {
			writeFileSync(resultPath, JSON.stringify(await makeSnapshot(ctx, settingsForRead)));
			return;
		}
		const requested = requestedRaw.trim();
		if (!requested) {
			fail(resultPath, "Invalid model selector; use provider/model-id");
			return;
		}

		const separator = requested.indexOf("/");
		const providerId = separator < 0 ? requested : requested.slice(0, separator);
		const modelId = separator < 0 ? undefined : requested.slice(separator + 1);
		if (!providerId || requested.includes("\\")) {
			fail(resultPath, "Invalid model selector; use provider/model-id");
			return;
		}
		const snapshot = await makeSnapshot(ctx, settingsForRead);
		const provider = snapshot.providers.find(entry => entry.id === providerId);
		if (provider && !provider.signedIn && provider.models.length === 0) {
			fail(resultPath, `Sign in: run \`omp\`, then /login and pick ${provider.name}`);
			return;
		}
		if (!modelId) {
			fail(resultPath, "Invalid model selector; use provider/model-id");
			return;
		}
		const model = provider?.models.find(entry => entry.selector === requested || entry.id === modelId);
		if (!model) {
			fail(resultPath, "Unknown or unavailable model selector");
			return;
		}

		const settingsForWrite = await Settings.init({ cwd: ctx.cwd });
		if (settingsForWrite.get("modelRoleStorage") === "project") settingsForWrite.setProjectModelRole("default", model.selector);
		else settingsForWrite.setModelRole("default", model.selector);
		await settingsForWrite.flush();

		const enabled = await resolveAllowedModels(ctx.modelRegistry, settingsForWrite, getModelMatchPreferences(settingsForWrite));
		const verified = resolveModelRoleValue(settingsForWrite.getModelRole("default"), enabled, {
			settings: settingsForWrite,
			matchPreferences: getModelMatchPreferences(settingsForWrite),
		}).model;
		if (!verified || `${verified.provider}/${verified.id}` !== model.selector) {
			fail(resultPath, "Selected model did not resolve as the default model");
			return;
		}
		writeFileSync(resultPath, JSON.stringify(await makeSnapshot(ctx, settingsForWrite)));
	});
}
