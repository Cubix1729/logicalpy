from .core import Formula, Or, And


class DisjunctiveClause:
    """A class for representing a disjunctive clause

    Attributes:
        literals (tuple): the literals of the clause

    """

    def __init__(self, *literals: Formula):
        """The clause's constructor

        Args:
            *literals (Formula): the literals of the disjunctive clause, each as a Formula

        Raises:
            ValueError: if any of the arguments given is not a literal (i.e. a proposition or its negation)

        """
        for literal in literals:
            if not literal.is_literal():
                raise ValueError(f"Formula '{literal}' is not a literal")
        self.literals = literals

    def is_empty(self) -> bool:
        """Tests whether the clause is empty"""
        return len(self.literals) == 0

    def __str__(self):
        if len(self.literals) >= 2:
            return "({})".format(" ∨ ".join(str(literal) for literal in self.literals))
        elif len(self.literals) == 1:
            return str(self.literals[0])
        else:
            return "◻"

    def __repr__(self) -> str:
        return "DisjunctiveClause({})".format(
            ", ".join([repr(literal) for literal in self.literals])
        )

    def __eq__(self, other):
        if isinstance(other, DisjunctiveClause):
            return set(self.literals) == set(other.literals)
        return False

    def __iter__(self):
        return iter(self.literals)


class ConjunctiveClause:
    """A class for representing a conjunctive clause

    Attributes:
        literals (tuple): the literals of the clause

    Note:
        Conjunctive clauses are less used than disjunctive clauses. This class is only used in DNF clausal results.

    """

    def __init__(self, *literals: Formula):
        """The clause's constructor

        Args:
            *literals (Formula): the literals of the disjunctive clause, each as a Formula

        Raises:
            ValueError: if any of the arguments given is not a literal (i.e. a proposition or its negation)

        """
        for literal in literals:
            if not literal.is_literal():
                raise ValueError(f"Formula '{literal}' is not a literal")
        self.literals = literals

    def is_empty(self) -> bool:
        """Tests whether the clause is empty"""
        return len(self.literals) == 0

    def __str__(self):
        if len(self.literals) >= 2:
            return "({})".format(" ∧ ".join(str(literal) for literal in self.literals))
        elif len(self.literals) == 1:
            return str(self.literals[0])
        else:
            return "◻"

    def __repr__(self) -> str:
        return "ConjunctiveClause({})".format(
            ", ".join([repr(literal) for literal in self.literals])
        )

    def __eq__(self, other):
        if isinstance(other, ConjunctiveClause):
            return set(self.literals) == set(other.literals)
        return False

    def __iter__(self):
        return iter(self.literals)


def to_nnf(formula: Formula) -> Formula:
    """Converts a formula to negation normal form (NNF), with no implications or bi-implications and
    all negations directly applied to propositions

    Args:
        formula (Formula): the formula to convert

    Returns:
        (Formula): the resulting formula in NNF

    """

    formula = formula._eliminate_conditionals()
    formula = formula._move_negations_inward()

    return formula


def to_cnf(formula: Formula) -> Formula:
    """Converts a formula to conjunctive normal form (CNF)

    Args:
        formula (Formula): the formula to convert

    Returns:
        (Formula): the resulting formula in CNF

    Note:
        This function does not always return the canonical CNF form of the formula. It instead uses syntactic rewriting
        rules to convert a formula to CNF

    """

    formula = to_nnf(formula)

    old_formula = formula
    formula = formula._distribute_or_over_and()

    while old_formula != formula:
        old_formula = formula
        formula = formula._distribute_or_over_and()

    return formula


def to_dnf(formula: Formula) -> Formula:
    """Converts a formula to disjunctive normal form (DNF)

    Args:
        formula (Formula): the formula to convert

    Returns:
        (Formula): the resulting formula in DNF

    Note:
        This function does not always return the canonical DNF form of the formula. It instead uses syntactic rewriting
        rules to convert a formula to DNF

    """

    formula = to_nnf(formula)

    old_formula = formula
    formula = formula._distribute_and_over_or()

    while old_formula != formula:
        old_formula = formula
        formula = formula._distribute_and_over_or()

    return formula


def _find_disjuncts(formula) -> list:
    if isinstance(formula, Or):
        return _find_disjuncts(formula.a) + _find_disjuncts(formula.b)
    else:
        return [Formula(formula)]


def _find_conjuncts(formula) -> list:
    if isinstance(formula, And):
        return _find_conjuncts(formula.a) + _find_conjuncts(formula.b)
    else:
        return [Formula(formula)]


def to_clausal_cnf(formula: Formula) -> list[DisjunctiveClause]:
    """Converts a formula to conjunctive normal form (CNF) like `to_cnf`, but as a list of disjunctive clauses

    Args:
        formula (Formula): the formula to convert

    Returns:
        (list[DisjunctiveClause]): the resulting CNF form, as a list of disjunctive clauses representing their conjunction

    """

    formula = to_cnf(
        formula
    )._formula  # we are manipulating connectives objects, not Formula objects
    conjuncts_list = _find_conjuncts(formula)

    list_of_clauses = []

    for conjunct in conjuncts_list:
        list_of_clauses.append(DisjunctiveClause(*_find_disjuncts(conjunct._formula)))

    return list_of_clauses


def to_clausal_dnf(formula: Formula) -> list[ConjunctiveClause]:
    """Converts a formula to disjunctive normal form (DNF) like `to_dnf`, but as a list of conjunctive clauses

    Args:
        formula (Formula): the formula to convert

    Returns:
        (list[ConjunctiveClause]): the resulting DNF form, as a list of conjunctive clauses representing their disjunction

    """

    formula = to_dnf(
        formula
    )._formula  # we are manipulating connectives objects, not Formula objects
    disjuncts_list = _find_disjuncts(formula)

    list_of_clauses = []

    for disjunct in disjuncts_list:
        list_of_clauses.append(ConjunctiveClause(*_find_conjuncts(disjunct._formula)))

    return list_of_clauses
