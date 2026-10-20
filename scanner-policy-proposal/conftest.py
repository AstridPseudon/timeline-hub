from __future__ import annotations

from pathlib import Path

import pytest


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption("--agent-root", action="store", required=True, help="extracted Agent checkout")


@pytest.fixture
def agent_root(request: pytest.FixtureRequest) -> Path:
    return Path(request.config.getoption("--agent-root")).resolve(strict=True)

