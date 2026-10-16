export type ProjectDraftSnapshot<T> = { text: string; queue: T[] };

export function sameProjectDraft<T>(left: ProjectDraftSnapshot<T>, right: ProjectDraftSnapshot<T>): boolean {
  return left.text === right.text && JSON.stringify(left.queue) === JSON.stringify(right.queue);
}

/** One local composer lifetime, retained while its last save finishes after unmount. */
export class ProjectChatDraftPersistence<T> {
  mounted = true;
  private chain: Promise<void> = Promise.resolve();
  private requested = 0;
  private acknowledgedThrough = 0;

  constructor(public revision: number, public saved: ProjectDraftSnapshot<T>) {}

  observe(revision: number, saved: ProjectDraftSnapshot<T>, local: ProjectDraftSnapshot<T>): void {
    // Never give divergent unsaved text a newer CAS token. Only an unchanged
    // base or an exact acknowledgement can safely advance this composer's base.
    if (revision > this.revision && (sameProjectDraft(saved, this.saved) || sameProjectDraft(saved, local))) {
      this.revision = revision;
      this.saved = saved;
      if (sameProjectDraft(saved, local)) this.acknowledgedThrough = this.requested;
    }
  }

  save(snapshot: ProjectDraftSnapshot<T>, write: (revision: number) => Promise<number>): Promise<void> {
    const request = ++this.requested;
    const pending = this.chain.catch(() => undefined).then(async () => {
      // An exact acknowledgement of newer local text supersedes older queued
      // snapshots; they must never overwrite that already durable text.
      if (request <= this.acknowledgedThrough || sameProjectDraft(snapshot, this.saved)) return;
      const revision = await write(this.revision);
      if (revision >= this.revision) {
        this.revision = revision;
        this.saved = snapshot;
      }
    });
    this.chain = pending;
    return pending;
  }
}
