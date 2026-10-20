"""Server-only replay of the original captured intent on an accepted head."""
from __future__ import annotations

from ._command_state import State
from .commands import execute
from .inverse import check_intervening


def replay(plan, head_bundle, *, intervening_records=(), inverse_records=(), id_map=None, closures=None):
    check_intervening(plan.records, intervening_records, state=State(head_bundle))
    return execute(head_bundle, plan.commands, inverse_records=inverse_records,
                   intervening_records=intervening_records, id_map=id_map, closures=closures)
