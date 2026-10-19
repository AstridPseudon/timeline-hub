"""Same-interpreter owner for the profile helper launch recipe.

The receipt is diagnostic data, never a transferable custody capability.
Callers retain this object, and keep the interpreter alive on an unresolved
launch instead of turning its primary exception into a top-level traceback.
"""
from __future__ import annotations

import os
import threading
from pathlib import Path

from .custody_broker import _atomic_owner_json
from .process_group import popen_owned_group


class _ProfileLaunchOwner:
    def __init__(self, receipt: Path):
        self.receipt = receipt
        self.process = self.custody = None
        self.primary_error = self.cleanup_error = self.evidence_error = None
        self.cleanup_complete = False
        self._started = False

    def _persist_failure(self, phase):
        broker = getattr(self.custody, "_launch_broker", None)
        registration = getattr(broker, "registration", None) or {}
        identity = registration.get("identity") or {}
        root = getattr(self.custody, "root", None)
        journal = getattr(broker, "journal_path", None)
        _atomic_owner_json(self.receipt, {
            "version": "astrid.profile-launch-failure/v1", "authority": "NONE",
            "owner_pid": os.getpid(), "phase": phase,
            "process_pid": getattr(self.process, "pid", None),
            "process_birth_id": getattr(self.process, "_astrid_process_birth", None),
            "custody_root": str(root) if root is not None else None,
            "journal_path": str(journal) if journal is not None else None,
            "broker_phase": getattr(broker, "_observation_phase", None),
            "broker_state": getattr(broker, "state", None),
            "identity": {key: identity.get(key) for key in ("pid", "uid", "birth_id")},
            "primary_error_type": type(self.primary_error).__name__,
            "cleanup_error_type": type(self.cleanup_error).__name__ if self.cleanup_error else None,
            "cleanup_complete": self.cleanup_complete,
        })

    def _retain_before_cleanup(self, error):
        self.primary_error = error
        self.process, self.custody = error.process, error.custody
        try:
            self._persist_failure("before-cleanup")
        except BaseException as evidence_error:
            self.evidence_error = evidence_error
            raise

    def launch(self, argv, **kwargs):
        if self._started:
            raise RuntimeError("profile launch owner is single-use")
        self._started = True
        try:
            self.process = popen_owned_group(
                argv, _launch_failure_observer=self._retain_before_cleanup, **kwargs)
        except BaseException as error:  # noqa: BLE001 - retain the original live owner on every launch refusal
            # The actual admission exception owns these attachments. Never
            # reconstruct them from a PID, persisted record, or another owner.
            self.primary_error = error
            self.process = getattr(error, "process", None)
            self.custody = getattr(error, "custody", None)
            self.cleanup_error = getattr(error, "launch_cleanup_error", None)
            self.cleanup_complete = getattr(error, "launch_cleanup_complete", False)
            self.evidence_error = self.evidence_error or getattr(error, "launch_evidence_error", None)
            try:
                self._persist_failure("launch-refused")
            except BaseException as evidence_error:  # noqa: BLE001 - evidence failure cannot discard custody
                self.evidence_error = self.evidence_error or evidence_error
            self.keep_unresolved_owner()
            return None
        self.custody = getattr(self.process, "_astrid_custody", None)
        return self.process

    def keep_unresolved_owner(self):
        """Hold this original owner on refusal; no retry or recovery action."""
        if self.primary_error is None or self.process is None or self.cleanup_complete:
            return
        parked = threading.Event()
        while True:
            # Deliberate foreground retention, not a background service. Neither
            # elapsed time nor an interrupt creates authority to abandon custody.
            try:
                parked.wait()
            except (KeyboardInterrupt, SystemExit):
                continue
