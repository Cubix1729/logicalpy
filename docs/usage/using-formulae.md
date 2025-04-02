# Using Formulae

## Latex rendering

Formulae can be rendered as LaTex code, with the `as_latex()` method of `Formula` objects.
Example:

```python
>>> from logicalpy import Formula
>>> test_formula = Formula.from_string("(P -> (~P & P)) v Q")
>>> print(test_formula.as_latex())
$(P \to (\neg P \land P)) \lor Q$
```

The above LaTex would render as follow: $(P \to (\neg P \land P)) \lor Q$

## Formula Propositions

You can get the set of all the propositions of a formula (with every proposition represented by its name) with
the `propositions()` method of the `Formula` class:

```python
>>> from logicalpy import Formula
>>> test_formula = Formula.from_string("P -> Q")
>>> test_formula.propositions()
{'P', 'Q'}
```

## Semantic valuation

`Formula` objects can be tested with a particular valuation, with the `is_satisfied()` method. This method takes
a valuation as a `dict` associating each proposition name (`str`) with a truth value (`bool`) and returns
whether the `Formula` is satisfied by the valuation.
Example:

```python
>>> from logicalpy import Formula
>>> test_formula = Formula.from_string("P & Q")
>>> test_formula.is_satisfied({"P": True, "Q": False})
False
>>> test_formula.is_satisfied({"P": True, "Q": True})
True
```

<br>

For a complete reference of the `Formula` class, see the [API reference](../api-reference/logicalpy/base.md#logicalpy.base.Formula).
