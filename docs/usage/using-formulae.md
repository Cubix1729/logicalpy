# Using Formulae

## LaTeX Rendering

Formulae can be rendered as LaTeX code, with the `to_latex()` method of `Formula` objects.
Example:

```python
>>> from logicalpy import Formula
>>> fml = Formula.from_string("(P -> (~P & P)) v Q")
>>> print(fml.to_latex())
$(P \to (\neg P \land P)) \lor Q$
```

The above LaTeX would render as follow: $(P \to (\neg P \land P)) \lor Q$

## Equality testing

Two formulae can be tested for equality with the normal Python equality testing syntax.
Example:

```python
>>> from logicalpy import Formula
>>> Formula.from_string("A & B") == Formula.from_string("A -> C")
False
>>> Formula.from_string("A v (B v C)") == Formula.from_string("A | (B | C)")
True
```

!!! note
    This only tests if the propositions are ***exactly*** the same.
    For instance, two semantically equivalent formulae but with different structures will not
    be considered equal.
    Likewise, formulae with the same structure but with different proposition
    names will not be considered equal.

## Formula Propositions

You can get the set of all the propositions of a formula with every proposition represented by its
name (`str`) using the `propositions()` method of `Formula` objects:

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
