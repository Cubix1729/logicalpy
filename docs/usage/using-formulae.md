# Using Formulae

## Latex Rendering

Formulae can be rendered as LaTex code, with the `to_latex()` method of `Formula` objects.
Example:

```python
>>> from logicalpy import Formula
>>> fml = Formula.from_string("(P -> (~P & P)) v Q")
>>> print(fml.to_latex())
$(P \to (\neg P \land P)) \lor Q$
```

The above LaTex would render as follow: $(P \to (\neg P \land P)) \lor Q$

## Formula Propositions

You can get the set of all the propositions of a formula (with every proposition represented by its name) with
the `propositions()` method of the `Formula` class:

```python
>>> from logicalpy import Formula
>>> fml = Formula.from_string("P -> Q")
>>> fml.propositions()
{'P', 'Q'}
```

## Semantic Valuation

`Formula` objects can be tested with a particular valuation, with the `is_satisfied()` method. This method takes
a valuation as a `dict` associating each proposition name (`str`) with a truth value (`bool`) and returns
whether the `Formula` is satisfied by the valuation.
Example:

```python
>>> from logicalpy import Formula
>>> fml = Formula.from_string("P & Q")
>>> fml.is_satisfied({"P": True, "Q": False})
False
>>> fml.is_satisfied({"P": True, "Q": True})
True
```

<br>

For a complete reference of the `Formula` class, see its [API reference](../api-reference/logicalpy/base.md#logicalpy.base.Formula).
