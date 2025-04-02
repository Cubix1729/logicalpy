# Resolution Theorem Proving

The [`resolution`](../api-reference/logicalpy/normal_forms.md) sub-module can be used for propositional
resolution proving.

## Usage

The class `ResolutionProver` is used for automated resolution refutation.
Its constructor takes the premises of the logical argument as an iterable containing `Formula` objects, and
and the conclusion to prove as a `Formula` as well.
The `prove()` method returns (a tuple containing) two objects:

 - Whether a contradiction was derived from the premises and the negated conclusion
 - The full resolution proof as a `str`

See the example below for a proof of $A \lor B, A \to C, B \to C \vdash C$:

```python
from logicalpy import Formula, Proposition, Or, Implies
from logicalpy.resolution import ResolutionProver

premises = [
    Formula.from_string("A v B"),
    Formula.from_string("A -> C"),
    Formula.from_string("B -> C")
]

conclusion = Formula.from_string("C")

test_prover = ResolutionProver(premises=premises, conclusion=conclusion)

refutation_found, proof_str = test_prover.prove()

print("Refutation found:", refutation_found)

print("\nProof:\n" + proof_str)
```

Output:

```
Refutation found: True

Proof:
Resolution proof for argument A ∨ B, A → C, B → C ∴ C

1. (A ∨ B)                    Premise clause
2. (¬A ∨ C)                   Premise clause
3. (¬B ∨ C)                   Premise clause
4. ¬C                         Negated conclusion clause
5. (B ∨ C)                    Resolve 1, 2
6. (A ∨ C)                    Resolve 1, 3
7. ¬A                         Resolve 2, 4
8. B                          Resolve 1, 7
9. C                          Resolve 2, 6
10. ◻                         Resolve 4, 9

Refutation found: conclusion valid
```

<br>

For a complete reference of the `resolution` sub-module, see the [corresponding API reference](../api-reference/logicalpy/resolution.md).