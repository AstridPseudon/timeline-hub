"""Server-only replay of the original captured intent on an accepted head."""
from __future__ import annotations

from .commands import execute
from .inverse import check_intervening


def replay(plan, head_bundle, *, intervening_records=(), inverse_records=(), id_map=None, closures=None,
           verified_media=()):
    check_intervening(plan.records, intervening_records,
                      identities_only=all(command['op'] not in ('timeline.inverse', 'timeline.restore')
                                          for command in plan.commands))
    return execute(head_bundle, plan.commands, inverse_records=inverse_records,
                   intervening_records=intervening_records, id_map=id_map, closures=closures,
                   verified_media=verified_media)
