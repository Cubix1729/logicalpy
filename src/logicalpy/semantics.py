from .base import Formula
from itertools import product
from typing import Optional, Iterable


def is_tautology(formula: Formula) -> bool:
    """Tests wether a formula is a tautology

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
    """Tests wether a formula is satisfiable

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
    """Tests wether two formulae are (semantically) equivalent

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
    """Tests wether several formulae are jointly satisfiable

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
    """Tests the (semantic) validity of an argument, defined by the given premises and conclusion

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
