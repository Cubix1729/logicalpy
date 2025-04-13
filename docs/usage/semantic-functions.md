# Semantic Functions

Semantics functions are contained in the [`semantics`](../api-reference/logicalpy/semantics.md) sub-module. They include:

## Truth tables

Truth tables can be built using the `TruthTable` class. Then, the string representation of the truth table
can be found with the `to_str` method (or directly with the `str` built-in constructor).
You can also use the `to_latex()` or `to_markdown()` methods to render the truth table to LaTex or Markdown.

Example:

```python
>>> from logicalpy import Formula
>>> from logicalpy.semantics import TruthTable
>>> fml = Formula.from_string("P v (~Q & ~P)")
>>> truth_table = TruthTable(fml)
>>> print(truth_table)
P    Q    P ∨ (¬Q ∧ ¬P)
---  ---  ---------------
T    T    T
T    F    T
F    T    F
F    F    T
>>> print(truth_table.to_latex())
\begin{tabular}{c|c|c}
 P   & Q   & $P \lor (\neg Q \land \neg P)$   \\
\hline
 T   & T   & T                                \\
 T   & F   & T                                \\
 F   & T   & F                                \\
 F   & F   & T                                \\
\end{tabular}
>>> print(truth_table.to_markdown())
| P   | Q   | P ∨ (¬Q ∧ ¬P)   |
|-----|-----|-----------------|
| T   | T   | T               |
| T   | F   | T               |
| F   | T   | F               |
| F   | F   | T               |
```

The above Markdown renders as follow:

| P   | Q   | P ∨ (¬Q ∧ ¬P)   |
|-----|-----|-----------------|
| T   | T   | T               |
| T   | F   | T               |
| F   | T   | F               |
| F   | F   | T               |

!!! note

    The LaTex code generated for a truth table uses the `tabular` environment, and it cannot be rendered using MathJax, but only
    using a pure LaTex compiler. Here is how the above LaTex code generated would render:

    ![LaTex rendering](./truth_table_latex_example.svg){: style="height:122px;width:238px"}
    <!---I doubled the dimentions of the image (w=119 and h=61) -->


## Satisfiability/consistency test

To check whether a formula is satisfiable, use the `is_satisfiable()` function.
For getting one satisfying assignment for the formula, use the `one_satisfying_valuation()` function.
For getting all of them, the `all_satisfying_valuations()` function can be used.
To check whether *several* formulae are jointly satisfiable, use the function `are_jointly_satisfiable()`.

Example:

```python
>>> from logicalpy import Formula
>>> from logicalpy.semantics import *
>>> # With one formula:
>>> fml = Formula.from_string("P -> Q")
>>> is_satisfiable(fml)
True
>>> one_satisfying_valuation(fml)
{'P': False, 'Q': False}
>>> all_satisfying_valuations(fml)
[{'P': False, 'Q': False}, {'P': False, 'Q': True}, {'P': True, 'Q': True}]
>>> # With several formulae:
>>> are_jointly_satisfiable(Formula.from_string("P <-> Q"), Formula.from_string("~P & Q"))
False
```

<br>

For a complete reference of the `semantics` sub-module, see the [corresponding API reference](../api-reference/logicalpy/semantics.md).
