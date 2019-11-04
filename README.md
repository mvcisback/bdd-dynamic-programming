# bdd-dynamic-programming
Library for performing dynamic programming over a Reduced Ordered
Decision Diagram.

[![Build Status](https://cloud.drone.io/api/badges/mvcisback/dfa/status.svg)](https://cloud.drone.io/mvcisback/dfa)
[![codecov](https://codecov.io/gh/mvcisback/dfa/branch/master/graph/badge.svg)](https://codecov.io/gh/mvcisback/dfa)
[![PyPI version](https://badge.fury.io/py/dfa.svg)](https://badge.fury.io/py/dfa)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT


# Installation

If you just need to use `bdd-dyn`, you can just run:

`$ pip install bdd-dyn`

For developers, note that this project uses the
[poetry](https://poetry.eustace.io/) python package/dependency
management tool. Please familarize yourself with it and then
run:

`$ poetry install`

# Usage

The `bdd_dyn` library supports two types of folds:

1. Folding over the DAG of a `BDD` starting at the True/False leaves
   and merging until the root. This fold combines the values of the
   children with the value of the current node and passes it to the
   parent.

2. Folding over a path in the DAG, starting at the root and moving the
   the corresponding leaf.

In both cases, local context such as the levels of the parent and
child nodes are passed in.

As input, each of these take in a bdd, from the
[dd](https://github.com/tulip-control/dd) library and function for
accumulating or merging.

The following example illustrates how to use `bdd_dyn` to count the
number of solutions to a predicate using `reduce_bdd` and evaluate a
path using `reduce_bdd_path`.

```python
from dd.cudd import BDD
from bdd_dyn import reduce_bdd, reduce_bdd_path

# Step 1. Get a BDD.
manager = BDD()
manager.add_var('x')
manager.add_var('y')
bdd = manager.add_expr('x | y')

# Step 2. Create merge function.
def merge(, **ignore_context):
    

```
