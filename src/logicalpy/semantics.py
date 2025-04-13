from typing import Optional, Iterable
from itertools import product
import re
from tabulate import tabulate
from .base import Formula


class TruthTable:
    """A class representing a truth table"""

    def __init__(self, formula: Formula):
        """The truth table's constructor

        Args:
            formula (Formula): the formula to build the truth table for

        """

        self.formula = formula

        # Attributes storing return values for more efficiency
        self._str_table = None
        self._markdown_table = None
        self._latex_table = None

    def to_str(self) -> str:
        """Renders the truth table as a str with the `tabulate` library (style used: 'simple')

        Returns:
            (str): the truth table

        """

        if self._str_table is not None:
            return self._str_table

        table_data = []

        formula_props = sorted(list(self.formula.propositions()))
        table_headers = formula_props + [str(self.formula)]

        truth_valuations_possible = product((True, False), repeat=len(formula_props))

        for valuation in truth_valuations_possible:
            valuation_dict = {prop: value for (prop, value) in zip(formula_props, valuation)}
            if self.formula.is_satisfied(valuation_dict):
                truth_value = "T"
            else:
                truth_value = "F"

            table_data.append(["T" if val is True else "F" for val in valuation] + [truth_value])

        self._str_table = tabulate(table_data, headers=table_headers, tablefmt="simple")
        return self._str_table

    def __str__(self) -> str:
        return self.to_str()

    def __repr__(self) -> str:
        return f"TruthTable({self.formula})"

    def to_markdown(self) -> str:
        """Renders the truth table as Markdown with the `tabulate` library

        Returns:
            (str): the Markdown truth table

        """

        if self._markdown_table is not None:
            return self._markdown_table

        table_data = []

        formula_props = sorted(list(self.formula.propositions()))
        table_headers = formula_props + [str(self.formula)]

        truth_valuations_possible = product((True, False), repeat=len(formula_props))

        for valuation in truth_valuations_possible:
            valuation_dict = {prop: value for (prop, value) in zip(formula_props, valuation)}
            if self.formula.is_satisfied(valuation_dict):
                truth_value = "T"
            else:
                truth_value = "F"

            table_data.append(["T" if val is True else "F" for val in valuation] + [truth_value])

        self._str_table = tabulate(table_data, headers=table_headers, tablefmt="github")
        return self._str_table

    def to_latex(self) -> str:
        """Renders the truth table as LaTex (with the `tabulate` library)

        Returns:
            (str): the LaTex output, which uses the `tabular` LaTex environment

        """
        if self._latex_table is not None:
            return self._latex_table

        table_data = []

        formula_props = sorted(list(self.formula.propositions()))
        table_headers = formula_props + [self.formula.to_latex()]

        truth_valuations_possible = product((True, False), repeat=len(formula_props))

        for valuation in truth_valuations_possible:
            valuation_dict = {prop: value for (prop, value) in zip(formula_props, valuation)}
            if self.formula.is_satisfied(valuation_dict):
                truth_value = "T"
            else:
                truth_value = "F"

            table_data.append(["T" if val is True else "F" for val in valuation] + [truth_value])

        latex_result = tabulate(table_data, headers=table_headers, tablefmt="latex_raw")
        # Add vertical bars between columns and remove very first horizontal bar
        latex_result = re.sub(
            r"begin\{tabular\}\{.+\}\n\\hline",
            r"begin{tabular}{" + "|".join(["c" for _ in range(len(table_headers))]) + "}",
            latex_result,
            count=1,
        )
        # Remove last horizontal bar
        latex_result = latex_result.replace(r"\hline" + "\n" + r"\end{tabular}", r"\end{tabular}")
        self._latex_table = latex_result
        return self._latex_table


def is_tautology(formula: Formula) -> bool:
    """Tests whether a formula is a tautology

    Args:
        formula (Formula): the formula to test

    Returns:
        (bool): True if the formula given is a tautology, and False otherwise

    """

    formula_props = list(formula.propositions())

    truth_valuations_possible = product((False, True), repeat=len(formula_props))

    for valuation in truth_valuations_possible:
        valuation_dict = {prop: value for (prop, value) in zip(formula_props, valuation)}
        if not formula.is_satisfied(valuation_dict):
            return False
    return True


