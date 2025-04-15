from logicalpy.resolution import *
from logicalpy.normal_forms import *
from logicalpy import Formula
import unittest


class TestResolution(unittest.TestCase):
    def test_complementary_literals(self):
        literals_to_test = (
            ("~A", "A", True),
            ("B", "~B", True),
            ("C", "B", False),
            ("~E", "~E", False),
        )

        for (
            literal_1_str,
            literal_2_str,
            expected,
        ) in literals_to_test:
            self.assertIs(
                are_complementary_literals(
                    Formula.from_string(literal_1_str),
                    Formula.from_string(literal_2_str),
                ),
                expected,
            )

    def test_resolve(self):
        clauses_to_test = (
            (
                DisjunctiveClause(
                    Formula.from_string("P"),
                    Formula.from_string("~Q"),
                ),
                DisjunctiveClause(
                    Formula.from_string("Q"),
                    Formula.from_string("R"),
                ),
                DisjunctiveClause(
                    Formula.from_string("P"),
                    Formula.from_string("R"),
                ),
            ),
            (
                DisjunctiveClause(Formula.from_string("P")),
                DisjunctiveClause(Formula.from_string("R")),
                None,
            ),
        )

        for (
            clause_1,
            clause_2,
            expected,
        ) in clauses_to_test:
            self.assertEqual(
                resolve(clause_1, clause_2),
                expected,
            )

    def test_resolution_prover(self):
        arguments_to_test = (
            (["P", "P -> Q"], "R", False),
            (
                ["A v C", "A -> B", "C -> B"],
                "B",
                True,
            ),
            (["~J -> (J & ~J)"], "J", True),
        )

        for (
            premises_str,
            conclusion_str,
            expected,
        ) in arguments_to_test:
            self.assertIs(
                ResolutionProver(
                    premises=[
                        Formula.from_string(premise_str) for premise_str in premises_str
                    ],
                    conclusion=Formula.from_string(conclusion_str),
                ).prove()[0],
                expected,
            )


if __name__ == "__main__":
    unittest.main()
