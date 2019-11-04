import funcy as fn
from itertools import combinations_with_replacement as combinations

try:
    from dd.cudd import BDD
except ImportError:
    from dd.autoref import BDD

import bdd_dyn


def test_reduce():
    @fn.memoize
    def merge1(ctx, low=None, high=None):
        return 1 if low is None else low + high

    manager = BDD()
    manager.add_var('x')
    manager.add_var('y')
    bexpr = manager.add_expr('x & y')

    val = bdd_dyn.reduce_bdd(bexpr, merge1)
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

    _eval = bdd_dyn.reduce_bdd(bexpr, merge2)
    for vals in combinations([True, False], 2):
        assert all(vals) == _eval(vals)
