import funcy as fn


def reduce_bdd(node, merge, *, manager=None, prev_lvl=-1):
    if manager is None:
        manager = node.bdd

    val = node.var
    if val is None:  # Must be a leaf True xor False node.
        return merge(val=(node == manager.true))

    def _reduce(c):
        return reduce_bdd(c, merge, manager=manager, prev_lvl=node.level)

    low, high = fn.map(_reduce, (node.low, node.high))

    return merge(
        val=val, negated=node.negated,
        high=high, high_lvl=node.high.level, low=low, low_lvl=node.low.level,
    )
