from dataclasses import dataclass
from typing import Set, IO, List
import string


@dataclass
class AnswerGroup:
    """information about the answers provided by a group of passengers"""

    questions_answered_with_yes: Set[str]


def load_answers_from_file(f: IO) -> List[AnswerGroup]:
    """load answers from the puzzle input"""

    groups = []

    answered_with_yes = set()
    for line in f:
        # if we encounter a blank line and have data, this is the end of a group, so record it
        if not line.strip() and answered_with_yes:
            groups.append(AnswerGroup(
                questions_answered_with_yes=answered_with_yes,
            ))
            answered_with_yes = set()
            continue

        # otherwise, find all unique letters in this line of text
        # and add them to the current set of unique letters
        answered_with_yes.update(set(letter for letter in line if letter in string.ascii_lowercase))

    # if we get to the end and have values in our set, then there's a group that wasn't followed
    # by a final blank line, so record the values from that group
    if answered_with_yes:
        groups.append(AnswerGroup(
            questions_answered_with_yes=answered_with_yes,
        ))

    return groups


def main():
    # load the answers from the input file
    with open('input/day6.txt') as f:
        answer_groups = load_answers_from_file(f)

    for group in answer_groups:
        print(f"- {len(group.questions_answered_with_yes)} questions answered with yes")

    # total the number of yes-answers in each group
    total_answered_with_yes = sum(
        len(group.questions_answered_with_yes)
        for group in answer_groups
    )
    print(f"total questions answered with yes: {total_answered_with_yes}")


if __name__ == '__main__':
    main()
