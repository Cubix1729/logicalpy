from logicalpy.normal_forms import *
from logicalpy import Formula
import unittest


class TestNormalForms(unittest.TestCase):
    def test_nnf(self):
        formulae_to_test = (
            ("~(P -> Q)", "P & (~Q)"),
            ("~Q & ~(P <->Q)", "~Q & ((P & ~Q) v (Q & ~P))"),
            ("~(P v (~~~P))", "~P & P"),
            ("~(Q v (P -> R))", "~Q & (P & ~R)"),
        )

        for formula_str, expected_result_str in formulae_to_test:
            self.assertEqual(to_nnf(Formula.from_string(formula_str)), Formula.from_string(expected_result_str))

    def test_cnf(self):
        formulae_to_test = (
            ("P <-> Q", "(~P v Q) & (~Q v P)"),
            ("P -> ~(P & P)", "~P v (~P v ~P)"),
            ("(P -> Q) -> R", "(R v P) & (R v ~Q)"),
        )

        for formula_str, expected_result_str in formulae_to_test:
            self.assertEqual(to_cnf(Formula.from_string(formula_str)), Formula.from_string(expected_result_str))

    def test_dnf(self):
        formulae_to_test = (
            ("P <-> Q", "((~Q & ~P) v (~Q & Q)) v ((P & ~P) v (P & Q))"),
            ("P -> ~(P & P)", "~P v (~P v ~P)"),
            ("(P -> Q) -> R", "(P & ~Q) v R"),
            ("(P <-> Q) -> (~P & R)", "((P & ~Q) v (Q & ~P)) v (~P & R)"),
        )

        for formula_str, expected_result_str in formulae_to_test:
            self.assertEqual(to_dnf(Formula.from_string(formula_str)), Formula.from_string(expected_result_str))

    def test_clausal_cnf(self):
        formulae_to_test = (
            ("P <-> Q", "((¬P ∨ Q) ∧ (¬Q ∨ P))"),
            ("(P -> Q) -> R", "((R ∨ P) ∧ (R ∨ ¬Q))"),
        )

        for formula_str, expected_result in formulae_to_test:
            self.assertEqual(
                f"({" ∧ ".join([str(clause) for clause in to_clausal_cnf(Formula.from_string(formula_str))])})",
                expected_result,
            )

    def test_clausal_dnf(self):
        formulae_to_test = (
            ("P <-> Q", "((¬Q ∧ ¬P) ∨ (¬Q ∧ Q) ∨ (P ∧ ¬P) ∨ (P ∧ Q))"),
            ("(P -> Q) -> R", "((P ∧ ¬Q) ∨ R)"),
        )

        for formula_str, expected_result in formulae_to_test:

            self.assertEqual(
                f"({" ∨ ".join([str(clause) for clause in to_clausal_dnf(Formula.from_string(formula_str))])})",
                expected_result,
            )


if __name__ == "__main__":
    unittest.main()
