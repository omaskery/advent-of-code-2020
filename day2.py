from typing import List, Optional, Tuple
from dataclasses import dataclass
import re


@dataclass
class PasswordPolicy:
    min_occurrences: int
    max_occurrences: int
    letter: str


@dataclass
class PasswordEntry:
    policy: PasswordPolicy
    password: str


PASSWORD_ENTRY_REGEX = re.compile(r'^\s*(?P<min>\d+)-(?P<max>\d+)\s+(?P<letter>[a-zA-Z])\s*:\s*(?P<password>.+)\s*$')


def build_password_entry_from_line(line: str) -> PasswordEntry:
    match = PASSWORD_ENTRY_REGEX.fullmatch(line)
    if not match:
        raise Exception(f"failed to parse password database entry: {line}")

    return PasswordEntry(
        policy=PasswordPolicy(
            min_occurrences=int(match.group('min')),
            max_occurrences=int(match.group('max')),
            letter=match.group('letter'),
        ),
        password=match.group('password'),
    )


def does_password_satisfy_policy(password: str, policy: PasswordPolicy) -> bool:
    occurrences = len([letter for letter in password if letter == policy.letter])
    return policy.min_occurrences <= occurrences <= policy.max_occurrences


def main():
    # load the 'passwords' from our input file
    with open('input/day2.txt') as f:
        entries = [build_password_entry_from_line(line) for line in f if line]

    valid_entries = [entry for entry in entries if does_password_satisfy_policy(entry.password, entry.policy)]

    print(f"there seem to be {len(valid_entries)} entries!")


if __name__ == '__main__':
    main()
