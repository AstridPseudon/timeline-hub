/**
 * A still, empty picture of the editor, drawn behind the connection cards so the person feels they are already in
 * the app and only one step from it. It has no Runtime behind it, takes no input and is hidden from assistive tech.
 * Geometry follows the real editor: a top bar, the preview, a timeline with a ruler and tracks, and the right pane.
 */
const AVATAR_SRC = '/astrid-favicon.svg';

function Bar({ className }: { className: string }) {
  return <div className={`rounded-md bg-muted ${className}`} />;
}

export function EmptyEditorShell() {
  return (
    <div aria-hidden="true" {...({ inert: '' } as object)} className="pointer-events-none absolute inset-0 flex select-none bg-background opacity-60">
      <div className="flex min-w-0 flex-1 flex-col">
        <div className="flex h-11 items-center gap-2 border-b border-border px-3">
          <img src={AVATAR_SRC} alt="" className="h-7 w-7" />
          <Bar className="h-7 w-36 border border-border bg-card" />
          <Bar className="h-7 w-7" />
          <Bar className="h-7 w-28 border border-border bg-card" />
        </div>
        <div className="flex min-h-0 flex-1 items-center justify-center p-6">
          <div className="aspect-video max-h-full w-full max-w-3xl rounded-lg border border-border bg-muted/60" />
        </div>
        <div className="h-48 shrink-0 space-y-2 border-t border-border bg-card/60 p-3">
          <div className="flex gap-6">
            {[0, 1, 2, 3, 4].map((tick) => <Bar key={tick} className="h-2 w-10 bg-muted/70" />)}
          </div>
          <div className="flex items-center gap-2"><Bar className="h-9 w-12" /><Bar className="h-9 flex-1 bg-muted/40" /></div>
          <div className="flex items-center gap-2"><Bar className="h-9 w-12" /><Bar className="h-9 flex-1 bg-muted/40" /></div>
          <div className="flex items-center gap-2"><Bar className="h-9 w-12" /><Bar className="h-9 flex-1 bg-muted/40" /></div>
        </div>
      </div>
      <div className="hidden w-[300px] shrink-0 flex-col border-l border-border bg-card/60 md:flex">
        <div className="space-y-2 border-b border-border p-3">
          <Bar className="h-9 w-full border border-border bg-card" />
        </div>
        <div className="flex-1 p-3"><Bar className="h-5 w-24" /></div>
        <div className="p-3"><Bar className="h-24 w-full border border-border bg-card" /></div>
      </div>
    </div>
  );
}
