from typing import Iterable, Optional
from itertools import combinations
import time
from .normal_forms import to_clausal_cnf, DisjunctiveClause
from .base import Formula, Not


def are_complementary_literals(literal_1: Formula, literal_2: Formula) -> bool:
    """A function to test whether two literals are complementary

    Args:
        literal_1 (Formula): the first literal
        literal_2 (Formula): the second literal

    Returns:
        (bool): True if the two literals are complementary, False otherwise

    Raises:
        ValueError: if any of the two formulae given isn't a literal

    """

    if not literal_1.is_literal():
        raise ValueError(f"formula '{literal_1}' is not a literal")
    if not literal_2.is_literal():
        raise ValueError(f"formula '{literal_2}' is not a literal")

    if literal_2.is_proposition() and literal_1.is_negation() and literal_1.formula.a == literal_2.formula:
        return True
    elif literal_1.is_proposition() and literal_2.is_negation() and literal_2.formula.a == literal_1.formula:
        return True

    return False


def resolve(clause_1: DisjunctiveClause, clause_2: DisjunctiveClause) -> Optional[DisjunctiveClause]:
    """A function for apply the resolution inference rule to two disjunctive clauses

    Args:
        clause_1 (DisjunctiveClause): the first clause to resolve
        clause_2 (DisjunctiveClause): the second clause to resolve

    Returns:
        (Optional[DisjunctiveClause]): the resulting resolved (disjunctive) clause if the two given clauses are resolvable, and None otherwise

    """

    for literal_1 in clause_1:
        for literal_2 in clause_2:
            if are_complementary_literals(literal_1, literal_2):
                resulting_literals = []

                for literal in clause_1:
                    if literal != literal_1 and literal != literal_2:
                        resulting_literals.append(literal)
                for literal in clause_2:
                    if literal != literal_1 and literal != literal_2:
                        resulting_literals.append(literal)

                return DisjunctiveClause(*resulting_literals)


def _is_tautology(clause: DisjunctiveClause) -> bool:
    for literal_1, literal_2 in combinations(clause, 2):
        if are_complementary_literals(literal_1, literal_2):
            return True
    return False


def _remove_redundancy(clause: DisjunctiveClause) -> DisjunctiveClause:
    all_literals = []
    for literal in clause:
        if literal not in all_literals:
            all_literals.append(literal)

    return DisjunctiveClause(*all_literals)


class ResolutionProver:
    """A class implementing a prover based on the resolution procedure

    Attributes:
        premises (Iterable[Formula]): the premises of the argument to prove
        conclusion (Formula): the conclusion to prove from the premises (whose contrary would have to be refuted)

    """

    def __init__(self, premises: Iterable[Formula], conclusion: Formula):
        """The prover's constructor

        Args:
            premises (Iterable[Formula]): the premises of the argument to prove
            conclusion (Formula): the conclusion of the argument

        """

        self.premises = premises
        self.conclusion = conclusion

        # We convert the premises to a list of clauses

        all_clauses = []
        for premise in premises:
            cnf_form = to_clausal_cnf(premise)

            for clause in cnf_form:
                clause = _remove_redundancy(clause)
                if not (_is_tautology(clause) or clause in all_clauses):  # remove tautologies or redundant clauses
                    all_clauses.append(clause)

        # We store the index in the clauses of the last premise clause (so the next one is the start of the negation of the conclusion)
        self._premises_end_index = len(all_clauses)

        # We negate the conclusion and add it to the clauses

        negated_conclusion = Formula(Not(conclusion.formula))

        negated_conclusion_cnf = to_clausal_cnf(negated_conclusion)

        for clause in negated_conclusion_cnf:
            clause = _remove_redundancy(clause)
            if not (_is_tautology(clause) or clause in all_clauses):
                all_clauses.append(clause)

        self._all_clauses = all_clauses
        self._refutation_found = False
        self._terminated_without_refutation = False

    def _apply_resolution(self) -> Optional[tuple[DisjunctiveClause, int, int]]:
        """Resolves two clauses if possible and changes `all_clauses` in consideration. The clauses that were resolved are removed, and the resolvent is added.

        Returns:
            (Optional[tuple[DisjunctiveClause, int, int]]): the resulting resolved clause as well as the indexes of two
            clauses from which it was derived if possible, and None otherwise

        """

        # We first look for a contradiction
        for clause_1, clause_2 in combinations(self._all_clauses, 2):
            if len(clause_1.literals) == len(clause_2.literals) == 1:  # the two clauses only have one literal each
                resolvent = resolve(clause_1, clause_2)

                if resolvent is not None:  # we have found a contradiction
                    self._all_clauses.append(resolvent)
                    self._refutation_found = True

                    return resolvent, self._all_clauses.index(clause_1), self._all_clauses.index(clause_2)

        # We then look for two clauses to be resolved
        for clause_1, clause_2 in combinations(self._all_clauses, 2):
            resolvent = resolve(clause_1, clause_2)

            if resolvent is not None:
                resolvent = _remove_redundancy(resolvent)

                if resolvent in self._all_clauses or _is_tautology(resolvent):
                    continue

                self._all_clauses.append(resolvent)

                if resolvent.is_empty():
                    self._refutation_found = True

                return resolvent, self._all_clauses.index(clause_1), self._all_clauses.index(clause_2)

        self._terminated_without_refutation = True
        return None

    def prove(self) -> tuple[bool, str]:
        """Solves the goal given to the constructor by refutation, with the resolution procedure

        Returns:
            (bool): whether a refutation was found from the negated conclusion and the premises, i.e. whether the conclusion is valid given the premises
            (str): the full refutation proof as text

        """

        proof_finished = False
        proof_str = "Resolution proof for argument {0} ∴ {1}\n\n".format(
            ", ".join([str(premise) for premise in self.premises]), str(self.conclusion)
        )
        line_num = 1

        for clause in self._all_clauses[: self._premises_end_index]:
            proof_str += f"{line_num}. {clause}".ljust(30) + "Premise clause\n"
            line_num += 1

        for clause in self._all_clauses[self._premises_end_index :]:
            proof_str += f"{line_num}. {clause}".ljust(30) + "Negated conclusion clause\n"
            line_num += 1

        while not (self._terminated_without_refutation or self._refutation_found):
            result = self._apply_resolution()
            if result is not None:
                resolvent, index_1, index_2 = result
                proof_str += f"{line_num}. {resolvent}".ljust(30) + f"Resolve {index_1 + 1}, {index_2 + 1}\n"
            line_num += 1

        if self._terminated_without_refutation:
            proof_str += "\nNo refutation found: conclusion invalid"
            return False, proof_str

        else:  # refutation found
            proof_str += "\nRefutation found: conclusion valid"
            return True, proof_str
