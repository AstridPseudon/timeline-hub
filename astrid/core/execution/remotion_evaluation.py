"""Requested planner frames from the existing host, with a bounded local cache.

Inputs are already compiled track spans/transitions. This is not a Python scene
evaluator or a visibility/coverage API. Role queries and reflow do not import it.
"""
from __future__ import annotations

from collections import OrderedDict
import hashlib
import json
from pathlib import Path
import tempfile
import threading

from .remotion_frame_owner import FrameOwnerError
from .remotion_host_session import _read, host_remotion_client


class RemotionEvaluationClient:
    def __init__(self, *, project_dir, node_executable, attempt_root, renderer_closure,
                 environment=None, port=31500):
        """Use a host-admitted task and a callable for its current renderer closure.

        Bind the existing renderer_environment_identity to the selected project
        in the caller. Recompute that identity on each query so component,
        package and font changes cannot reuse old answers. revision_digest must
        describe the relevant resolved timeline inputs, excluding unrelated edits.
        """
        if not callable(renderer_closure):
            raise TypeError("renderer_closure must supply the current admitted identity")
        self.project = Path(project_dir).resolve(strict=True)
        self.node = Path(node_executable).resolve(strict=True)
        self.attempt = Path(attempt_root).resolve(strict=True)
        self.closure = renderer_closure
        self.environment = dict(environment or {})
        self.port = port
        self._cache = OrderedDict()
        self._cache_bytes = 0
        self._lock = threading.RLock()

    def query_track(self, *, revision_digest, spans, transitions, frames):
        """Return public queryTrackFrame records, including zero-opacity mounts."""
        if (not isinstance(revision_digest, str) or not revision_digest
                or not isinstance(frames, (list, tuple)) or not 0 < len(frames) <= 120
                or any(type(frame) is not int or not 0 <= frame <= 2**53 - 1 for frame in frames)):
            raise FrameOwnerError("evaluation_inputs_invalid")
        props = {"spans": spans, "transitions": transitions, "frames": list(frames)}
        # Copy callers' mutable inputs before admission/cache lookup.
        encoded = json.dumps(props, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()
        if len(encoded) > 8 * 1024 * 1024:
            raise FrameOwnerError("frame_request_too_large")
        frames = json.loads(encoded)["frames"]
        with self._lock:
            closure = self.closure()
            if not isinstance(closure, str) or not closure:
                raise FrameOwnerError("renderer_closure_unavailable")
            key = hashlib.sha256(json.dumps([revision_digest, closure]).encode() + b"\0" + encoded).digest()
            if key in self._cache:
                self._cache.move_to_end(key)
                return json.loads(self._cache[key])
            client = host_remotion_client()
            if client is None:
                raise FrameOwnerError("frame_owner_unavailable")
            with tempfile.TemporaryDirectory(prefix="evaluation-", dir=self.attempt) as temporary:
                root = Path(temporary).resolve(strict=True)
                path = root / "props.json"
                path.write_bytes(encoded)
                request = {
                    "type": "evaluate", "projectDir": str(self.project),
                    "compositionId": "AstridTrackEvaluation", "nodeExecutable": str(self.node),
                    "remotionCli": str(self.project / "node_modules/@remotion/cli/remotion-cli.js"),
                    "propsPath": str(path), "outputDir": str(root / "unused-frames"),
                    "frames": list(frames), "resolution": None,
                    "port": self.port, "environment": dict(self.environment),
                }
                response = client.request(closure, request, _read)
            if not isinstance(response, dict) or response.get("ok") is not True:
                raise FrameOwnerError("evaluation_failed: " + str(response.get("error", "invalid reply")
                                      if isinstance(response, dict) else "invalid reply"))
            result = response.get("evaluation")
            if (not isinstance(result, list) or len(result) != len(frames)
                    or any(not isinstance(value, dict) or type(value.get("frame")) is not int
                           or value["frame"] != frame or not isinstance(value.get("layers"), list)
                           for value, frame in zip(result, frames))):
                raise FrameOwnerError("evaluation_response_invalid")
            if self.closure() != closure:
                raise FrameOwnerError("renderer_closure_changed_during_query")
            answer = json.dumps(result, separators=(",", ":"), allow_nan=False).encode()
            if len(answer) > 8 * 1024 * 1024:
                raise FrameOwnerError("evaluation_response_too_large")
            self._cache[key] = answer
            self._cache_bytes += len(answer)
            while len(self._cache) > 128 or self._cache_bytes > 8 * 1024 * 1024:
                _, retired = self._cache.popitem(last=False)
                self._cache_bytes -= len(retired)
            return json.loads(answer)
