from dataclasses import dataclass


COLUMN_WIDTH = 8
ROW_COUNT = 128


LOWER_ROW = 'F'
HIGHER_ROW = 'B'
LOWER_COLUMN = 'L'
HIGHER_COLUMN = 'R'


@dataclass
class SeatPosition:
    """a position of a seat on the plane"""

    row: int
    column: int

    @property
    def seat_id(self):
        """calculate the seat ID from the seat's row and column"""

        return self.row * COLUMN_WIDTH + self.column


def decode_seat_position(code: str) -> SeatPosition:
    """turns a binary space partition code from the input into a seat position"""

    # the row is the first 7 characters
    row_specifier = code[:7]
    # the column is the characters after the first 7
    col_specifier = code[7:]

    return SeatPosition(
        row=binary_search_code(row_specifier, 0, ROW_COUNT-1, LOWER_ROW, HIGHER_ROW),
        column=binary_search_code(col_specifier, 0, COLUMN_WIDTH-1, LOWER_COLUMN, HIGHER_COLUMN),
    )


def binary_search_code(code: str, lower_bound: int, upper_bound: int, down_char: str, up_char: str) -> int:
    """explores the range of numbers using the provided code, binary searching up or down based on specified chars"""

    # we'll keep searching until the search space is just 1 value, making the upper and lower bound the same
    while lower_bound != upper_bound:
        # chop the first letter off the code so we can look at it, leaving the rest for the subsequent iterations
        next_specifier, code = code[0], code[1:]

        # we're going to move the lower bound up by half, or the upper bound down by half
        offset = int((upper_bound - lower_bound + 1) / 2)

        # note that because the upper bound is _inclusive_ (up to and including, rather than up to but not including)
        # we have to deal with some "off by 1"-ness below, see the +1 and -1 in each case!

        # if the code says to use the lower half, move the upper bound down
        if next_specifier == down_char:
            upper_bound = lower_bound + offset - 1
        # if the code says to use the upper half, move the lower bound up
        elif next_specifier == up_char:
            lower_bound = upper_bound - offset + 1
        else:
            raise Exception(f"unexpected character in code: '{next_specifier}'")

    return lower_bound


def main():
    # load the seat positions from the input file
    with open('input/day5.txt') as f:
        seat_positions = [
            decode_seat_position(line)
            for line in f
        ]

    # determine the largest value of seat ID for all seat positions
    highest_seat_id = max(position.seat_id for position in seat_positions)
    print(f"highest seat ID: {highest_seat_id}!")


if __name__ == '__main__':
    main()
