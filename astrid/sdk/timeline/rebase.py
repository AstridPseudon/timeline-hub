"""Server-only replay of the original captured intent on an accepted head."""
from __future__ import annotations

from ._command_state import State
from .commands import execute
from .inverse import check_intervening


def replay(plan, head_bundle, *, intervening_records=(), inverse_records=(), id_map=None, closures=None,
           verified_media=(), schema_inputs=(), realm_id=None, resolve_inputs=None,
           verified_producer=None):
    check_intervening(
        plan.records, intervening_records, state=State(head_bundle),
        identities_only=(all(command['op'] not in ('timeline.inverse', 'timeline.restore')
                             for command in plan.commands)
                         and not any(command['op'] == 'clip.move-set' for command in plan.commands)))
    from ._materialization import consume
    sources = {**(closures or {})}
    sources[plan.bundle['base_parent']['revision_id']] = plan.bundle
    return execute(consume(head_bundle, plan.records, closures=sources), plan.commands, inverse_records=inverse_records,
                   intervening_records=intervening_records, id_map=plan.id_map if id_map is None else id_map, closures=sources,
                   materializations=plan.records,
                   verified_media=verified_media, schema_inputs=schema_inputs, realm_id=realm_id,
                   resolve_inputs=resolve_inputs, verified_producer=verified_producer)
