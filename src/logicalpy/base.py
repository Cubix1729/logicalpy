import lark


class Proposition:
    """A class representing propositions

    Attributes:
        name (str): the name of the proposition
    """

    def __init__(self, name: str):
        if name == "":
            raise ValueError("a proposition name cannot be ''")
        self.name = name

    def __str__(self) -> str:
        return self.name

    def __eq__(self, other):
        if isinstance(other, Proposition):
            return self.name == other.name
        return False

    def as_latex(self) -> str:
        return self.name

    def propositions(self) -> set:
        return {self.name}

    def is_satisfied(self, valuation: dict[str, bool]) -> bool:
        try:
            return valuation[self.name]
        except KeyError:
            raise ValueError(f"proposition '{self.name}' is not associated with a value")

    def __and__(self, other):
        return And(self, other)

    def __or__(self, other):
        return Or(self, other)

    def __rshift__(self, other):
        return Implies(self, other)

    def __invert__(self):
        return Not(self)

    def _eliminate_conditionals(self):
        return self

    def _move_negations_inward(self):
        return self

    def _distribute_or_over_and(self):
        return self

    def _distribute_and_over_or(self):
        return self


class Not:
    """A class representing logical negation

    Attributes:
        a: the negated content

    """

    def __init__(self, a):
        self.a = a

    def __str__(self) -> str:
        return f"¬{self.a}"

    def __eq__(self, other) -> bool:
        if isinstance(other, Not):
            return self.a == other.a
        return False

    def as_latex(self) -> str:
        return r"\neg " + self.a.as_latex()

    def propositions(self) -> set[str]:
        return self.a.propositions()

    def is_satisfied(self, valuation: dict[str, bool]) -> bool:
        return not self.a.is_satisfied(valuation)

    def __and__(self, other):
        return And(self, other)

    def __or__(self, other):
        return Or(self, other)

    def __rshift__(self, other):
        return Implies(self, other)

    def __invert__(self):
        return Not(self)

    def _eliminate_conditionals(self):
        return Not(self.a._eliminate_conditionals())

    def _move_negations_inward(self):
        if isinstance(self.a, Not):  # double negation elimination
            return self.a.a._move_negations_inward()
        elif isinstance(self.a, And):  # De Morgan's law #1 (~(A & B) <-> ~A v ~B)
            return Or(Not(self.a.a)._move_negations_inward(), Not(self.a.b)._move_negations_inward())
        elif isinstance(self.a, Or):  # De Morgan's law #2 (~(A v B) <-> ~A & ~B)
            return And(Not(self.a.a)._move_negations_inward(), Not(self.a.b)._move_negations_inward())
        else:  # matches no rule
            return self

    def _distribute_or_over_and(self):
        return Not(self.a._distribute_or_over_and())

    def _distribute_and_over_or(self):
        return Not(self.a._distribute_and_over_or())


class _TwoPlaceConnective:
    """A general class for all two places logical connectives (not meant for actual use)"""

    CONNECTIVE_SYMBOL = None  # not defined in the base class
    LATEX_SYMBOL = None  # same

    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __str__(self) -> str:
        return f"({self.a} {self.CONNECTIVE_SYMBOL} {self.b})"

    def __eq__(self, other) -> bool:
        if isinstance(other, type(self)):
            return self.a == other.a and self.b == other.b
        return False

    def as_latex(self) -> str:
        return f"({self.a.as_latex()} {self.LATEX_SYMBOL} {self.b.as_latex()})"

    def propositions(self) -> set[str]:
        return self.a.propositions().union(self.b.propositions())

    def __and__(self, other):
        return And(self, other)

    def __or__(self, other):
        return Or(self, other)

    def __rshift__(self, other):
        return Implies(self, other)

    def __invert__(self):
        return Not(self)

    def _eliminate_conditionals(self):
        return type(self)(self.a._eliminate_conditionals(), self.b._eliminate_conditionals())

    def _move_negations_inward(self):
        return type(self)(self.a._move_negations_inward(), self.b._move_negations_inward())

    def _distribute_or_over_and(self):
        return type(self)(self.a._distribute_or_over_and(), self.b._distribute_or_over_and())

    def _distribute_and_over_or(self):
        return type(self)(self.a._distribute_and_over_or(), self.b._distribute_and_over_or())


