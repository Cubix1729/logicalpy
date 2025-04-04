from logicalpy import Proposition, Not, And, Or, Implies, BiImplies, Formula
import unittest


class TestFormula(unittest.TestCase):
    test_formula = Formula(Implies(And(Or(Proposition("P"), Proposition("Q")), Proposition("P")), Proposition("P")))

    def test_equal(self):
        P = Proposition("P")
        Q = Proposition("Q")
        self.assertEqual(
            Formula(Implies(And(Or(Proposition("P"), Proposition("Q")), Not(Proposition("Q"))), Proposition("P"))),
            Formula(Implies(And(Or(Proposition("P"), Proposition("Q")), Not(Proposition("Q"))), Proposition("P"))),
        )

    def test_overloaded_operators(self):
        P = Proposition("P")
        Q = Proposition("Q")
        self.assertEqual(Formula(Implies(And(Or(P, Q), Not(Q)), P)), Formula(((P | Q) & (~Q)) >> P))

    def test_str(self):
        P = Proposition("P")
        Q = Proposition("Q")
        self.assertEqual(str(Formula(Implies(And(Or(P, Q), Not(Q)), P))), "((P ∨ Q) ∧ ¬Q) → P")

    def test_repr(self):
        P = Proposition("P")
        self.assertEqual(
            repr(Formula(Or(And(P, P), P))), "Formula(Or(And(Proposition('P'), Proposition('P')), Proposition('P')))"
        )

    def test_propositions(self):
        P = Proposition("P")
        Q = Proposition("Q")
        self.assertEqual(Formula(Implies(P, Implies(Q, BiImplies(P, Q)))).propositions(), {"P", "Q"})

    def test_valuation_1(self):  # with a tautology
        P = Proposition("P")
        Q = Proposition("Q")
        for val_P, val_Q in ((False, False), (True, False), (False, True), (True, True)):
            self.assertEqual(
                Formula(Implies(P, And(P, Or(P, Q)))).is_satisfied(valuation={"P": val_P, "Q": val_Q}), True
            )

    def test_valuation_2(self):  # with a contradiction
        P = Proposition("P")
        Q = Proposition("Q")
        for val_P, val_Q in ((False, False), (True, False), (False, True), (True, True)):
            self.assertEqual(
                Formula(And(Implies(Q, Q), And(P, Not(P)))).is_satisfied(valuation={"P": val_P, "Q": val_Q}), False
            )

    def test_parser(self):
        P = Proposition("P")
        Q = Proposition("Q")
        formulae_to_parse = {
            "P v Q": Formula(Or(P, Q)),
            "P | ~P": Formula(Or(P, Not(P))),
            "(Q & P) -> (Q <-> P)": Formula(Implies(And(Q, P), BiImplies(Q, P))),
            "(Q ∧ P) → (Q ↔ P)": Formula(Implies(And(Q, P), BiImplies(Q, P))),
            "(P ⇒ Q) ⇒ (P ⇔ Q)": Formula(Implies(Implies(P, Q), BiImplies(P, Q))),
            "~~~P": Formula(Not(Not(Not(P)))),
            "¬Q v P": Formula(Or(Not(Q), P)),
        }
        for test_str, expected_formula in formulae_to_parse.items():
            self.assertEqual(Formula.from_string(test_str), expected_formula)

    def test_latex(self):
        formulae_to_test = (
            ("(P v Q) & ~P", r"$(P \lor Q) \land \neg P$"),
            ("P -> (Q <-> P)", r"$P \to (Q \leftrightarrow P)$"),
        )
        for formula_str, expected in formulae_to_test:
            self.assertEqual(Formula.from_string(formula_str).to_latex(), expected)

    def test_main_connectives(self):
        self.assertEqual(Formula.from_string("P").is_proposition(), True)
        self.assertEqual(Formula.from_string("~(P & (P -> Q))").is_negation(), True)
        self.assertEqual(Formula.from_string("R v (P -> R)").is_disjunction(), True)
        self.assertEqual(Formula.from_string("P & (P -> Q)").is_conjunction(), True)
        self.assertEqual(Formula.from_string("P -> Q").is_implication(), True)
        self.assertEqual(Formula.from_string("P <-> (P v P)").is_bi_implication(), True)
        self.assertEqual(Formula.from_string("P").is_literal(), True)
        self.assertEqual(Formula.from_string("~Q").is_literal(), True)
        self.assertEqual(Formula.from_string("P <-> (P v P)").is_literal(), False)


if __name__ == "__main__":
    unittest.main()
