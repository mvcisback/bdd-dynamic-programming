import funcy as fn
from itertools import combinations_with_replacement as combinations

try:
    from dd.cudd import BDD
except ImportError:
    from dd.autoref import BDD

import bdd_dyn


def test_reduce():
    @fn.memoize(key_func=lambda val, **_: val)
    def merge(low=None, high=None, **_):
        return 1 if low is None else low + high

    manager = BDD()
    manager.add_var('x')
    manager.add_var('y')
    bexpr = manager.add_expr('x & y')

    val = bdd_dyn.reduce_bdd(bexpr, merge)
    assert val == bexpr.dag_size

    # Convert BDD to function.
    def merge(val, low=None, high=None, negated=False, **_):
        if low is None:
            return lambda _: val

        def _eval(vals):
            val, *vals2 = vals
            out = high(vals2) if val else low(vals2)
            return negated ^ out

        return _eval

    _eval = bdd_dyn.reduce_bdd(bexpr, merge)
    for vals in combinations([True, False], 2):
        assert all(vals) == _eval(vals)
