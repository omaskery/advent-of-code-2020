from typing import List, Dict, IO, Optional, Union, Tuple
from dataclasses import dataclass
import string


@dataclass
class Measurement:
    value: int
    measurement_unit: str


@dataclass
class Passport:
    birth_year: int
    issue_year: int
    expiration_year: int
    height: Measurement
    hair_colour: str
    eye_colour: str
    passport_id: str
    country_id: Optional[str]


@dataclass
class InvalidPassport:
    fields: Dict[str, str]
    reason: str


class PassportValidationError(Exception):

    def __init__(self, fields: Dict[str, str], reason: str):
        self.fields = fields
        self.reason = reason

    def __str__(self):
        return f"invalid passport: {self.reason} ({self.fields})"


def build_passport_from_fields(fields: Dict[str, str]) -> Passport:
    required_fields = [
        'byr', 'iyr', 'eyr',
        'hgt', 'hcl', 'ecl',
        'pid', 'cid',
    ]

    # sneaky hack to let north pole passports be legal ;0 omg
    required_fields.remove('cid')

    # check for all the required fields
    has_required_fields = all(
        field in fields
        for field in required_fields
    )
    if not has_required_fields:
        raise PassportValidationError(fields, "does not have all required fields")

    # utility to read height measurements
    def build_measurement_from_field(value: str) -> Measurement:
        if value[-2:] not in ('in', 'cm'):
            raise PassportValidationError(fields, f'"{value[-2:]}" is not a valid measurement unit')

        return Measurement(
            value=int(value[:-2]),
            measurement_unit=value[-2:],
        )

    # read all the passport fields in as the correct types
    passport = Passport(
        birth_year=int(fields['byr']),
        issue_year=int(fields['iyr']),
        expiration_year=int(fields['eyr']),
        height=build_measurement_from_field(fields['hgt']),
        hair_colour=fields['hcl'],
        eye_colour=fields['ecl'],
        passport_id=fields['pid'],
        country_id=fields.get('cid'),
    )

    # validate the passport rules:

    def in_range(value, lower, upper):
        return lower <= value <= upper

    if not in_range(passport.birth_year, 1920, 2002):
        raise PassportValidationError(fields, "invalid birth year")

    if not in_range(passport.issue_year, 2010, 2020):
        raise PassportValidationError(fields, "invalid issue year")

    if not in_range(passport.expiration_year, 2020, 2030):
        raise PassportValidationError(fields, "invalid expiration year")

    if (passport.height.measurement_unit == 'cm' and not in_range(passport.height.value, 150, 193))\
            or (passport.height.measurement_unit == 'in' and not in_range(passport.height.value, 59, 76)):
        raise PassportValidationError(fields, "invalid height")

    if passport.hair_colour[0:1] != '#':
        raise PassportValidationError(fields, "hair colour must start with #")
    if len(passport.hair_colour) != 7:
        raise PassportValidationError(fields, "hair colour must consist of # followed by 6 hex digits")
    if not all(letter in string.hexdigits for letter in passport.hair_colour[1:]):
        raise PassportValidationError(fields, "hair colour digits must be valid hex digits (a-z, 0-9)")

    if passport.eye_colour not in ('amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'):
        raise PassportValidationError(fields, "eye colour invalid")

    if len(passport.passport_id) != 9:
        raise PassportValidationError(fields, "passport ID must be a 9 digit number including leading 0s")
    if not all(digit in string.digits for digit in passport.passport_id):
        raise PassportValidationError(fields, "passport ID must only consist of digits (0-9)")

    return passport


def load_passports(f: IO) -> Tuple[List[Passport], List[InvalidPassport]]:
    """loads all of the passports from the provided IO object"""

    # record all the good and bad passports we've read in
    invalid_passports = []
    valid_passports = []

    def create_passport():
        # try and build a valid passport
        try:
            valid_passports.append(build_passport_from_fields(fields))
        # if the passport is invalid, record it as such
        except PassportValidationError as e:
            invalid_passports.append(InvalidPassport(
                fields=e.fields,
                reason=e.reason,
            ))
        except Exception:
            print(f"failed to build passport from fields {fields}")
            raise

    fields = {}
    # go through each line of the file
    for line in f:
        # if this is a blank line and we've read some fields in so far, then this is the end of a passport
        if not line.strip() and fields:
            # so store the fields we've read so far as a new passport
            create_passport()
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
        create_passport()

    return valid_passports, invalid_passports


def main():
    # load the passports from the input file
    with open('input/day4.txt') as f:
        valid_passports, invalid_passports = load_passports(f)

    print(f"loaded {len(valid_passports) + len(invalid_passports)} passports")
    for p in invalid_passports:
        print(f"- invalid passport {p.fields} reason: {p.reason}")
    print(f"number of valid passports: {len(valid_passports)}!")


if __name__ == '__main__':
    main()
