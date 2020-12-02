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


# this is a regular expression, it is designed to match specific patterns of text (the lines of text in the input file)
# it splits the line up into the individual pieces described in the puzzle
PASSWORD_ENTRY_REGEX = re.compile(r'^\s*(?P<min>\d+)-(?P<max>\d+)\s+(?P<letter>[a-zA-Z])\s*:\s*(?P<password>.+)\s*$')


def build_password_entry_from_line(line: str) -> PasswordEntry:
    # try and match our regular expression to the line of text from the input
    match = PASSWORD_ENTRY_REGEX.fullmatch(line)
    if not match:
        raise Exception(f"failed to parse password database entry: {line}")

    # now it's matched, we can store the individual values into our password entry
    return PasswordEntry(
        policy=PasswordPolicy(
            min_occurrences=int(match.group('min')),
            max_occurrences=int(match.group('max')),
            letter=match.group('letter'),
        ),
        password=match.group('password'),
    )


def does_password_satisfy_policy(password: str, policy: PasswordPolicy) -> bool:
    # count the number of letters in the password that match the policy
    occurrences = len([letter for letter in password if letter == policy.letter])
    # return whether the number of occurrences is within the limits specified in the policy
    return policy.min_occurrences <= occurrences <= policy.max_occurrences


def main():
    # load the 'passwords' from our input file
    with open('input/day2.txt') as f:
        entries = [build_password_entry_from_line(line) for line in f if line]

    # find all the entries that pass the corresponding password policy
    valid_entries = [entry for entry in entries if does_password_satisfy_policy(entry.password, entry.policy)]

    print(f"there seem to be {len(valid_entries)} entries!")


if __name__ == '__main__':
    main()
