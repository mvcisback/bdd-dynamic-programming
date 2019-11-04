# Fold-BDD
Library for folding (or reducing) over a Reduced Ordered Binary Decision Diagram.

[![Build Status](https://cloud.drone.io/api/badges/mvcisback/dfa/status.svg)](https://cloud.drone.io/mvcisback/dfa)
[![codecov](https://codecov.io/gh/mvcisback/dfa/branch/master/graph/badge.svg)](https://codecov.io/gh/mvcisback/dfa)
[![PyPI version](https://badge.fury.io/py/dfa.svg)](https://badge.fury.io/py/dfa)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# Installation

If you just need to use `fold_bdd`, you can just run:

`$ pip install fold-bdd`

For developers, note that this project uses the
[poetry](https://poetry.eustace.io/) python package/dependency
management tool. Please familarize yourself with it and then
run:

`$ poetry install`

# Usage

The `fold-bdd` library supports two types of folds:

1. Folding over the DAG of a `BDD` starting at the root and then
   recursively merging the low and high branches until the
   `True`/`False` leaves. This is simply a compressed variant
   of a post-order traversal.

2. Folding over a path in the DAG, starting at the root and moving the
   the corresponding leaf.

In both cases, local context such as the levels of the parent and
child nodes are passed in.

As input, each of these take in a bdd, from the
[dd](https://github.com/tulip-control/dd) library and function for
accumulating or merging. 

The following example illustrates how to use `fold_bdd` to count the
number of solutions to a predicate using `post_order` and evaluate a
path using `fold_path`.

```python
from dd.cudd import BDD
from fold_bdd import post_order, fold_path

# Create BDD.
manager = BDD()
manager.add_var('x')
manager.add_var('y')
bexpr = manager.add_expr('x | y')


# Count number of solutions to bexpr.

def merge(ctx, low, high):
    prev_lvl = -1 if ctx.prev_lvl is None else ctx.prev_lvl
    count = 2**(ctx.curr_lvl - prev_lvl - 1)
    if low is None:
        return count if ctx.node_val else 0

    return (low + high)*count

def count_solutions(bexpr):
    return post_order(bexpr, merge)

assert count_solutions(bexpr) == 3
```
