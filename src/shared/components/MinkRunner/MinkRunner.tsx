import './MinkRunner.css';

/**
 * Astrid's loading mark: the mink running in place over a streaming ground. Decorative only.
 *
 * `bootSize` draws it at the size of index.html's boot mink (180 device pixels wide) and marks it
 * `data-boot-mink-continue`: when the boot layer lifts onto a page that shows this mark (src/app/bootLayer.ts),
 * this one takes over the boot mink's stride in place instead of the two crossfading.
 */
export function MinkRunner({ className = '', bootSize = false }: { className?: string; bootSize?: boolean }) {
  return (
    <div
      className={`astrid-mink-runner ${bootSize ? 'astrid-mink-runner-boot' : ''} ${className}`}
      data-boot-mink-continue={bootSize ? '' : undefined}
      aria-hidden="true"
    >
      <span className="astrid-mink-runner-window"><span className="astrid-mink-runner-sprite" /></span>
      <span className="astrid-mink-runner-ground"><span /></span>
    </div>
  );
}
