from dataclasses import dataclass
from typing import List, Optional
import enum


@enum.unique
class CellContents(enum.Enum):
    """represent the contents of a single grid cell on the map"""

    OPEN = enum.auto()
    TREE = enum.auto()


@dataclass
class Map:
    """represents a map of the area"""

    rows: List[List[CellContents]]

    @property
    def height(self):
        """retrieve the height of the map in cells"""

        return len(self.rows)

    @property
    def width(self):
        """retrieve the width of the map in cells"""

        return len(self.rows[0])

    def get_contents_at(self, position: 'Vec2') -> Optional[CellContents]:
        """get the contents of the specified cell, accounting for the fact the map repeats on the horizontal axis"""

        # if the position is off the map then return nothing
        if position.y > self.height:
            return None

        # get the row of the map
        row = self.rows[position.y]

        # now get the cell in the map, but modulus the x co-ordinate by the width of the map so that it wraps around
        return row[position.x % len(row)]


def build_row_of_map(line: str) -> List[CellContents]:
    """turns a line from the input file into the cells that make up a row of the map"""

    # record which symbols we treat as what cell contents
    letter_mappings = {
        '.': CellContents.OPEN,
        '#': CellContents.TREE,
    }

    return [
        # map the letter to its corresponding cell contents
        letter_mappings[letter]
        # for every letter in the line
        for letter in line
        # but only if the letter is one we recognise in our mapping
        if letter in letter_mappings
    ]


@dataclass
class Vec2:
    """represent a 2-dimensional vector, which can be used as a coordinate"""

    x: int
    y: int

    def __add__(self, other: 'Vec2') -> 'Vec2':
        """add two vectors together to produce a new one"""

        return Vec2(self.x + other.x, self.y + other.y)


def count_trees_encountered_given_slope(area: Map, start_position: Vec2, slope: Vec2) -> int:
    """
    given a map, starting position and direction of travel, calculates how many trees are encountered on the way down
    """

    # our position is initially the starting position
    position = start_position
    # and we've seen no trees so far
    trees_encountered = 0

    # while we haven't gone off the bottom of the map
    while position.y < area.height:
        # see what we'd hit at the current position
        encountered = area.get_contents_at(position)
        # if we get nothing back, we've gone off the map, so stop!
        if encountered is None:
            break

        # if we've encountered a tree, record that fact
        if encountered == CellContents.TREE:
            trees_encountered += 1

        # either way, we move to the next position based on our velocity, ready for the next loop
        position = position + slope

    return trees_encountered


def main():
    # load the map from the input file
    with open('input/day3.txt') as f:
        map_of_area = Map(rows=[
            build_row_of_map(line)
            for line in f
            if line
        ])

    start_position = Vec2(x=0, y=0)
    # list of all the slopes we need to check
    slopes_to_check = [
        Vec2(x=1, y=1),
        Vec2(x=3, y=1),
        Vec2(x=5, y=1),
        Vec2(x=7, y=1),
        Vec2(x=1, y=2),
    ]

    # we're going to multiply this variable by lots of numbers
    # if we intialise it with 1 it makes the logic easier later
    product_of_encountered = 1

    # check each slope in turn
    for slope in slopes_to_check:
        encountered_on_slope = count_trees_encountered_given_slope(map_of_area, start_position, slope)
        print(f"encountered {encountered_on_slope} trees on the '{slope}' slope!")

        # multiply each result by the running product so far
        product_of_encountered *= encountered_on_slope

    print(f"the product of the trees encountered is {product_of_encountered}!")


if __name__ == '__main__':
    main()
