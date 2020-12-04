from dataclasses import dataclass
from typing import List, Dict, IO


@dataclass
class Passport:
    fields: Dict[str, str]


def load_passports(f: IO) -> List[Passport]:
    """loads all of the passports from the provided IO object"""

    passports = []

    fields = {}
    # go through each line of the file
    for line in f:
        # if this is a blank line and we've read some fields in so far, then this is the end of a passport
        if not line.strip() and fields:
            # so store the fields we've read so far as a new passport
            passports.append(Passport(fields=fields))
            # remember to reset the fields to empty ready to read the next passport
            fields = {}

        # chop the line of text by spaces
        parts = line.split()
        # then for each block of text
        for part in parts:
            # split by colon into a key and value
            k, v = part.split(":", maxsplit=1)
            # and record that key and value pair
            fields[k] = v

    # if we get to the end of the file, but have some fields in our dictionary
    # then there was a passport that didn't have a blank line after it because
    # the file ended, so let's just catch that by appending what we have as a passport
    if fields:
        passports.append(Passport(fields=fields))

    return passports


def validate_passport(passport: Passport, required_fields: List[str]) -> bool:
    """determines whether a passport contains all required fields"""

    return all(
        field in passport.fields
        for field in required_fields
    )


def main():
    # load the passports from the input file
    with open('input/day4.txt') as f:
        passports = load_passports(f)

    print(f"loaded {len(passports)} passports")

    required_fields = [
        'byr', 'iyr', 'eyr',
        'hgt', 'hcl', 'ecl',
        'pid', 'cid',
    ]

    # sneaky hack to let north pole passports be legal ;0 omg
    required_fields.remove('cid')

    # build a list of valid passports
    valid_passports = [
        # keep each passport
        p
        # from the passport list
        for p in passports
        # if it's valid
        if validate_passport(p, required_fields)
    ]

    print(f"number of valid passports: {len(valid_passports)}!")


if __name__ == '__main__':
    main()
