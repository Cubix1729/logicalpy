# Hilbert-Style Proof System

The interactive prover for Hilbert systems is implemented in the [`hilbert`](../api-reference/logicalpy/hilbert.md) sub-module.

## Usage

The class for Hilbert proofs is `HilbertProof`.
Its constructor takes as its arguments the premises and the conclusion of the argument to prove, as well as the axiom system to use.
The default axiom system used is Jan Łukasiewicz's third axiom system,
called later P$_2$ by Alonzo Church, who popularised it.

The axiom schemata are the following (indicated with Greek letters to differentiate them from simple formulae):

 - A1: $\phi \to (\psi \to \phi)$

 - A2: $(\phi \to (\psi \to \chi)) \to ((\phi \to \psi) \to (\phi \to \chi))$

 - A3: $(\neg \phi \to \neg \psi) \to (\psi \to \phi)$

The inference rule used is Modus Ponens:

$$
\frac{A, A \to B}{B}
$$

To add a line with one of the premises in the proof, use the `add_premise_line(premise)` method.
If you want to add an instance of one of the axiom schemata, you can use the `add_axiom_instance(formula, axiom_name)` method.
Finally, to apply Modus Ponens to two of the previous proof lines, use the `apply_modus_ponens(line_num_a, line_num_b)` method.

Example interactive proof of $A \to A$:

```python
>>> from logicalpy import Formula, Proposition
>>> from logicalpy.hilbert import HilbertProof
>>> A, B = Proposition("A"), Proposition("B")
>>> p = HilbertProof(premises=[], conclusion=Formula(A >> A))
>>> p.add_axiom_instance(Formula(A >> ((B >> A) >> A)), "A1")
>>> print(p)
1. A → ((B → A) → A)                                        A1
>>> p.add_axiom_instance(Formula((A >> ((B >> A) >> A)) >> ((A >> (B >> A)) >> (A >> A))), "A2")
>>> print(p)
1. A → ((B → A) → A)                                        A1
2. (A → ((B → A) → A)) → ((A → (B → A)) → (A → A))          A2
>>> p.apply_modus_ponens(1, 2)
>>> print(p)
1. A → ((B → A) → A)                                        A1
2. (A → ((B → A) → A)) → ((A → (B → A)) → (A → A))          A2
3. (A → (B → A)) → (A → A)                                  MP 1, 2
>>> p.add_axiom_instance(Formula(A >> (B >> A)), "A1")
>>> print(p)
1. A → ((B → A) → A)                                        A1
2. (A → ((B → A) → A)) → ((A → (B → A)) → (A → A))          A2
3. (A → (B → A)) → (A → A)                                  MP 1, 2
4. A → (B → A)                                              A1
>>> p.apply_modus_ponens(4, 3)
>>> print(p)
1. A → ((B → A) → A)                                        A1
2. (A → ((B → A) → A)) → ((A → (B → A)) → (A → A))          A2
3. (A → (B → A)) → (A → A)                                  MP 1, 2
4. A → (B → A)                                              A1
5. A → A                                                    MP 4, 3
>>> print(p.to_latex())
\begin{enumerate}
\item $A \to ((B \to A) \to A)$ by A1
\item $(A \to ((B \to A) \to A)) \to ((A \to (B \to A)) \to (A \to A))$ by A2
\item $(A \to (B \to A)) \to (A \to A)$ by MP 1, 2
\item $A \to (B \to A)$ by A1
\item $A \to A$ by MP 4, 3
\end{enumerate}
```

Like for truth tables, the LaTeX generated is not supported by MathJax, as it uses the `enumerate` environnement.
With a LaTeX compiler, it would render like this:

![LaTeX Rendering](./hilbert_style_proof_example.svg){: style="height:180px;width:578px"}

## Creating a new axiom system

In order to use an axiom system that is not the default one, you will need to create it.
An axiom system consists in LogicalPy of a `dict` mapping each axiom schema name (`str`) to its `Formula`.

!!! note
    Formulae given to create an axiom system will be treated as axiom schemata.

As an example, we will define Frege's axiom system.
Here are the axiom schemata:

 - $\phi \to (\psi \to \phi)$
 - $(\phi \to (\psi \to \chi)) \to ((\phi \to \psi) \to (\psi \to \chi))$
 - $(\phi \to (\psi \to \chi)) \to (\psi \to (\phi \to \chi))$
 - $(\phi \to \psi) \to (\neg \psi \to \neg \phi)$
 - $\neg \neg \phi \to \phi$
 - $\phi \to \neg \neg \phi$

In the Python implementation, we will name them A1, A2, A3 and so on up to A6.

```python
>>> from logicalpy import Formula
>>> frege_axiom_system = {
...    "A1": Formula.from_string("A -> (B -> A)"),
...    "A2": Formula.from_string("(A -> (B -> C)) -> ((A -> B) -> (A -> C))"),
...    "A3": Formula.from_string("(A -> (B -> C)) -> (B -> (A -> C))"),
...    "A4": Formula.from_string("(A -> B) -> (~B -> ~A)"),
...    "A5": Formula.from_string("~~A -> A"),
...    "A6": Formula.from_string("A -> ~~A"),
...}
>>> from logicalpy.hilbert import HilbertProof
>>> # Then you can use the system to make a proof
>>> # if you precise axiom_system=frege_axiom_system
>>> # when constructing the HilbertProof
```

<br>

For a complete reference of the `hilbert` sub-module, see the [corresponding API reference](../api-reference/logicalpy/hilbert.md).
