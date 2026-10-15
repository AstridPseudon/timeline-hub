"""Requested scene answers from the existing warm owner, with a bounded cache.

Legacy planner queries remain distinct from final scene visibility queries.
"""
from __future__ import annotations

from collections import OrderedDict
import hashlib
import json
import math
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

    def query_scene(self, *, revision_digest, scene, frames):
        """Final requested-frame visibility/coverage/bounds through the existing owner."""
        return self._query(revision_digest=revision_digest, props={"scene": scene, "frames": frames}, frames=frames, scene=True)

    def query_track(self, *, revision_digest, spans, transitions, frames):
        """Return public queryTrackFrame records, including zero-opacity mounts."""
        return self._query(revision_digest=revision_digest,
            props={"spans": spans, "transitions": transitions, "frames": frames}, frames=frames)

    def _query(self, *, revision_digest, props, frames, scene=False):
        if (not isinstance(revision_digest, str) or not revision_digest
                or not isinstance(frames, (list, tuple)) or not 0 < len(frames) <= 120
                or any(type(frame) is not int or not 0 <= frame <= 2**53 - 1 for frame in frames)):
            raise FrameOwnerError("evaluation_inputs_invalid")
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
            if scene:
                for value in result:
                    if (value.get("coverage") not in {"COVERED", "DIP", "GAP", "UNKNOWN"}
                            or value.get("content") not in {"CONTENT", "EMPTY", "UNKNOWN", None}
                            or not isinstance(value.get("findings"), list)):
                        raise FrameOwnerError("evaluation_response_invalid")
                    for layer in value["layers"]:
                        if (not isinstance(layer, dict) or not isinstance(layer.get("clipId"), str)
                                or layer.get("visible") not in (True, False, "unknown")
                                or not isinstance(layer.get("bounds"), dict)
                                or layer["bounds"].get("status") not in {"known", "unknown"}
                                or not isinstance(layer.get("findings"), list)):
                            raise FrameOwnerError("evaluation_response_invalid")
                        opacity = layer.get("opacity")
                        if opacity is not None and (type(opacity) not in (int, float)
                                or not math.isfinite(opacity) or not 0 <= opacity <= 1):
                            raise FrameOwnerError("evaluation_response_invalid")
                        bounds = layer["bounds"]
                        if bounds["status"] == "known":
                            rect = bounds.get("rect")
                            if (not isinstance(rect, dict) or set(rect) != {"x", "y", "width", "height"}
                                    or any(type(v) not in (int, float) or not math.isfinite(v) for v in rect.values())
                                    or rect["width"] < 0 or rect["height"] < 0):
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
