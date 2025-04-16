from .base import Formula
from typing import Iterable
import re


P2_AXIOM_SYSTEM = {
    "A1": Formula.from_string("A -> (B -> A)"),
    "A2": Formula.from_string("(A -> (B -> C)) -> ((A -> B) -> (A -> C))"),
    "A3": Formula.from_string("(~A -> ~B) -> (B -> A)"),
}
r"""The default axiom system for Hilbert proofs.

It is Łukasiewicz's third axiom system, called later P₂ by Alonzo Church, who
popularised it.

The axiom schemata are the following:

 - A1: $\phi \to (\psi \to \phi)$

 - A2: $(\phi \to (\psi \to \chi)) \to ((\phi \to \psi) \to (\phi \to \chi))$

 - A3: $(\neg \phi \to \neg \psi) \to (\psi \to \phi)$

"""


def _make_regex_from_formula(
    formula: Formula,
) -> str:
    formula_props = formula.propositions()
    formula_str = str(formula)
    formula_str = formula_str.replace("(", r"\(").replace(")", r"\)")
    for prop in formula_props:
        # For every proposition in the formula, we first replace its *first* occurrence by a regex definition
        formula_str = formula_str.replace(prop, f"(?P<{prop}>.*)", 1)
        # We then replace the *other* occurrences of the propositions by backreferences
        formula_str = re.sub(
            f"([\\s\\(])({prop})",
            r"\1(?P=\2)",
            formula_str,
        )
    return formula_str


def matches_axiom(formula: Formula, axiom_schema: Formula) -> bool:
    """Tests whether a formula is an instance of an axiom schema

    Args:
        formula (Formula): the formula to test
        axiom_schema (Formula): the axiom schema

    Returns:
        (bool): True if `formula` is an instance of `axiom_schema`, and False otherwise

    """
    formula_str = str(formula)
    axiom_regex = _make_regex_from_formula(axiom_schema)
    return re.fullmatch(axiom_regex, formula_str) is not None


def apply_modus_ponens(formula_a: Formula, formula_b: Formula) -> Formula:
    """Applies Modus Ponens inference rule ($A, A \to B \therefore B$) to two formulae to derive a conclusion

    Args:
        formula_a (Formula): the first formula
        formula_b (Formula): the second formula

    Returns:
        (Formula): the conclusion derived with Modus Ponens from the formulae given (the order of the formulae does not matter)

    Raises:
        ValueError: if Modus Ponens cannot be applied in any order to the formulae

    """
    if formula_a.is_implication():
        if formula_a._formula.a == formula_b._formula:
            return Formula(formula_a._formula.b)

    if formula_b.is_implication():
        if formula_b._formula.a == formula_a._formula:
            return Formula(formula_b._formula.b)

    raise ValueError(
        f"cannot apply Modus Ponens to formulae '{formula_a}' and '{formula_b}'"
    )


class HilbertProof:
    """A class for making proofs with a Hilbert axiomatic system

    Attributes:
        premises (Iterable[Formula]): the premises of the argument to prove
        conclusion (Formula): the conclusion to prove from the premises
        axiom_system (dict[str, Formula]): the axiom system used in the proof

    """

    def __init__(
        self,
        premises: Iterable[Formula],
        conclusion: Formula,
        axiom_system: list[Formula] = P2_AXIOM_SYSTEM,
    ):
        """The constructor of the proof

        Args:
            premises (Iterable[Formula]): the premises of the argument to prove
            conclusion (Formula): the conclusion to prove from the premises
            axiom_system (dict[str, Formula]): the axiom system to work with, as a dictionary
                mapping axiom schemata names (`str`) to the axiom formulae

        """
        self.premises = premises
        self.conclusion = conclusion
        self.axiom_system = axiom_system
        self._lines: list[tuple[Formula, str]] = []

    def add_premise_line(self, premise: Formula):
        """Adds a line in the proof containing the premise given

        Args:
            premise (Formula): the premise to add to the lines

        Raises:
            ValueError: if the premise given isn't in the premises of the argument to prove

        """
        if premise not in self.premises:
            raise ValueError(
                f"premise '{premise}' is not in the premises of the argument to prove"
            )

        self._lines.append((premise, "Premise"))

    def add_axiom_instance(self, formula: Formula, axiom_name: str):
        """Adds a line in the proof with a formula that is an instance of an axiom schema

        Args:
            formula (Formula): the formula to add to the proof lines
            axiom_name (str): the name of the axiom schema that justifies the formula given

        Raises:
            ValueError: if the axiom schema name given does not exist or if the formula given is not
                an instance of the axiom schema

        """
        if not axiom_name in self.axiom_system:
            raise ValueError(f"axiom schema '{axiom_name}' does not exist")
        axiom_formula = self.axiom_system[axiom_name]
        if not matches_axiom(formula, axiom_formula):
            raise ValueError(
                f"formula '{formula}' is not an instance of axiom schema '{axiom_name}'"
            )
        self._lines.append((formula, axiom_name))

    def apply_modus_ponens(self, line_num_a: int, line_num_b: int):
        """Adds in the proof a formula infered by Modus Ponens from two preceding formulae

        Args:
            line_num_a (int): the line number of the first formula
            line_num_b (int): the line number of the second formula

        Raises:
            ValueError: if Modus Ponens cannot be applied in any order to the formulae

        Note:
            Line numbers start at one, and not at zero.

        """
        formula_a = self._lines[line_num_a - 1][0]
        formula_b = self._lines[line_num_b - 1][0]
        resulting_formula = apply_modus_ponens(formula_a, formula_b)
        self._lines.append(
            (
                resulting_formula,
                f"MP {line_num_a}, {line_num_b}",
            )
        )

    def remove_line(self, line_index: int):
        """Removes a line with the line number given from the proof
        (line numbers start at one)"""
        del self._lines[line_index - 1]

    def goal_accomplished(self) -> bool:
        """Checks whether the goal defined when constructing the proof is accomplished or not"""
        return self._lines[-1][0] == self.conclusion

    def __str__(self) -> str:
        result_lines = []
        for line_index, (
            formula,
            justification,
        ) in enumerate(self._lines):
            line_str = f"{line_index + 1}. {formula}".ljust(50)
            line_str += justification
            result_lines.append(line_str)
        return "\n".join(result_lines)

    def to_latex(self) -> str:
        """Renders the proof to LaTex

        Returns:
            (str): the LaTex representation of the proof, which uses the `enumerate` environnement

        """
        result_lines = [r"\begin{enumerate}"]
        for formula, justification in self._lines:
            line_str = rf"\item {formula.to_latex()} by {justification}"
            result_lines.append(line_str)
        result_lines.append(r"\end{enumerate}")
        return "\n".join(result_lines)
