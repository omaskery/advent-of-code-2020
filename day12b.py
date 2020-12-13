import enum
import math
from dataclasses import dataclass, field


@enum.unique
class Operation(enum.Enum):
    """what the navigation computer wants us to do next"""

    North = enum.auto()
    East = enum.auto()
    South = enum.auto()
    West = enum.auto()
    Left = enum.auto()
    Right = enum.auto()
    Forward = enum.auto()


def compass_direciton_to_vector(operation: Operation) -> 'Vector2':
    """convert a compass direction into a vector"""

    mapping = {
        Operation.North: Vector2(+0.0, -1.0),
        Operation.East:  Vector2(+1.0, +0.0),
        Operation.South: Vector2(+0.0, +1.0),
        Operation.West:  Vector2(-1.0, +0.0),
    }
    return mapping[operation]


@dataclass
class Instruction:
    """instruction from the navigation computer"""

    operation: Operation
    argument: int


def parse_instruction(line: str) -> Instruction:
    """parse a navigation computer instruction from a line of input text"""

    operation_str = line[0]
    argument = int(line[1:])

    operation_map = {
        'N': Operation.North,
        'E': Operation.East,
        'S': Operation.South,
        'W': Operation.West,
        'L': Operation.Left,
        'R': Operation.Right,
        'F': Operation.Forward,
    }
    operation = operation_map[operation_str]

    return Instruction(
        operation=operation,
        argument=argument,
    )


@dataclass
class Vector2:
    """represent a 2-dimensional vector, a direction and a magnitude"""

    x: float = 0.0
    y: float = 0.0

    def __add__(self, other: 'Vector2') -> 'Vector2':
        """returns the sum of this vector and the provided vector"""

        return Vector2(
            x=self.x + other.x,
            y=self.y + other.y,
        )

    def __mul__(self, other: float) -> 'Vector2':
        """returns the result of multiplying this vector by the provided scalar value"""

        return Vector2(
            x=self.x * other,
            y=self.y * other,
        )

    def angle(self) -> float:
        """the angle of this vector from 'east'"""

        return math.degrees(math.atan2(self.y, self.x))

    def magnitude_squared(self) -> float:
        """the magnitude of this vector squared"""

        return self.x ** 2 + self.y ** 2

    def magnitude(self) -> float:
        """the magnitude of this vector"""

        return math.sqrt(self.magnitude_squared())

    def rotate_by(self, angle_degrees: float) -> 'Vector2':
        """rotate this vector around its origin by the specified number of degrees"""

        # work out the current rotation
        current_angle_degrees = self.angle()
        # work out its current length
        current_magnitude = self.magnitude()

        # just create a new vector with an updated rotation, but the same length
        return Vector2.from_heading(
            heading_degrees=current_angle_degrees + angle_degrees,
            magnitude=current_magnitude,
        )

    def manhattan_distance(self) -> float:
        """returns the manhattan distance of this vector"""

        return abs(self.x) + abs(self.y)

    @staticmethod
    def from_heading(heading_degrees: float, magnitude: float) -> 'Vector2':
        """constructs a vector from a heading (in degrees) and magnitude"""

        heading_radians = heading_degrees * math.pi / 180.0
        return Vector2(
            x=math.cos(heading_radians) * magnitude,
            y=math.sin(heading_radians) * magnitude,
        )


@dataclass
class Ship:
    """the ship that follows navigation instructions"""

    position: Vector2 = field(default_factory=Vector2)
    waypoint: Vector2 = field(default_factory=lambda: Vector2(x=10.0, y=-1.0))

    def follow_instruction(self, instruction: Instruction):
        """updates the ship's position by following a navigation instruction"""

        # first see if we're moving the waypoint in an absolute compass direction
        if instruction.operation in (Operation.North, Operation.East, Operation.South, Operation.West):
            self.waypoint = self.waypoint + compass_direciton_to_vector(instruction.operation) * instruction.argument
        # otherwise if we're rotating the waypoint left and right
        elif instruction.operation in (Operation.Left, Operation.Right):
            heading_change = instruction.argument
            if instruction.operation == Operation.Left:
                heading_change = -heading_change
            self.waypoint = self.waypoint.rotate_by(heading_change)
        # finally, are we just moving toward the current waypoint
        elif instruction.operation == Operation.Forward:
            self.position = self.position + self.waypoint * instruction.argument


def main():
    # load the input instructions
    with open('input/day12.txt') as f:
        instructions = [
            parse_instruction(line)
            for line in f
        ]

    # create a new ship
    ship = Ship()
    # and have the ship follow the navigation instructions
    for i in instructions:
        ship.follow_instruction(i)

    print(f"ships manhattan distance from its starting position: {int(ship.position.manhattan_distance())}")


if __name__ == "__main__":
    main()
