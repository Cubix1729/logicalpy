# Normal Forms

The sub-module for normal forms is the `normal_forms` sub-module. Its functionalities include:

## CNF and DNF

Formulae can be converted to CNF (Conjunctive Normal Form) or to DNF (Disjunctive Normal Form) with the `to_cnf()` and `to_dnf()` functions,
which return an equivalent `Formula` in normal form.
The normal forms found are not canonical forms. Instead of using truth tables, the functions use the following rewriting rules:

1. All conditionals and biconditionals are removed using the rules:

    $$A \leftrightarrow B \equiv (A \to B) \land (B \to A)$$

    $$A \to B \equiv \neg A \lor B$$

2. Then negations are moved inwards, with De Morgan's laws:

    $$\neg (A \lor B) \equiv \neg A \land \neg B$$

    $$\neg (A \land B) \equiv \neg A \lor \neg B$$

    Double negations are removed:

    $$\neg \neg A \equiv A$$

    And at this point, NNF (Negation Normal Form) is obtained. You can directly use the `to_nnf()` function to convert a formula to NNF.

3. Finally:
    - If the desired form is CNF, we distribute disjunctions over conjunctions:
    
    $$A \lor (B \land C) \equiv (A \lor B) \land (A \lor C)$$

    - If the desired form is DNF, we distribute conjunctions over disjunctions:
    
    $$A \land (B \lor C) \equiv (A \land B) \lor (A \land C)$$


Example usage:

```python
>>> from logicalpy import Formula
>>> from logicalpy.normal_forms import to_cnf, to_dnf
>>> test_formula = Formula.from_string("~P -> ~(Q v P)")
>>> print(to_dnf(test_formula))
P ∨ (¬Q ∧ ¬P)
>>> print(to_cnf(test_formula))
(P ∨ ¬Q) ∧ (P ∨ ¬P)
```

## Clausal representations of normal forms

The `normal_forms` sub-module also contains classes representing conjunctive and disjunctive clauses.
The CNF and DNF forms can be found in terms of clauses with the `to_clausal_cnf()` and `to_clausal_dnf()` functions.
With `to_cnf()` and `to_dnf()`, the resulting normal forms are `Formula` instances, so disjunction and conjunction
are represented as binary operators, but with `to_clausal_cnf()` and `to_clausal_dnf()`, the results are lists
of clauses. Note that the resulting clauses aren't simplified.

<br>

For a complete reference of the `normal_forms` sub-module, see the [corresponding API reference](../api-reference/logicalpy/normal_forms.md).