def is_satisfiable(formula: Formula) -> bool:
    """Tests whether a formula is satisfiable

    Args:
        formula (Formula): the formula to test

    Returns:
        (bool): True if the formula given is satisfiable, and False otherwise

    """

    formula_props = list(formula.propositions())

    truth_valuations_possible = product((False, True), repeat=len(formula_props))

    for valuation in truth_valuations_possible:
        valuation_dict = {prop: value for (prop, value) in zip(formula_props, valuation)}
        if formula.is_satisfied(valuation_dict):
            return True
    return False


def are_equivalent(formula_1: Formula, formula_2: Formula) -> bool:
    """Tests whether two formulae are (semantically) equivalent

    Args:
        formula_1: the first formula to test
        formula_2: the second formula to test

    Returns:
        (bool): True if the two formulae given are semantically equivalent, and False otherwise

    """

    formula_props = list(formula_1.propositions().union(formula_2.propositions()))

    truth_valuations_possible = product((False, True), repeat=len(formula_props))

    for valuation in truth_valuations_possible:
        valuation_dict = {prop: value for (prop, value) in zip(formula_props, valuation)}
        if formula_1.is_satisfied(valuation_dict) != formula_2.is_satisfied(valuation_dict):
            return False
    return True


def are_jointly_satisfiable(*formulae: Formula) -> bool:
    """Tests whether several formulae are jointly satisfiable

    Args:
        *formulae (Formula): the formulae to test for satisfiability

    Returns:
        (bool): True, if the formulae are satisfiable, and False otherwise

    Raises:
        ValueError: if one or less formulae are given

    """
    if len(formulae) <= 1:
        raise ValueError("cannot test consistency for 1 formula or less")

    props = []
    for formula in formulae:
        props.extend(formula.propositions())

    truth_valuations_possible = product((False, True), repeat=len(props))

    for valuation in truth_valuations_possible:
        valuation_dict = {prop: value for (prop, value) in zip(props, valuation)}
        if all([formula.is_satisfied(valuation_dict) for formula in formulae]):
            return True
    return False


def one_satisfying_valuation(formula: Formula) -> Optional[dict[str, bool]]:
    """Returns one valuation that satisfies the formula given

    Args:
        formula: the formula to test with valuations

    Returns:
        (Optional[dict[str, bool]]): a valuation that satisfies the formula if it exists, and None otherwise

    """

    formula_props = list(formula.propositions())

    truth_valuations_possible = product((False, True), repeat=len(formula_props))

    for valuation in truth_valuations_possible:
        valuation_dict = {prop: value for (prop, value) in zip(formula_props, valuation)}
        if formula.is_satisfied(valuation_dict):
            return valuation_dict
    return None


def all_satisfying_valuations(formula: Formula) -> list[dict[str, bool]]:
    """Returns all the valuations that satisfy the formula given

    Args:
        formula: the formula to test for valuations

    Returns:
        (list[dict[str, bool]]): the list of all the valuations that satisfy the formula given.
            Each valuation is dictionary mapping each proposition name to a truth value (bool)

    """

    formula_props = list(formula.propositions())

    truth_valuations_possible = product((False, True), repeat=len(formula_props))

    satisfying_valuations = []

    for valuation in truth_valuations_possible:
        valuation_dict = {prop: value for (prop, value) in zip(formula_props, valuation)}
        if formula.is_satisfied(valuation_dict):
            satisfying_valuations.append(valuation_dict)
    return satisfying_valuations


def is_valid_argument(premises: Iterable[Formula], conclusion: Formula) -> bool:
    """Tests whether an argument is (semantically) valid, i.e. whether the premises given entail the conclusion given

    Args:
        premises (Iterable[Formula]): the premises of the argument
        conclusion (Formula): the conclusion of the argument

    Returns:
        (bool): True if the argument is valid, and False otherwise

    """

    all_props_set = set()
    for premise in premises:
        all_props_set = all_props_set.union(premise.propositions())
    all_props_set = all_props_set.union(conclusion.propositions())

    argument_props = list(all_props_set)

    truth_valuations_possible = product((False, True), repeat=len(argument_props))

    for valuation in truth_valuations_possible:
        valuation_dict = {prop: value for (prop, value) in zip(argument_props, valuation)}

        all_premises_true = True

        for premise in premises:
            if not premise.is_satisfied(valuation_dict):  # at least one premise is False under the current valuation
                all_premises_true = False
                break

        if all_premises_true:
            if not conclusion.is_satisfied(valuation_dict):
                return False

    return True
