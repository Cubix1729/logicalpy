# Semantic Functions

Semantics functions are contained in the [`semantics`](../api-reference/logicalpy/semantics.md) sub-module. They include:

## Satisfiability/Consistency Test

To check whether a formula a satisfiable, use the `is_satisfiable()` function.
For getting one satisfying assignment for the formula, use the `one_satisfying_valuation()` function.
For getting all of them, use the `all_satisfying_valuations()` function.
To check whether *several* formulae are jointly satisfiable, the function `are_jointly_satisfiable()` can be used.

Example:

```python
>>> from logicalpy import Formula
>>> from logicalpy.semantics import *
>>> # With one formula:
>>> test_formula = Formula.from_string("P -> Q")
>>> is_satisfiable(test_formula)
True
>>> one_satisfying_valuation(test_formula)
{'P': False, 'Q': False}
>>> all_satisfying_valuations(test_formula)
[{'P': False, 'Q': False}, {'P': False, 'Q': True}, {'P': True, 'Q': True}]
>>> # With several formulae:
>>> are_jointly_satisfiable(Formula.from_string("P <-> Q"), Formula.from_string("~P & Q"))
False
```

<br>

For a complete reference of the `semantics` sub-module, see the [corresponding API reference](../api-reference/logicalpy/semantics.md).
