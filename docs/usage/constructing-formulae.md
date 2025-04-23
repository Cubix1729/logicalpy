# Constructing Formulae with LogicalPy

With LogicalPy, propositional formulae (class [`Formula`](../api-reference/logicalpy/base.md#logicalpy.base.Formula)) can be constructed in three different ways:

## Using the formula parser

You can use the propositional parser built with `lark`, with the class method `Formula.from_string()`.
Propositions consist of one or several letters, optionally followed by one several digits.
The connectives are as follow:

|  Name  |  Symbols  |
|--------|-----------|
| Negation | `~` or `¬`|
|Conjunction|`&` or `∧`|
|Disjunction|`v`, `|` or `∨`|
|Implication|`->`, `→` or `⇒`|
|Bi-implication|`<->`, `↔` or `⇔`|

Example:

```python
from logicalpy import Formula

fml = Formula.from_string("(~P & (P -> Q)) <-> P")

print(fml)
```

Output:

```
(¬P ∧ (P → Q)) ↔ P
```

## Using the overloaded operators

You can also use the overloaded logical operators: `&` for and, `|` for or, `>>` for implies, and `~` for not, to form
a formula from propositions (class `Proposition`).
Example:

```python
from logicalpy import Formula, Proposition

P = Proposition("P")
Q = Proposition("Q")

fml = (~P & (P >> Q)) | P

print(fml)
```

Output:

```
(¬P ∧ (P → Q)) ∨ P
```

## Directly using the base classes

Finally, you can directly use the base classes `Proposition`, `Not`, `And`, `Or`, `Implies` and `BiImplies`.
Example:

```python
from logicalpy import Formula, Proposition, And, Or, Not, Implies, BiImplies

P = Proposition("P")
Q = Proposition("Q")

fml = Formula(Or(And(Not(P), Implies(P, Q)), P))

print(fml)
```

Output:

```
(¬P ∧ (P → Q)) ∨ P
```
