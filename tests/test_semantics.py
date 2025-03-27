from logicalpy.semantics import *
from logicalpy import Formula
import unittest


class TestSemantics(unittest.TestCase):
    def test_tautology(self):
        formulae_to_test = (
            ("P v (~P)", True),
            ("P -> (P -> P)", True),
            ("P & P", False),
            ("P v Q", False),
            ("(P & Q) -> (P v Q)", True),
            ("((P -> Q) -> P) -> P", True),
            ("(P -> Q) <-> (~P v Q)", True),
        )

        for formula_str, expected in formulae_to_test:
            self.assertIs(is_tautology(Formula.from_string(formula_str)), expected)

    def test_satisfiability(self):
        formulae_to_test = (
            ("P v (~P)", True),
            ("P -> (P -> P)", True),
            ("P & P", True),
            ("(P & Q) -> (P v Q)", True),
            ("((P -> Q) -> P) -> P", True),
            ("(P -> Q) <-> (~P v Q)", True),
            ("P & (~P)", False),
            ("P v (R -> Q)", True),
        )

        for formula_str, expected in formulae_to_test:
            self.assertIs(is_satisfiable(Formula.from_string(formula_str)), expected)

    def test_equivalence(self):
        formulae_to_test = (
            ("P -> (~R)", "(~P) v (~R)", True),
            ("P v (Q v R)", "(Q v P) v R", True),
            ("Q & P", "Q v P", False),
            ("P -> Q", "Q -> P", False),
            ("A v (A & B)", "A", True),
            ("P -> Q", "Q -> R", False),
        )

        for formula_str_1, formula_str_2, expected in formulae_to_test:
            self.assertIs(
                are_equivalent(Formula.from_string(formula_str_1), Formula.from_string(formula_str_2)), expected
            )

    def test_consistency(self):
        formulae_to_test = (
            (("P", "P -> R", "R -> Q"), True),
            (("P", "(~P) v Q", "~Q"), False),
            (("P -> R", "~R", "P"), False),
            (("P -> Q", "~P", "~Q"), True),
            (("A", "B"), True),
        )

        for formulae, expected in formulae_to_test:
            self.assertIs(are_consistent([Formula.from_string(formula) for formula in formulae]), expected)

    def test_one_satisfying_valuation(self):
        formulae_to_test = ("P -> Q", "P v ((~B) & (T -> E))", "~P v P", "(~Q) & Q")

        for formula_str in formulae_to_test:
            formula = Formula.from_string(formula_str)
            statisfying_valuation = one_satisfying_valuation(formula)
            if statisfying_valuation is not None:
                self.assertIs(formula.is_satisfied(statisfying_valuation), True)

            else:  # formula should unsatisfiable (i.e. a contradiction)
                self.assertIs(is_satisfiable(formula), False)

    def test_all_satisfying_valuations(self):
        formulae_to_test = ("P -> Q", "P v ((~B) & (T -> E))", "~P v P", "(~Q) & Q")

        for formula_str in formulae_to_test:
            formula = Formula.from_string(formula_str)
            statisfying_valuations = all_satisfying_valuations(formula)

            for valuation in statisfying_valuations:
                self.assertIs(formula.is_satisfied(valuation), True)

    def test_argument_validity(self):
        arguments_to_test = (
            (("P", "P -> Q"), "Q", True),
            (("P -> Q", "~P"), "~Q", False),
            (("A v B", "B -> C", "A -> C"), "C", True),
            (("A v B", "~B"), "A", True),
            (("P v R", "Q v R"), "R", False),
            (("~A -> (A v B)", "~A"), "B", True),
            ((), "(~P) v P", True),
            (("~~P", "Q -> P"), "Q", False),
        )

        for argument_premises, argument_conclusion, expected in arguments_to_test:
            self.assertIs(
                is_valid_argument(
                    [Formula.from_string(premise) for premise in argument_premises],
                    Formula.from_string(argument_conclusion),
                ),
                expected,
            )


if __name__ == "__main__":
    unittest.main()