class And(_TwoPlaceConnective):
    """A class representing logical conjunction

    Attributes:
        a: the left hand part of the conjunction
        b: the right hand part of the conjunction
    """

    CONNECTIVE_SYMBOL = "∧"
    LATEX_SYMBOL = r"\land"

    def is_satisfied(self, valuation: dict[str, bool]) -> bool:
        return self.a.is_satisfied(valuation) and self.b.is_satisfied(valuation)

    def _distribute_and_over_or(self):
        if isinstance(self.b, Or):
            return Or(And(self.a, self.b.a)._distribute_and_over_or(), And(self.a, self.b.b)._distribute_and_over_or())
        elif isinstance(self.a, Or):
            return Or(And(self.b, self.a.a)._distribute_and_over_or(), And(self.b, self.a.b)._distribute_and_over_or())
        else:
            return And(self.a._distribute_and_over_or(), self.b._distribute_and_over_or())


class Or(_TwoPlaceConnective):
    """A class representing logical disjunction

    Attributes:
        a: the left hand part of the disjunction
        b: the right hand part of the disjunction
    """

    CONNECTIVE_SYMBOL = "∨"
    LATEX_SYMBOL = r"\lor"

    def is_satisfied(self, valuation: dict[str, bool]) -> bool:
        return self.a.is_satisfied(valuation) or self.b.is_satisfied(valuation)

    def _distribute_or_over_and(self):
        if isinstance(self.b, And):
            return And(Or(self.a, self.b.a)._distribute_or_over_and(), Or(self.a, self.b.b)._distribute_or_over_and())
        elif isinstance(self.a, And):
            return And(Or(self.b, self.a.a)._distribute_or_over_and(), Or(self.b, self.a.b)._distribute_or_over_and())
        else:
            return Or(self.a._distribute_or_over_and(), self.b._distribute_or_over_and())


class Implies(_TwoPlaceConnective):
    """A class representing logical implication

    Attributes:
        a: the left hand part of the implication
        b: the right hand part of the implication
    """

    CONNECTIVE_SYMBOL = "→"
    LATEX_SYMBOL = r"\to"

    def is_satisfied(self, valuation: dict[str, bool]) -> bool:
        return (not self.a.is_satisfied(valuation)) or self.b.is_satisfied(valuation)

    def _eliminate_conditionals(self):
        return Or(Not(self.a._eliminate_conditionals()), self.b._eliminate_conditionals())


class BiImplies(_TwoPlaceConnective):
    """A class representing logical bi-implication (also called biconditional)

    Attributes:
        a: the left hand part of the biconditional
        b: the right hand part of the biconditional
    """

    CONNECTIVE_SYMBOL = "↔"
    LATEX_SYMBOL = r"\leftrightarrow"

    def is_satisfied(self, valuation: dict[str, bool]) -> bool:
        return self.a.is_satisfied(valuation) == self.b.is_satisfied(valuation)

    def _eliminate_conditionals(self):
        a = self.a._eliminate_conditionals()
        b = self.b._eliminate_conditionals()
        return And(Or(Not(a), b), Or(Not(b), a))


propositional_grammar = r"""
start: formula
PROP: /[A-Za-z]+[0-9]*/

formula: PROP                                  -> proposition
       | formula ("<->" | "↔" | "⇔") formula  -> biconditional
       | formula ("->" | "⇒" | "→") formula   -> implication
       | formula ("v" | "∨" | "|") formula     -> disjunction
       | formula ("&" | "∧") formula           -> conjunction
       | ("~" | "¬") formula             -> negation
       | "(" formula ")"

%import common.WS
%ignore WS
"""

propositional_parser = lark.Lark(propositional_grammar)


def _interpret_formula_tree(tree: lark.Tree):
    match tree.data:
        case "start":
            return _interpret_formula_tree(tree.children[0])
        case "proposition":
            return Proposition(str(tree.children[0]))
        case "negation":
            return Not(_interpret_formula_tree(tree.children[0]))
        case "disjunction":
            return Or(_interpret_formula_tree(tree.children[0]), _interpret_formula_tree(tree.children[1]))
        case "conjunction":
            return And(_interpret_formula_tree(tree.children[0]), _interpret_formula_tree(tree.children[1]))
        case "implication":
            return Implies(_interpret_formula_tree(tree.children[0]), _interpret_formula_tree(tree.children[1]))
        case "biconditional":
            return BiImplies(_interpret_formula_tree(tree.children[0]), _interpret_formula_tree(tree.children[1]))
        case "formula":
            return _interpret_formula_tree(tree.children[0])


