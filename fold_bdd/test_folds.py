import funcy as fn
from itertools import combinations_with_replacement as combinations

try:
    from dd.cudd import BDD
except ImportError:
    from dd.autoref import BDD

from fold_bdd import post_order


def test_post_order():
    @fn.memoize
    def merge1(ctx, low=None, high=None):
        return 1 if low is None else low + high

    manager = BDD()
    manager.add_var('x')
    manager.add_var('y')
    bexpr = manager.add_expr('x & y')

    val = post_order(bexpr, merge1)
    assert val == bexpr.dag_size

    # Convert BDD to function.
    def merge2(ctx, low=None, high=None):
        if low is None:
            return lambda _: ctx.node_val

        def _eval(vals):
            val, *vals2 = vals
            out = high(vals2) if val else low(vals2)
            return ctx.negated ^ out

        return _eval

    _eval = post_order(bexpr, merge2)
    for vals in combinations([True, False], 2):
        assert all(vals) == _eval(vals)

    def merge3(ctx, low, high):
        prev_lvl = -1 if ctx.prev_lvl is None else ctx.prev_lvl
        count = 2**(ctx.curr_lvl - prev_lvl - 1)
        if low is None:
            return count if ctx.node_val else 0

        return (low + high)*count

    bexpr2 = manager.add_expr('x | y')

    assert post_order(bexpr, merge3) == 1
    assert post_order(bexpr2, merge3) == 3
    assert False
