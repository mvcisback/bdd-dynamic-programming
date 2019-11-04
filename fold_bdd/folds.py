from typing import Union, Optional

import attr


@attr.s(auto_attribs=True, frozen=True)
class Context:
    node_val: Union[str, bool]
    negated: bool
    max_lvl: int
    prev_lvl: Optional[int] = None
    low_lvl: Optional[int] = None
    high_lvl: Optional[int] = None
    curr_lvl: Optional[int] = None


def post_order(node, merge, *, manager=None, prev_lvl=None):
    if manager is None:
        manager = node.bdd

    ctx = Context(
        node_val=node.var, negated=node.negated,
        prev_lvl=prev_lvl, max_lvl=len(manager.vars),
    )

    if ctx.node_val is None:
        ctx = attr.evolve(
            ctx, node_val=(node == manager.true), curr_lvl=ctx.max_lvl
        )
        return merge(ctx=ctx, low=None, high=None)
    else:
        ctx = attr.evolve(
            ctx,
            low_lvl=node.low.level,
            high_lvl=node.high.level,
            curr_lvl=node.level,
        )

    def _reduce(c):
        return post_order(c, merge, manager=manager, prev_lvl=node.level)

    return merge(ctx=ctx, high=_reduce(node.high), low=_reduce(node.low))
