import { useEffect, useState } from 'react';
import { ArrowRight } from 'lucide-react';
import { APP_ENTRY_PATH, rememberAppEntryPreference } from '@/app/entryClassification.ts';
import { PublicAstridInstallDialog } from './PublicAstridInstallDialog';

/** The first visit starts with the browser-only welcome; installation remains optional. */
export function PublicAstridHeroCta({ active = true }: { active?: boolean }) {
  const [installOpen, setInstallOpen] = useState(false);
  useEffect(() => { if (!active) setInstallOpen(false); }, [active]);
  return (
    <>
      <div className="astrid-hero-cta">
        <a className="astrid-button astrid-button-primary" href={APP_ENTRY_PATH}
          data-active={active} aria-hidden={!active} tabIndex={active ? undefined : -1}
          onClick={rememberAppEntryPreference}>
          <span>Try Astrid</span><ArrowRight size={17} aria-hidden="true" />
        </a>
        <button className="astrid-button" type="button" data-active={active}
          aria-hidden={!active} aria-haspopup="dialog" tabIndex={active ? undefined : -1}
          onClick={() => setInstallOpen(true)}>Get the app</button>
      </div>
      <PublicAstridInstallDialog open={installOpen && active} onClose={() => setInstallOpen(false)} />
    </>
  );
}
