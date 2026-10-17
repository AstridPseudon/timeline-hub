import { useEffect, useMemo, useRef } from "react";
import {
  createProjectTranscriptHost,
  type ProjectTranscriptHostInput,
} from "../lib/project-transcript-host.ts";

/** A source editing session follows its document owner, not render callbacks. */
export function useProjectTranscriptHost(
  input: ProjectTranscriptHostInput,
  owner: object,
  timelineId: string,
) {
  const latest = useRef(input);
  latest.current = input;
  const host = useMemo(
    () =>
      createProjectTranscriptHost({
        dataRef: input.dataRef,
        repository: input.repository,
        assets: input.assets,
        items: input.items,
        pendingWork: input.pendingWork,
        commitData: (...args) => latest.current.commitData(...args),
        flushPendingSave: () =>
          latest.current.flushPendingSave?.() ?? Promise.resolve(),
        editability: {
          checkTimeline: () =>
            latest.current.editability?.checkTimeline?.() ?? { allowed: true },
          check: (value) =>
            latest.current.editability?.check(value) ?? { allowed: true },
        },
        getTimelineLaneVisible: () =>
          latest.current.getTimelineLaneVisible?.() ?? false,
        setTimelineLaneVisible: (visible) =>
          latest.current.setTimelineLaneVisible?.(visible),
      }),
    // A provider may reuse its repository across timeline sessions.
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [input.dataRef, input.repository, input.assets, input.items, input.pendingWork, owner, timelineId],
  );
  useEffect(() => {
    host.start();
    void host.refreshSources();
    return () => host.dispose();
  }, [host]);
  return host;
}
