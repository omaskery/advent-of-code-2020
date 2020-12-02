from dataclasses import dataclass
import re


@dataclass
class PasswordPolicy:
    position_a: int
    position_b: int
    letter: str


@dataclass
class PasswordEntry:
    policy: PasswordPolicy
    password: str


# this is a regular expression, it is designed to match specific patterns of text (the lines of text in the input file)
# it splits the line up into the individual pieces described in the puzzle
PASSWORD_ENTRY_REGEX = re.compile(r'^\s*(?P<a>\d+)-(?P<b>\d+)\s+(?P<letter>[a-zA-Z])\s*:\s*(?P<password>.+)\s*$')


def build_password_entry_from_line(line: str) -> PasswordEntry:
    # try and match our regular expression to the line of text from the input
    match = PASSWORD_ENTRY_REGEX.fullmatch(line)
    if not match:
        raise Exception(f"failed to parse password database entry: {line}")

    # now it's matched, we can store the individual values into our password entry
    return PasswordEntry(
        policy=PasswordPolicy(
            position_a=int(match.group('a')),
            position_b=int(match.group('b')),
            letter=match.group('letter'),
        ),
        password=match.group('password'),
    )


def does_password_satisfy_policy(password: str, policy: PasswordPolicy) -> bool:
    matching_letter_positions = [
        # keep the indexes (1 indexed)
        index + 1
        # of every letter in the password
        for index, letter in enumerate(password)
        # where the index is one of the ones specified in the policy
        # AND the letter in that position matches the letter specified in the policy
        if (index + 1) in (policy.position_a, policy.position_b) and letter == policy.letter
    ]

    # the rules say that EXACTLY ONE of those positions can contain the letter
    return len(matching_letter_positions) == 1


def main():
    # load the 'passwords' from our input file
    with open('input/day2.txt') as f:
        entries = [build_password_entry_from_line(line) for line in f if line]

    # find all the entries that pass the corresponding password policy
    valid_entries = [entry for entry in entries if does_password_satisfy_policy(entry.password, entry.policy)]

    print(f"there seem to be {len(valid_entries)} entries!")


if __name__ == '__main__':
    main()
