from logicalpy import Formula
from logicalpy.hilbert import *
import unittest


class TestHilbert(unittest.TestCase):
    def test_axiom_matching(self):
        test_axiom_schema = Formula.from_string("~(P & (Q -> P))")
        test_formulae = [
            ("~(P & ((A v A) -> P))", True),
            ("~(A & (B -> C))", False),
            ("~(B & (A -> B))", True),
            ("P v Q", False),
        ]

        for formula_str, expected in test_formulae:
            self.assertIs(matches_axiom(Formula.from_string(formula_str), test_axiom_schema), expected)

    def test_modus_ponens(self):
        test_formulae = [
            ("P", "P -> Q", "Q"),
            ("A", "A -> B", "B"),
            ("(A v A) -> A", "A v A", "A"),
            ("P -> Q", "(P -> Q) -> P", "P"),
            ("(P & Q) -> F", "P v Q", None),
            ("S", "(S v D) -> F", None),
        ]

        for formula_str_a, formula_str_b, expected in test_formulae:
            formula_a = Formula.from_string(formula_str_a)
            formula_b = Formula.from_string(formula_str_b)
            if expected is None:
                with self.assertRaises(ValueError):
                    apply_modus_ponens(formula_a, formula_b)

            else:
                expected_result = Formula.from_string(expected)
                self.assertEqual(apply_modus_ponens(formula_a, formula_b), expected_result)

    def test_hilbert_proof(self):
        # Proof
        test_proof = HilbertProof(premises=[], conclusion=Formula.from_string("P -> P"))
        test_proof.add_axiom_instance(Formula.from_string("P -> ((Q -> P) -> P)"), "A1")
        test_proof.add_axiom_instance(
            Formula.from_string("(P -> ((Q -> P) -> P)) -> ((P -> (Q -> P)) -> (P -> P))"), "A2"
        )
        test_proof.apply_modus_ponens(1, 2)
        test_proof.add_axiom_instance(Formula.from_string("P -> (Q -> P)"), "A1")
        test_proof.apply_modus_ponens(4, 3)

        # Actual tests
        self.assertIs(test_proof.goal_accomplished(), True)
        self.assertEqual(
            str(test_proof),
            """1. P → ((Q → P) → P)                              A1
2. (P → ((Q → P) → P)) → ((P → (Q → P)) → (P → P))A2
3. (P → (Q → P)) → (P → P)                        MP 1, 2
4. P → (Q → P)                                    A1
5. P → P                                          MP 4, 3""",
        )
        self.assertEqual(
            test_proof.to_latex(),
            r"""\begin{enumerate}
\item $P \to ((Q \to P) \to P)$ by A1
\item $(P \to ((Q \to P) \to P)) \to ((P \to (Q \to P)) \to (P \to P))$ by A2
\item $(P \to (Q \to P)) \to (P \to P)$ by MP 1, 2
\item $P \to (Q \to P)$ by A1
\item $P \to P$ by MP 4, 3
\end{enumerate}""",
        )


if __name__ == "__main__":
    unittest.main()
