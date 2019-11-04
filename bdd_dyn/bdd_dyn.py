from typing import Union, Optional

import attr


@attr.s(auto_attribs=True, frozen=True)
class Context:
    node_val: Union[str, bool]
    negated: bool
    prev_lvl: Optional[int] = None
    low_lvl: Optional[int] = None
    high_lvl: Optional[int] = None
    curr_lvl: Optional[int] = None


def reduce_bdd(node, merge, *, manager=None, prev_lvl=None):
    if manager is None:
        manager = node.bdd

    ctx = Context(node_val=node.var, negated=node.negated, prev_lvl=prev_lvl)

    if ctx.node_val is None:
        ctx = attr.evolve(ctx, node_val=(node == manager.true))
        return merge(ctx=ctx, low=None, high=None)
    else:
        ctx = attr.evolve(
            ctx,
            low_lvl=node.low.level,
            high_lvl=node.high.level,
            curr_lvl=node.level,
        )

    def _reduce(c):
        return reduce_bdd(c, merge, manager=manager, prev_lvl=node.level)

    return merge(ctx=ctx, high=_reduce(node.high), low=_reduce(node.low))
