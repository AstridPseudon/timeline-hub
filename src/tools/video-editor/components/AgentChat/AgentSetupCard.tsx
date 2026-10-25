import { useCallback, useEffect, useRef, useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { Loader2 } from 'lucide-react';
import { AstridLocalClient } from '@/integrations/astrid/client.ts';
import { isAgentSetupError } from '@/integrations/astrid/acpRoutes.ts';
import { BridgeRouteError } from '@/integrations/astrid/transport.ts';
import { AGENT_CHAT_COPY as copy } from '@/integrations/astrid/chatCopy.ts';
import { LOCAL_AGENT_IDS, type LocalAgentChoice, type LocalAgentId } from '@/integrations/astrid/localAgents.ts';
import { Button } from '@/shared/components/ui/button.tsx';
import { AgentIcon, agentNames, isAgentUsable } from './agentIdentity';
import { CommandLine, CommandStep } from './CommandLine';
import { readNewChatChoice, rememberNewChatChoice } from './newChatThinkingSelection';

// Saving a key validates it with OpenRouter and lists models afterwards, which can take longer than a read.
const client = new AstridLocalClient({ projectSlug: 'astrid-acp', timeoutMs: 120_000 });
// ACP model ids are provider/model selectors; the catalog lists bare ids per provider.
const selectorOf = (providerId: string, modelId: string) => `${providerId}/${modelId}`;
const setupName = (agent: LocalAgentId) => agent === 'astrid' ? copy.astridAgent : agentNames[agent];
const setupState = (agent: LocalAgentChoice | undefined) => JSON.stringify([agent?.state, agent?.signIn, agent?.steps?.map(({ kind, command, label }) => [kind, command, label])]);

type Props = {
  agents: LocalAgentChoice[];
  defaultAgent: LocalAgentId;
  initialAgent?: LocalAgentId;
  initialError?: unknown;
  refetchAgents: () => Promise<unknown> | unknown;
  startChatWith: (agent: LocalAgentId, model?: string, isCurrent?: () => boolean) => Promise<{ error?: unknown; sessionId?: string | null } | void>;
  onSetup?: (agent: LocalAgentId) => void;
  onComplete: (agent: LocalAgentId, sessionId?: string | null) => void;
};

function status(agent: LocalAgentChoice | undefined, id: LocalAgentId) {
  if (id === 'astrid' && (!isAgentUsable(agent) || agent?.signIn === 'unknown')) return copy.setUp;
  if (agent?.state === 'not-installed') return copy.notInstalled;
  if (agent?.state === 'sign-in' || agent?.signIn === 'signed-out') return copy.signIn;
  return isAgentUsable(agent) ? agent?.signIn === 'unknown' ? copy.checkSignIn : copy.ready : copy.setUp;
}

/** Inline setup owns its steps; AgentChat owns session creation and recovery. */
export function AgentSetupCard({ agents, defaultAgent, initialAgent, initialError, refetchAgents, startChatWith, onSetup, onComplete }: Props) {
  const [selected, setSelected] = useState<LocalAgentId>(() => {
    const last = readNewChatChoice()?.agent ?? defaultAgent;
    return initialAgent ?? (isAgentUsable(agents.find(agent => agent.id === last)) ? last
      : LOCAL_AGENT_IDS.find(id => id !== 'astrid' && agents.some(agent => agent.id === id && agent.signIn === 'signed-in')) ?? 'astrid');
  });
  const [step, setStep] = useState<'choose' | 'setup' | 'starting' | 'failed'>(initialAgent ? 'setup' : 'choose');
  const [agentFailure, setAgentFailure] = useState({ agent: initialAgent ?? selected, error: initialError });
  const failure = agentFailure.agent === selected ? agentFailure.error : null;
  const [failedRow, setFailedRow] = useState(() => initialError ? { id: initialAgent, state: setupState(agents.find(row => row.id === initialAgent)) } : null);
  const [showStartingBack, setShowStartingBack] = useState(false);
  const [search, setSearch] = useState('');
  const [chosenModel, setChosenModel] = useState<string | null>(null);
  const [checkingKey, setCheckingKey] = useState(false);
  const [keyError, setKeyError] = useState<string | null>(null);
  const keyInput = useRef<HTMLInputElement>(null);
  const rows = useRef<Partial<Record<LocalAgentId, HTMLDivElement | null>>>({});
  const inFlight = useRef(false);
  const attempt = useRef(0);
  const mounted = useRef(true);
  useEffect(() => { mounted.current = true; return () => { mounted.current = false; }; }, []);
  useEffect(() => {
    if (!initialAgent || inFlight.current) return;
    setSelected(initialAgent);
    if (initialError) {
      setAgentFailure({ agent: initialAgent, error: initialError });
      setFailedRow({ id: initialAgent, state: setupState(agents.find(row => row.id === initialAgent)) });
    }
    setStep('setup');
  }, [initialAgent, initialError]);
  const agent = agents.find(row => row.id === selected);
  const currentAgent = useRef(agent);
  currentAgent.current = agent;
  const canAdvance = failedRow?.id !== selected || failedRow.state !== setupState(agent);
  const models = useQuery({
    queryKey: ['agent-setup-models'], queryFn: () => client.acp.models(),
    enabled: step === 'setup' && selected === 'astrid', retry: false,
    refetchInterval: step === 'setup' && selected === 'astrid' ? 3000 : false,
    refetchOnWindowFocus: true,
  });
  const begin = useCallback(async (model?: string) => {
    if (inFlight.current) return;
    inFlight.current = true;
    const request = ++attempt.current;
    const isCurrent = () => mounted.current && request === attempt.current;
    setStep('starting');
    setAgentFailure({ agent: selected, error: null });
    try {
      const result = await startChatWith(selected, model, isCurrent);
      if (!isCurrent()) return;
      if (result?.error) throw result.error;
      await refetchAgents();
      if (!isCurrent()) return;
      rememberNewChatChoice({ agent: selected, ...(model ? { model } : {}) });
      onComplete(selected, result?.sessionId);
    } catch (error) {
      if (!isCurrent()) return;
      setAgentFailure({ agent: selected, error });
      setFailedRow({ id: selected, state: setupState(currentAgent.current) });
      if (isAgentSetupError(error)) {
        setStep('setup');
        void refetchAgents();
        if (selected === 'astrid') void models.refetch();
      } else setStep('failed');
    } finally { inFlight.current = false; }
  }, [models.refetch, onComplete, refetchAgents, selected, startChatWith]);

  const back = () => { attempt.current += 1; setStep('choose'); };
  useEffect(() => {
    setShowStartingBack(false);
    if (step !== 'starting') return;
    const timer = window.setTimeout(() => setShowStartingBack(true), 10_000);
    return () => window.clearTimeout(timer);
  }, [step]);

  useEffect(() => {
    if (step === 'choose') rows.current[selected]?.focus({ preventScroll: true });
  }, [step, selected]);
  useEffect(() => {
    if (step !== 'setup') return;
    const refresh = () => { void refetchAgents(); };
    const focus = () => { refresh(); if (selected === 'astrid') void models.refetch(); };
    const timer = window.setInterval(refresh, 3000);
    window.addEventListener('focus', focus);
    return () => { window.clearInterval(timer); window.removeEventListener('focus', focus); };
  }, [models.refetch, refetchAgents, selected, step]);
  useEffect(() => {
    if (failedRow?.id === selected && failedRow.state !== setupState(agent)) setFailedRow(null);
  }, [agent, failedRow, selected]);
  useEffect(() => {
    if (step === 'setup' && selected !== 'astrid' && canAdvance && isAgentUsable(agent)) void begin();
  }, [agent, begin, canAdvance, selected, step]);

  const providers = [...(models.data?.providers ?? [])].sort((a, b) => Number(b.signedIn) - Number(a.signedIn));
  const hasModels = providers.some(provider => provider.signedIn && provider.models.length > 0);
  const availableModels = providers.filter(provider => provider.signedIn)
    .flatMap(provider => provider.models.filter(item => `${provider.name} ${item.name} ${item.id}`.toLowerCase().includes(search.toLowerCase()))
      .map(item => ({ ...item, selector: selectorOf(provider.id, item.id) })));
  const modelId = chosenModel && availableModels.some(model => model.selector === chosenModel) ? chosenModel
    : (!chosenModel ? availableModels.find(model => model.selector === models.data?.currentModel)?.selector : undefined) ?? availableModels[0]?.selector;
  const model = availableModels.find(model => model.selector === modelId);
  const setupError = isAgentSetupError(failure);
  const steps = agent?.steps?.length ? agent.steps.filter(item => agent.state === 'not-installed' || item.kind === 'sign-in') : [];
  const instructions = <div className="space-y-2">
    {steps.length ? steps.map((item, index) => <CommandStep key={index} {...item} />)
      : failure instanceof BridgeRouteError && failure.nextAction ? <CommandStep command={failure.nextAction} label={copy.setUp} />
      : agent?.line ? <p><CommandLine line={agent.line} /></p> : null}
  </div>;
  const waiting = (text: string) => <p role="status" aria-live="polite" className="flex items-center gap-2 text-muted-foreground"><Loader2 aria-hidden="true" className="h-3.5 w-3.5 animate-spin" />{text}</p>;
  const errorMessage = failure instanceof BridgeRouteError ? failure.detail : failure instanceof Error ? failure.message : failure ? String(failure) : null;

  return <section aria-label={copy.setupTitle} className="space-y-3 rounded-lg border border-border p-3 text-sm">
    {step === 'choose' ? <>
      <h2 className="font-medium">{copy.setupTitle}</h2>
      <div role="listbox" aria-label={copy.setupTitle}>
        {LOCAL_AGENT_IDS.map((id, index) => {
          const row = agents.find(item => item.id === id);
          return <div key={id} ref={node => { rows.current[id] = node; }} role="option" aria-selected={selected === id} tabIndex={selected === id ? 0 : -1}
            className={`flex w-full items-center gap-2 rounded-md p-2 text-left hover:bg-muted focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring ${selected === id ? 'bg-muted' : ''}`}
            onFocus={() => setSelected(id)} onClick={() => { setSelected(id); setStep('setup'); onSetup?.(id); }}
            onKeyDown={event => {
              if (event.key === 'Enter' || event.key === ' ') { event.preventDefault(); setSelected(id); setStep('setup'); onSetup?.(id); return; }
              const next = event.key === 'ArrowDown' ? (index + 1) % LOCAL_AGENT_IDS.length : event.key === 'ArrowUp' ? (index + LOCAL_AGENT_IDS.length - 1) % LOCAL_AGENT_IDS.length : event.key === 'Home' ? 0 : event.key === 'End' ? LOCAL_AGENT_IDS.length - 1 : null;
              if (next !== null) { event.preventDefault(); setSelected(LOCAL_AGENT_IDS[next]); }
            }}>
            <AgentIcon agent={id} className="h-4 w-4 shrink-0" />
            <span className="min-w-0 flex-1"><span className="block">{setupName(id)}</span><span className="block text-xs text-muted-foreground">{id === 'astrid' ? copy.astridSubtitle : copy.computerSubtitle(agentNames[id])}</span>
              {id === 'astrid' && row?.creditLine && <span className="block text-xs text-muted-foreground">{row.creditUrl ? <a href={row.creditUrl} target="_blank" rel="noreferrer" className="underline" onClick={event => event.stopPropagation()} onKeyDown={event => event.stopPropagation()}>{row.creditLine}</a> : row.creditLine}</span>}
            </span><span className="text-xs text-muted-foreground">{status(row, id)}</span>
          </div>;
        })}
      </div>
    </> : step === 'starting' ? <>
      {waiting(copy.gettingReady(setupName(selected)))}<p className="text-xs text-muted-foreground">{copy.firstTime}</p>
      {showStartingBack && <button type="button" className="text-xs underline" onClick={back}>{copy.back}</button>}
    </> : <>
      <button type="button" className="text-xs underline" onClick={back}>{copy.back}</button>
      <h2 className="font-medium">{setupName(selected)}</h2>
      {errorMessage && <p role="alert">{errorMessage}</p>}
      {step === 'setup' && selected === 'astrid' && setupError && instructions}
      {step === 'failed' ? <Button onClick={() => void begin(selected === 'astrid' ? modelId : undefined)}>{copy.tryAgain}</Button>
        : selected !== 'astrid' ? <>{instructions}{waiting(agent?.state === 'not-installed' && setupError !== 'agent_sign_in_required' ? copy.waitingForAgent(agentNames[selected]) : copy.waitingForSignIn)}</>
        : models.isLoading ? waiting(copy.loadingModels)
        : hasModels ? <>
          <label className="block"><span className="sr-only">{copy.searchModels}</span><input type="search" value={search} onChange={event => setSearch(event.target.value)} placeholder={copy.searchModels} className="w-full rounded-md border border-input bg-background px-2 py-1" /></label>
          <div className="max-h-64 space-y-2 overflow-y-auto">
            {providers.map(provider => {
              const matches = provider.models.filter(item => `${provider.name} ${item.name} ${item.id}`.toLowerCase().includes(search.toLowerCase()));
              return matches.length ? <fieldset key={provider.id} disabled={!provider.signedIn}>
                <legend className="text-xs font-medium text-muted-foreground">{provider.name}</legend>
                {matches.map(item => { const selector = selectorOf(provider.id, item.id); return <label key={selector} className="flex items-center gap-2 py-1"><input type="radio" name="setup-model" value={selector} checked={modelId === selector} onChange={() => setChosenModel(selector)} />{item.name}</label>; })}
              </fieldset> : null;
            })}
          </div>
          <Button disabled={!model} onClick={() => void begin(modelId)}>{copy.useModel(model?.name ?? '')}</Button>
        </> : <>
          {models.error && <p role="alert">{copy.modelsFailed}</p>}
          <h3 className="font-medium">{copy.openRouterRecommendation}</h3>
          <form className="space-y-2" onSubmit={event => {
            event.preventDefault();
            if (checkingKey) return;
            if (!keyInput.current?.value.trim()) { setKeyError(copy.emptyKey); keyInput.current?.focus(); return; }
            const request = client.acp.saveAstridApiKey('openrouter', keyInput.current.value.trim());
            keyInput.current.value = '';
            setCheckingKey(true); setKeyError(null);
            void request.then(async () => { setChosenModel(null); await Promise.all([models.refetch(), refetchAgents()]); }).catch(error => {
              if (!mounted.current) return;
              setKeyError(error.code === 'invalid_key' ? copy.invalidKey : error.code === 'provider_unreachable' ? copy.providerUnreachable : error.detail ?? error.message);
            }).finally(() => { if (mounted.current) setCheckingKey(false); });
          }}>
            <label className="block">{copy.openRouterKey}<input ref={keyInput} type="password" placeholder={copy.openRouterPlaceholder} autoComplete="off" spellCheck={false} className="mt-1 w-full rounded-md border border-input bg-background px-2 py-1" /></label>
            <Button type="submit" disabled={checkingKey}>{copy.connect}</Button>
            {checkingKey && waiting(copy.checkingKey)}
            {keyError && <p role="alert">{keyError}</p>}
          </form>
          <p className="text-xs text-muted-foreground"><a href="https://openrouter.ai/keys" target="_blank" rel="noreferrer" className="underline">{copy.getOpenRouterKey}</a></p>
          <p className="text-xs text-muted-foreground">{copy.keyPrivacy}</p>
          <details className="space-y-2"><summary className="cursor-pointer">{copy.alternativeSignIn}</summary>{!setupError && instructions}{waiting(copy.waitingForSignIn)}</details>
        </>}
    </>}
  </section>;
}
