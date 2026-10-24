"""Native per-user support paths for the Runtime.

The production default is intentionally boring and explicit.  Tests and local
development can inject ``home`` (or individual roots) without changing any
runtime behaviour.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import os

from runtime_protocol import platform


DATA_ROOT_ENV = "ASTRID_RUNTIME_DATA_ROOT"


@dataclass(frozen=True)
class RuntimePaths:
    home: Path
    app_support: Path
    runtime_support: Path
    catalog_path: Path
    discovery_path: Path
    credentials_dir: Path
    realms_dir: Path
    source_profiles_dir: Path
    instance_lock_path: Path
    bootstrap_lock_path: Path
    process_control_path: Path

    @classmethod
    def current(
        cls,
        home: Path | str | None = None,
        *,
        data_root: Path | str | None = None,
    ) -> "RuntimePaths":
        """Resolve the native per-user support paths without using the cwd.

        An explicit data root is used as supplied.
        """
        home_path = Path(home).expanduser() if home is not None else Path.home()
        configured_root = data_root if data_root is not None else os.environ.get(DATA_ROOT_ENV)
        if configured_root:
            app_support = Path(configured_root).expanduser()
            if not app_support.is_absolute():
                raise ValueError(f"{DATA_ROOT_ENV} must be an absolute path")
        else:
            app_support = platform.data_root(home_path)
        runtime = app_support / "runtime"
        return cls(
            home=home_path,
            app_support=app_support,
            runtime_support=runtime,
            catalog_path=runtime / "catalog.json",
            discovery_path=runtime / "discovery.json",
            credentials_dir=app_support / "credentials",
            realms_dir=runtime / "realms",
            source_profiles_dir=runtime / "source-profiles",
            instance_lock_path=runtime / "instance.lock",
            bootstrap_lock_path=runtime / "bootstrap.lock",
            process_control_path=runtime / "process-control.json",
        )

    @classmethod
    def sandbox(cls, root: Path | str) -> "RuntimePaths":
        """An injectable macOS-shaped fixture filesystem rooted at ``root``."""

        home = Path(root)
        return cls.current(home, data_root=home / "Library" / "Application Support" / "Astrid Runtime")

    def ensure_support_dirs(self) -> None:
        for directory in (
            self.app_support,
            self.runtime_support,
            self.credentials_dir,
            self.realms_dir,
            self.source_profiles_dir,
        ):
            platform.private_directory(directory)
