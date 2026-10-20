import type { ReactNode } from 'react';
import { useEffect, useRef, useState } from 'react';
import { AlertTriangle, Download, Play, Square } from 'lucide-react';
import { Button } from '@/shared/components/ui/button.tsx';
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from '@/shared/components/ui/dialog.tsx';
import { useTimelineChromeContext } from '@/tools/video-editor/hooks/timelineStore.ts';
import { mediaCrossOrigin } from '@/shared/lib/media/mediaCrossOrigin';

function diagnosticRecord(value: unknown): Record<string, unknown> | undefined {
  return value !== null && typeof value === 'object' && !Array.isArray(value)
    ? value as Record<string, unknown>
    : undefined;
}

function diagnosticText(value: unknown): string {
  if (typeof value === 'string') return value;
  try {
    return JSON.stringify(value);
  } catch {
    return String(value);
  }
}

/** Render button, render blocker message, and cancellation control. */
export function TimelineRenderControls({
  previewActionButtonClass,
  afterRenderControl,
}: {
  previewActionButtonClass: string;
  afterRenderControl?: ReactNode;
}) {
  const chrome = useTimelineChromeContext();
  const [playerOpen, setPlayerOpen] = useState(false);
  const [downloading, setDownloading] = useState(false);
  const [downloadError, setDownloadError] = useState<string | null>(null);
  const downloadAttemptRef = useRef(0);
  const { renderResultUrl, renderResultInfo } = chrome;
  const completedAt = renderResultInfo?.completedAt ?? null;
  const seenCompletion = useRef(completedAt);
  // A render that finishes while the editor is open shows the film once;
  // "Play last render" brings it back after closing.
  useEffect(() => {
    if (completedAt !== null && completedAt !== seenCompletion.current && renderResultUrl) {
      setPlayerOpen(true);
    }
    seenCompletion.current = completedAt;
  }, [completedAt, renderResultUrl]);
  useEffect(() => {
    setDownloading(false);
    setDownloadError(null);
    return () => { downloadAttemptRef.current += 1; };
  }, [renderResultInfo, renderResultUrl]);

  const download = async () => {
    const attempt = ++downloadAttemptRef.current;
    setDownloading(true);
    setDownloadError(null);
    try {
      await chrome.downloadRenderResult();
    } catch (error) {
      if (attempt === downloadAttemptRef.current) {
        setDownloadError(error instanceof Error ? error.message : 'Could not download render. Please try again.');
      }
    } finally {
      if (attempt === downloadAttemptRef.current) setDownloading(false);
    }
  };

  const hasResult = Boolean(renderResultUrl) && chrome.renderStatus !== 'rendering';
  const filename = chrome.renderResultFilename ?? 'timeline-render.mp4';
  const summary = renderResultInfo
    ? [
        renderResultInfo.revision !== null ? `Timeline version ${renderResultInfo.revision}` : null,
        new Date(renderResultInfo.completedAt).toLocaleString(),
      ].filter(Boolean).join(' · ')
    : filename;

  return (
    <>
      <Button
        type="button"
        size="sm"
        className={`gap-1.5 ${previewActionButtonClass}`}
        onClick={() => void chrome.startRender()}
        disabled={chrome.renderStatus === 'rendering'}
      >
        <Download className="h-3.5 w-3.5" />
        {chrome.renderStatus === 'rendering' && chrome.renderProgress
          ? `Render ${chrome.renderProgress.percent}%`
          : 'Render'}
      </Button>
      {afterRenderControl}
      {hasResult && (
        <Button
          type="button"
          size="sm"
          variant="outline"
          className={`gap-1.5 ${previewActionButtonClass}`}
          onClick={() => setPlayerOpen(true)}
        >
          <Play className="h-3 w-3" />
          Play last render
        </Button>
      )}
      {renderResultUrl && (
        <Dialog open={playerOpen} onOpenChange={setPlayerOpen}>
          <DialogContent className="max-w-3xl" data-video-editor-render-player="true">
            <DialogHeader>
              <DialogTitle>Rendered film</DialogTitle>
              <DialogDescription>{summary}</DialogDescription>
            </DialogHeader>
            <video
              key={renderResultUrl}
              src={renderResultUrl}
              crossOrigin={mediaCrossOrigin(renderResultUrl)}
              controls
              preload="metadata"
              className="max-h-[60dvh] w-full rounded bg-black"
              data-testid="timeline-render-player"
            />
            <div className="flex justify-end">
              <Button asChild size="sm" variant="outline" className="gap-1.5" disabled={downloading}>
                <a href={renderResultUrl} download={filename} aria-disabled={downloading} onClick={(event) => {
                  event.preventDefault();
                  if (!downloading) void download();
                }}>
                  <Download className="h-3.5 w-3.5" />
                  {downloading ? 'Downloading…' : 'Download'}
                </a>
              </Button>
            </div>
            {downloadError && <p role="alert" className="text-sm text-destructive">{downloadError}</p>}
          </DialogContent>
        </Dialog>
      )}
      {chrome.renderStatus === 'rendering' && chrome.activeRenderTaskId && (
        <Button
          type="button"
          size="sm"
          variant="outline"
          className={`gap-1.5 ${previewActionButtonClass}`}
          onClick={() => void chrome.cancelRender()}
          aria-label="Cancel render"
        >
          <Square className="h-3 w-3" />
          Cancel
        </Button>
      )}
      {chrome.renderStatus === 'error' && chrome.renderLog && (
        <div
          className="absolute right-0 top-full z-40 mt-1 max-h-[70vh] w-80 max-w-[calc(100vw-2rem)] overflow-y-auto rounded-md border border-red-500/30 bg-zinc-950/95 px-3 py-2 text-[11px] text-red-200 shadow-lg backdrop-blur-sm"
          data-video-editor-render-blocker="true"
        >
          <div className="flex items-start gap-1">
            <AlertTriangle className="mt-0.5 h-3 w-3 shrink-0" />
            <span>{chrome.renderLog.split('\n')[0]}</span>
          </div>
          {chrome.visualSeamReport && (
            <section className="mt-2 space-y-2 border-t border-red-500/20 pt-2" aria-label="Visual seam admission report">
              <p className="font-medium text-zinc-100">Visual boundary report</p>
              {chrome.visualSeamReport.boundaries.filter((boundary) => boundary.unacknowledgedRisk || boundary.structuralIssues.length > 0).map((boundary) => (
                <div key={boundary.frame} className="rounded border border-white/10 bg-white/5 px-2 py-1.5 text-zinc-200">
                  <p>Frame {boundary.frame} · {boundary.timeSeconds.toFixed(2)}s</p>
                  <p className="text-zinc-400">
                    {boundary.participants.map((participant) => participant.cue?.kind ?? participant.behavior).join(', ') || 'Boundary'}
                  </p>
                  {boundary.participants.map((participant) => (
                    <p key={`${participant.ownerId}:${participant.path.join('/')}:${participant.behavior}:${participant.cue?.kind ?? ''}:${participant.cue?.id ?? ''}:${participant.cue?.frame ?? ''}`} className="break-all text-zinc-500">
                      {participant.path.join(' / ')}
                    </p>
                  ))}
                  {boundary.structuralIssues.map((issue) => <p key={issue} className="text-red-300">{issue}</p>)}
                </div>
              ))}
              {chrome.visualSeamReport.structuralIssues.map((issue) => (
                <p key={issue} className="text-red-300">Structural issue: {issue}</p>
              ))}
              {chrome.visualSeamReport.opaqueElements.length > 0 && (
                <p className="text-amber-200">
                  Opaque visual elements ({chrome.visualSeamReport.opaqueElements.length}): {[...new Set(chrome.visualSeamReport.opaqueElements.map((element) => element.clipType))].join(', ')}
                </p>
              )}
              {(() => {
                const raw = chrome.visualSeamReport.rawDiagnostics;
                const rawBoundaries = Array.isArray(raw?.boundaries) ? raw.boundaries : [];
                const boundaryOpaquePaths = rawBoundaries.flatMap((item) => {
                  const paths = diagnosticRecord(item)?.opaquePaths;
                  return Array.isArray(paths) ? paths : [];
                });
                const opaquePaths = [...(Array.isArray(raw?.opaquePaths) ? raw.opaquePaths : []), ...boundaryOpaquePaths];
                const rawIssues = Array.isArray(raw?.structuralIssues) ? raw.structuralIssues : [];
                return (
                  <>
                    {opaquePaths.length > 0 && (
                      <div className="text-amber-200">
                        Opaque owner paths ({opaquePaths.length}):
                        {opaquePaths.slice(0, 12).map((path, index) => (
                          <p key={`${diagnosticText(path)}:${index}`} className="break-all text-zinc-400">{Array.isArray(path) ? path.join(' / ') : diagnosticText(path)}</p>
                        ))}
                        {opaquePaths.length > 12 && <p className="text-zinc-500">And {opaquePaths.length - 12} more. Expand Runtime details for the full report.</p>}
                      </div>
                    )}
                    {(rawIssues.length > 0 || opaquePaths.length > 0) && (
                      <details className="text-zinc-400">
                        <summary className="cursor-pointer">Runtime diagnostic details</summary>
                        <pre className="mt-1 whitespace-pre-wrap break-all">{diagnosticText({structuralIssues: rawIssues, opaquePaths})}</pre>
                      </details>
                    )}
                  </>
                );
              })()}
              {chrome.canDeclareSeamsAsHardCuts && (
                <Button type="button" size="sm" variant="outline" onClick={() => void chrome.declareSeamsAsHardCuts()}>
                  Declare flagged boundaries as hard cuts
                </Button>
              )}
              {chrome.canAcknowledgeVisualCues && (
                <Button type="button" size="sm" variant="outline" onClick={() => void chrome.acknowledgeVisualCuesAsSynchronized()}>
                  Acknowledge listed cues as synchronized
                </Button>
              )}
            </section>
          )}
        </div>
      )}
    </>
  );
}
