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

## Semantic valuation

`Formula` objects can be tested with a particular valuation, with the `is_satisfied()` method. This method takes
a valuation as a `dict` associating each proposition name (`str`) with a truth value (`bool`) and returns
wether the `Formula` is satisfied by the valuation.
Example:

```python
>>> from logicalpy import Formula
>>> test_formula = Formula.from_string("P & Q")
>>> test_formula.is_satisfied({"P": True, "Q": False})
False
>>> test_formula.is_satisfied({"P": True, "Q": True})
True
```