class Formula:
    """The general class for a propositional formula

    Attributes:
        formula: the formula described (can be an instance of any of the base connective classes)

    Examples:
        >>> from logicalpy import Proposition, Or, Not, Formula
        >>> P = Proposition("P")
        >>> test_formula = Formula(Or(P, Not(P)))
        >>> str(test_formula)
        'P ∨ ¬P'
        >>> test_formula.propositions()
        {'P'}
        >>> test_formula.is_satisfied({"P": True})
        True
        >>> print(Formula.from_string("P & (P -> P)")
        P ∧ (P → P)

    """

    def __init__(self, formula):
        """The formula's constructor

        Args:
            formula: the formula represented (can be an instance of any of the base connective classes)

        """
        self.formula = formula

    def __str__(self) -> str:
        formula_str = str(self.formula)
        if formula_str.startswith("(") and formula_str.endswith(")"):  # if there are outer parenthesis, we remove them
            return formula_str[1:-1]
        return formula_str

    def __eq__(self, other) -> bool:
        if isinstance(other, Formula):
            return self.formula == other.formula
        return False

    def __hash__(self) -> int:
        return hash(str(self))

    def as_latex(self) -> str:
        """Renders the formula as LaTex code

        Returns:
            (str): the LaTex representation of the formula, as inline math

        """
        formula_latex = self.formula.as_latex()
        if formula_latex.startswith("(") and formula_latex.endswith(
            ")"
        ):  # if there are outer parenthesis, we remove them
            return "$" + formula_latex[1:-1] + "$"
        return "$" + formula_latex + "$"

    @classmethod
    def from_string(cls, formula_str: str):
        """Builds a formula from a string representation of it

        Args:
            formula_str (str): the string containing the string representation of the formula

        Returns:
            (Formula): the formula built

        """
        return cls(_interpret_formula_tree(propositional_parser.parse(formula_str)))

    def propositions(self) -> set[str]:
        """A method for listing all the propositions of the formula

        Returns:
            (set[str]): the set of all the propositions of the formula, each represented by its name (str)

        """
        return self.formula.propositions()

    def is_satisfied(self, valuation: dict[str, bool]) -> bool:
        """Tests wether the formula is satisfied by the truth valuation given

        Args:
            valuation (dict[str, bool]): a dictionary associating each proposition name (str) with a truth value (bool)

        Returns:
            (bool): True is the formula is satisfied by the truth valuation given, and False otherwise

        Raises:
            ValueError: if the truth value of one of the formula's propositions isn't precised in the valuation given

        """
        return self.formula.is_satisfied(valuation)

    def is_literal(self) -> bool:
        """Tests wether the formula is a literal, i.e. a proposition or its negation"""
        if isinstance(self.formula, Proposition):
            return True
        elif isinstance(self.formula, Not):
            if isinstance(self.formula.a, Proposition):
                return True
        return False

    def is_proposition(self) -> bool:
        """Tests wether the formula is only a proposition"""
        return isinstance(self.formula, Proposition)

    def is_negation(self) -> bool:
        """Tests wether the formula's main connective is a negation"""
        return isinstance(self.formula, Not)

    def is_conjunction(self) -> bool:
        """Tests wether the formula's main connective is a conjunction"""
        return isinstance(self.formula, And)

    def is_disjunction(self) -> bool:
        """Tests wether the formula's main connective is a disjunction"""
        return isinstance(self.formula, Or)

    def is_implication(self) -> bool:
        """Tests wether the formula's main connective is an implication"""
        return isinstance(self.formula, Implies)

    def is_bi_implication(self) -> bool:
        """Tests wether the formula's main connective is a bi-implication"""
        return isinstance(self.formula, BiImplies)

    def _eliminate_conditionals(self):
        return Formula(self.formula._eliminate_conditionals())

    def _move_negations_inward(self):
        return Formula(self.formula._move_negations_inward())

    def _distribute_or_over_and(self):
        return Formula(self.formula._distribute_or_over_and())

    def _distribute_and_over_or(self):
        return Formula(self.formula._distribute_and_over_or())
