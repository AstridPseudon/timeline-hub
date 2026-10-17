"""Host-retained transports for the admitted full-video Remotion command.

Nothing here is deserialized as authority. The existing authenticated stdio
bridge creates this owner and retains it until all original children settle.
"""

from __future__ import annotations

import hashlib
import json
import os
import socket
import stat
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

from astrid.core.rendering.assets import InvocationAssetServer


@dataclass(frozen=True)
class RetainedRendererProfile:
    """Exact Seatbelt bytes held outside every workload-writable scope.

    This is a Host-produced launch resource, never a task-selected profile.
    The enclosing attempt owns cleanup after its original children settle.
    """

    path: Path
    identity: tuple
    directory_identity: tuple
    sha256: str

    @classmethod
    def create(cls, profile: str, policy):
        attempt = policy.attempt_root.resolve(strict=True)
        directory = Path(tempfile.mkdtemp(prefix=".renderer-policy-", dir=attempt))
        # A workload must never be able to replace the policy before sandbox-exec
        # consumes it. Project writes and scratch are separate admitted scopes.
        writable = (*policy.project.write_roots, policy.private_write_root)
        if any(directory.is_relative_to(root.resolve(strict=True)) for root in writable):
            directory.rmdir()
            raise ValueError("renderer policy overlaps workload writes")
        path = directory / "profile.sb"
        payload = profile.encode("utf-8")
        try:
            fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o400)
            with os.fdopen(fd, "wb") as stream:
                stream.write(payload)
                stream.flush()
                os.fsync(stream.fileno())
                metadata = os.fstat(stream.fileno())
            owner = directory.stat()
            retained = cls(path, (metadata.st_dev, metadata.st_ino),
                           (owner.st_dev, owner.st_ino), hashlib.sha256(payload).hexdigest())
            retained.validate()
            return retained
        except BaseException:
            path.unlink(missing_ok=True)
            directory.rmdir()
            raise

    def validate(self):
        directory = self.path.parent
        owner = directory.lstat()
        if (not stat.S_ISDIR(owner.st_mode) or owner.st_uid != os.getuid()
                or stat.S_IMODE(owner.st_mode) != 0o700
                or (owner.st_dev, owner.st_ino) != self.directory_identity
                or directory.resolve(strict=True) != directory):
            raise ValueError("renderer policy directory changed")
        fd = os.open(self.path, os.O_RDONLY | os.O_NOFOLLOW)
        with os.fdopen(fd, "rb") as stream:
            metadata = os.fstat(stream.fileno())
            if (not stat.S_ISREG(metadata.st_mode) or metadata.st_uid != os.getuid()
                    or stat.S_IMODE(metadata.st_mode) != 0o400 or metadata.st_nlink != 1
                    or (metadata.st_dev, metadata.st_ino) != self.identity
                    or hashlib.file_digest(stream, "sha256").hexdigest() != self.sha256):
                raise ValueError("renderer policy file changed")


@dataclass(frozen=True)
class QualifiedRendererReads:
    """Exact read closure from completed launch validation, never task input."""

    closure: object
    environment: tuple
    attempt: Path
    claim: tuple
    roots: tuple
    literals: tuple
    platform_inputs: tuple

    @classmethod
    def admit(cls, *, closure, environment, policy):
        from astrid.core.rendering.remotion_runtime import _validated_runtime

        closure.validate(closure.project)
        entry = _validated_runtime(
            closure.project, environment=environment, python_executable=sys.executable
        )
        roots = {closure.project, closure.installed_project / "node_modules"}
        literals = {Path(environment["ASTRID_REMOTION_VALIDATION_PATH"])}
        # The admitted Darwin Node binary reads this fixed system input at
        # startup. No OPENSSL_CONF/environment selector is accepted.
        from .remotion_host_session import _file_identity

        openssl_config = Path('/System/Library/OpenSSL/openssl.cnf')
        platform_inputs = ((openssl_config, _file_identity(openssl_config)),)
        literals.add(openssl_config)
        observed = entry["closure"]
        roots.update(Path(raw) for raw in observed["package_roots"])
        literals.update(Path(raw) for raw in observed["module_files"])
        literals.update(Path(raw) for raw in observed["search_paths"])
        for side in ("renderer", "generator"):
            observed = entry["registry"][side]["observation"]
            roots.update(
                Path(raw)
                for raw in (*observed["roots"], *observed["package_roots"])
                if Path(raw).is_dir()
            )
            literals.update(
                Path(raw)
                for raw in (
                    *observed["module_files"],
                    *observed["optional_files"],
                    *observed["search_paths"],
                )
            )
        literals.update(
            Path(raw.removeprefix("startup:")) for raw in entry["inputs"]["startup_inventory"]
        )
        for row in entry["registry"]["outputs"]:
            literals.update((Path(row["path"]), Path(row["resolved"])))
        for path in (*roots, *literals):
            if (
                not path.is_absolute()
                or path == Path("/")
                or ".." in path.parts
                or any(ord(c) < 32 for c in str(path))
            ):
                raise ValueError("qualified renderer path is invalid")
        return cls(
            closure,
            tuple(environment.items()),
            policy.attempt_root,
            policy.claim_binding,
            tuple(sorted(roots)),
            tuple(sorted(literals)),
            platform_inputs,
        )

    def validate(self, policy):
        from astrid.core.rendering.remotion_runtime import _validated_runtime

        if policy.attempt_root != self.attempt or policy.claim_binding != self.claim:
            raise ValueError("qualified renderer read owner changed")
        self.closure.validate(self.closure.project)
        from .remotion_host_session import _file_identity

        if any(_file_identity(path) != identity for path, identity in self.platform_inputs):
            raise ValueError('renderer platform read input changed')
        _validated_runtime(
            self.closure.project,
            environment=dict(self.environment),
            python_executable=sys.executable,
        )
        return self.roots, self.literals


