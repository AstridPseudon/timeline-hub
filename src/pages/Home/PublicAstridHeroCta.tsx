import { useEffect, useState } from 'react';
import { ArrowDownToLine } from 'lucide-react';
import { PublicAstridInstallDialog, SET_UP_ASTRID_COPY } from './PublicAstridInstallDialog';

/** The hero routes both audiences to the same OS-aware setup instructions. */
export function PublicAstridHeroCta({ active = true }: { active?: boolean }) {
  const [installOpen, setInstallOpen] = useState(false);
  useEffect(() => { if (!active) setInstallOpen(false); }, [active]);
  return (
    <>
      <div className="astrid-hero-cta">
        <button
          className="astrid-button astrid-button-primary"
          type="button"
          data-active={active}
          aria-hidden={!active}
          aria-haspopup="dialog"
          tabIndex={active ? undefined : -1}
          onClick={() => setInstallOpen(true)}
        >
          <span>{SET_UP_ASTRID_COPY.title}</span>
          <ArrowDownToLine size={17} aria-hidden="true" />
        </button>
      </div>
      <PublicAstridInstallDialog open={installOpen && active} onClose={() => setInstallOpen(false)} />
    </>
  );
}
