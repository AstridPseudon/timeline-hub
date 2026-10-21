# Draft voiceover synchronization action

The V3 action retains its eight inputs. It compares pinned script occurrences
with managed draft-audio provenance and requests changed speech through the
existing `generation.generate_speech` pipeline. Native capture prepares commands
from the settled five-field media selection and verified intrinsic duration.

The outer managed Python invocation supplies its task, attempt, executor, fence,
runtime epoch, admitted publication target, and output directory privately.
Caller inputs, client attributes, environment variables, and inner speech
identities cannot supply this context. Missing or inconsistent context refuses.
The action remains `network: false`.

For a changed result, the action writes the existing six-key proposal to
`authoring-proposal.json` and declares it in the standard result manifest as
`authoring_proposal`, with artifact type `timeline/authoring-proposal`. It
returns the proposal as action data. For `plan_only` and `unchanged`, it
instead writes the successful advisory result to `report.json` and declares
that report as the result. Those paths do not invent commands, a receipt, or a
publication. It never publishes a revision or renders video.
The requester queues the settled proposal with `TimelineSession.queue_proposal`
and flushes through its durable outbox; accepted publication enables guarded undo.

The shared public helper retains its original publication behavior. The action
calls the separate private managed-proposal entry, which preserves its
advisory plan/unchanged results and only settles a proposal for a real changed
case. Legacy audio adoption remains explicit through
`adopt_clip_ids`; locked, final, and recorded narration remains protected.
