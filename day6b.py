from dataclasses import dataclass
from typing import Set, IO, List
import string


@dataclass
class IndividualAnswers:
    """information about the answers provided by a single passenger"""

    questions_answered_with_yes: Set[str]


@dataclass
class AnswerGroup:
    """information about the answers provided by a group of passengers"""

    passengers: List[IndividualAnswers]

    @property
    def questions_answered_with_yes(self) -> Set[str]:
        """list all questions that had at least one passenger in this group answer yes"""

        answers = set()
        for p in self.passengers:
            answers.update(p.questions_answered_with_yes)

        return answers

    def questions_everyone_answered_yes_to(self) -> List[str]:
        """list all the questions that all passengers answeres yes to"""

        return [
            # record the question
            q
            # for every question that we know someone in the group answeres yes to
            for q in self.questions_answered_with_yes
            # if that question was answeres yes by every passenger
            if all(
                # is this question answers yes by this passenger
                q in p.questions_answered_with_yes
                # for each passenger in this group
                for p in self.passengers
            )
        ]


def load_answers_from_file(f: IO) -> List[AnswerGroup]:
    """load answers from the puzzle input"""

    groups = []

    individual_answers = []
    for line in f:
        # if we encounter a blank line and have data, this is the end of a group, so record it
        if not line.strip() and individual_answers:
            groups.append(AnswerGroup(
                passengers=individual_answers,
            ))
            individual_answers = []
            continue

        # otherwise, record all the answers to which an individual responded yes
        # and record that individual
        individual_answers.append(IndividualAnswers(
            questions_answered_with_yes=set(letter for letter in line if letter in string.ascii_lowercase)
        ))

    # if we get to the end and have values in our set, then there's a group that wasn't followed
    # by a final blank line, so record the individuals from that group
    if individual_answers:
        groups.append(AnswerGroup(
            passengers=individual_answers,
        ))

    return groups


def main():
    # load the answers from the input file
    with open('input/day6.txt') as f:
        answer_groups = load_answers_from_file(f)

    for group in answer_groups:
        print(f"- '{''.join(group.questions_everyone_answered_yes_to())}' ({len(group.questions_everyone_answered_yes_to())})")

    # total the number of questions in each group that everyone answered yes to
    total_answered_with_yes = sum(
        len(group.questions_everyone_answered_yes_to())
        for group in answer_groups
    )
    print(f"total questions answered with yes: {total_answered_with_yes}")


if __name__ == '__main__':
    main()
