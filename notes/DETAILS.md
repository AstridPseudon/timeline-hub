# WC8 details

No live caller was changed and no duplicate lines were removed. The exact
carrier gap is occurrence ownership:

1. `_retain_sheet` records a retained detached layer binding as
   `occurrence:<id>/clip:<id>`.
2. `NativeSheet.preview` permits omission only when the binding starts with
   `parent/clip:`.
3. The published `clip.delete` declaration/capture path accepts only
   `parent/clip:<id>` and refuses occurrence identities as unsupported
   ownership.

The existing local-only detached omission behavior is still required. With a
retained native artifact, `_duration_sheet` rejects a changed row set before
native preview; that boundary is left unchanged. The omission must not be
mapped to a fabricated parent identity.

The existing native parent omission, inverse/reload/retry, disjoint rebase,
and guarded membership refusal tests remain green in the targeted lane listed
in `../report.md`.
