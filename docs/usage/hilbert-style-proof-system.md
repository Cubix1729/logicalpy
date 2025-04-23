# Hilbert-Style Proof System

The interactive prover for Hilbert systems is implemented in the [`hilbert`](../api-reference/logicalpy/hilbert.md) sub-module.

## Usage

The class for Hilbert proofs is `HilbertProof`.
Its constructor takes as its arguments the premises and the conclusion of the argument to prove, as well as the axiom system to use.
The default axiom system used is Jan Łukasiewicz's third axiom system,
called later P$_2$ by Alonzo Church, who popularised it.

The axiom schemata are the following:

 - A1: $\phi \to (\psi \to \phi)$

 - A2: $(\phi \to (\psi \to \chi)) \to ((\phi \to \psi) \to (\phi \to \chi))$

 - A3: $(\neg \phi \to \neg \psi) \to (\psi \to \phi)$

The inference rule used is Modus Ponens:

$$
A, A \to B \therefore B
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
1. A → ((B → A) → A)                                        A1
2. (A → ((B → A) → A)) → ((A → (B → A)) → (A → A))          A2
>>> print(p)
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

Like for truth tables, the LaTex generated is not supported by MathJax, as it uses the `enumerate` environnement.
With a LaTex compiler, it would render like this:

![LaTex Rendering](./hilbert_style_proof_example.svg){: style="height:180px;width:578px"}