class RetainedRendererTransport:
    def __init__(self, *, bridge, closure, policy):
        bridge._guard()
        closure.validate(closure.project)
        self.bridge, self.closure, self.policy = bridge, closure, policy
        self.closed = False
        self.consumed = False
        self.services = {}
        self.browser = None
        self.browser_identity = None
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.bind(("127.0.0.1", 0))
            self.socket.listen(1024)
            self.address = self.socket.getsockname()
            self.identity = os.fstat(self.socket.fileno())
        except BaseException:
            self.socket.close()
            raise
        self.binding = hashlib.sha256(
            json.dumps(
                {
                    "bridge": bridge.digest,
                    "claim": policy.claim_binding,
                    "source": bridge.source_digest,
                    "closure": closure.receipt_digest,
                    "device": self.identity.st_dev,
                    "inode": self.identity.st_ino,
                    "endpoint": self.address,
                },
                sort_keys=True,
            ).encode()
        ).hexdigest()

    def validate(self, policy):
        if (
            self.closed
            or policy.attempt_root != self.policy.attempt_root
            or policy.claim_binding != self.policy.claim_binding
        ):
            raise ValueError("retained renderer owner or attempt changed")
        self.bridge._guard()
        self.closure.validate(self.closure.project)
        if self.browser is not None:
            from .remotion_host_session import _file_identity, _host_browser_executable

            if _host_browser_executable() != self.browser or _file_identity(self.browser) != self.browser_identity:
                raise ValueError('retained renderer browser input changed')
        current = os.fstat(self.socket.fileno())
        if (
            (current.st_dev, current.st_ino) != (self.identity.st_dev, self.identity.st_ino)
            or self.socket.family != socket.AF_INET
            or self.socket.getsockname() != self.address
            or self.socket.getsockopt(socket.SOL_SOCKET, socket.SO_TYPE) != socket.SOCK_STREAM
        ):
            raise ValueError("retained renderer socket changed")
        return (self.address[1], *(service.port for service in self.services.values()))

    def metadata(self):
        self.validate(self.policy)
        return dict(fd=0, host="127.0.0.1", port=self.address[1], binding=self.binding)

    def assets(self, root):
        self.validate(self.policy)
        root = self.bridge._artifact(root, exists=True)
        if not root.is_dir():
            raise ValueError("renderer asset root must be private staging")
        if root not in self.services:
            self.services[root] = InvocationAssetServer(
                root,
                allowed_origin=f"http://127.0.0.1:{self.address[1]}",
            ).start()
        return self.services[root].base_url

    def consume(self):
        self.validate(self.policy)
        if self.consumed:
            raise ValueError("retained renderer transport cannot be replayed")
        self.consumed = True
        return self.socket

    def select_browser(self):
        from .remotion_host_session import _file_identity, _host_browser_executable

        self.validate(self.policy)
        browser = _host_browser_executable()
        if browser is None:
            raise ValueError('retained browser transport requires installed Darwin Chrome')
        if self.browser is not None and browser != self.browser:
            raise ValueError('retained renderer browser changed')
        self.browser = browser
        self.browser_identity = _file_identity(browser)
        return browser

    def close(self):
        if self.closed:
            return
        # Called only after the existing bridge proves original child waits.
        for service in self.services.values():
            service.close()
        self.socket.close()
        self.closed = True


class RelayInvocationAssetServer:
    """Backend facade for the existing Host-owned InvocationAssetServer."""

    def __init__(self, client, staging_dir, *, allowed_origin):
        self.client = client
        self.staging_dir = Path(staging_dir).resolve(strict=True)
        self.base_url = None

    def __enter__(self):
        self.base_url = self.client.request("renderer_assets", {"root": str(self.staging_dir)})
        return self

    def local_url(self, path):
        from urllib.parse import quote

        path = Path(path).resolve(strict=True)
        if not path.is_file() or not path.is_relative_to(self.staging_dir) or self.base_url is None:
            raise ValueError("asset is outside invocation-private staging")
        return self.base_url + "/" + quote(path.relative_to(self.staging_dir).as_posix(), safe="/")

    def local_urls(self, assets):
        return {
            key: self.local_url(asset.local_path)
            for key, asset in assets.items()
            if asset.local_path is not None
        }

    def __exit__(self, *args):
        # Host retains service ownership through native child settlement, even
        # when the backend exits or its transport disappears during revocation.
        return None
