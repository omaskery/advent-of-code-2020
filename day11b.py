from typing import List, IO, Optional, Dict, Tuple
from dataclasses import dataclass
import pygame
import enum


@enum.unique
class SeatState(enum.Enum):
    """whether a grid of the map is floor, an empty seat or an occupied seat"""

    Floor = enum.auto()
    Empty = enum.auto()
    Occupied = enum.auto()


def parse_seat_state(state: str) -> SeatState:
    """decode text representation of seat state"""

    seat_state_map = {
        '.': SeatState.Floor,
        'L': SeatState.Empty,
        '#': SeatState.Occupied,
    }

    return seat_state_map[state]


@dataclass
class SeatingPlan:
    """the state of all seats"""

    seats: List[SeatState]
    width: int

    @property
    def height(self) -> int:
        """how many rows of seats there are"""

        return int(len(self.seats) / self.width)

    def get(self, x: int, y: int) -> Optional[SeatState]:
        """get the state of a particular seat, returns None if invalid coordinate"""

        # check for valid coordinate
        if x < 0 or y < 0 or x >= self.width or y >= self.height:
            return None

        # get the seat
        index = self._index(x, y)
        return self.seats[index]

    def set(self, x: int, y: int, value: SeatState):
        """update the state of a particular seat"""

        index = self._index(x, y)
        self.seats[index] = value

    def neighbours_of(self, x: int, y: int) -> Dict[Tuple[int, int], bool]:
        """get whether we can see occupied seats in each direction"""

        # all the possible direction vectors that we will look in
        directions = [
            (-1, -1), (+0, -1), (+1, -1),
            (-1, +0),           (+1, +0),
            (-1, +1), (+0, +1), (+1, +1),
        ]

        result = {}
        # for each direction
        for (dx, dy) in directions:
            # start at the adjacent position
            cx, cy = x + dx, y + dy
            # then, until we find an answer...
            while True:
                # get the content of the position we're looking at
                neighbour = self.get(cx, cy)
                # is it empty (off the grid), or an empty seat?
                if neighbour is None or neighbour == SeatState.Empty:
                    # if so the first seat we've seen is not occupied, so we can stop
                    # record that when looking in that direction we can't see an occupied seat
                    result[(dx, dy)] = False
                    break
                # is it an occupied seat?
                if neighbour == SeatState.Occupied:
                    # if so the first seat we've seen is occupied, so we can stop
                    # record that when looking in that direction we can see an occupied seat
                    result[(dx, dy)] = True
                    break

                # otherwise, move onto the next position in that direction
                cx, cy = cx + dx, cy + dy

        return result

    def clone(self) -> 'SeatingPlan':
        """creates a separate copy of the seating plan"""

        return SeatingPlan(
            seats=self.seats[:],
            width=self.width,
        )

    def _index(self, x: int, y: int) -> int:
        """calculate the index into our list of seats based on the seating coordinate"""

        return y * self.width + x


def load_seating_plan(f: IO) -> SeatingPlan:
    """decode seating plan from an input stream"""

    seats = []

    line_width: Optional[int] = None
    for line in f:
        # remove any surrounding whitespace
        line = line.strip()
        # ignore empty lines (e.g. end of file)
        if not line:
            continue

        # record the line length or validate that all lines have the same length
        if line_width is None:
            line_width = len(line)
        elif line_width != len(line):
            raise Exception(f"inconsistent line length in input ({line_width} so far vs {len(line)} in this line)")

        # store all the decoded seats from this line of input
        seats.extend([
            parse_seat_state(letter)
            for letter in line
        ])

    if not line_width:
        raise Exception("no lines read from input!")

    return SeatingPlan(
        seats=seats,
        width=line_width,
    )


def update_seating_plan(plan: SeatingPlan) -> SeatingPlan:
    """apply the rules from the puzzle to the seating plan, producing a new seating plan"""

    # start with a fresh copy to mutate
    next_plan = plan.clone()

    # evaluate the rules for every position in the grid
    for y in range(plan.height):
        for x in range(plan.width):
            current_state = plan.get(x, y)
            # there are only rules for empty or occupied seats, so skip everything else
            if current_state not in (SeatState.Empty, SeatState.Occupied):
                continue

            # count the number of occupied adjacent seats
            neighbours = plan.neighbours_of(x, y)
            number_of_occupied_neighbours = sum(
                1
                for occupied in neighbours.values()
                if occupied
            )

            # by default the next state will be the same as the current state, unless a rule overrides it
            next_state = current_state

            # apply the rules to this seat
            if current_state == SeatState.Empty and number_of_occupied_neighbours == 0:
                next_state = SeatState.Occupied
            elif current_state == SeatState.Occupied and number_of_occupied_neighbours >= 5:
                next_state = SeatState.Empty

            # if the seat state has changed, record the change
            if next_state != current_state:
                next_plan.set(x, y, next_state)

    return next_plan


def count_differences(a: SeatingPlan, b: SeatingPlan) -> int:
    """count how many seats have a different state between two seating plans"""

    return sum(
        # yield a 1 if the seats are different, otherwise a 0
        1 if seat_a != seat_b else 0
        # when comparing each corresponding seat in the two seating plans
        for seat_a, seat_b in zip(a.seats, b.seats)
    )


def main():
    # initialise a game library that lets us draw graphics
    pygame.init()
    # create a graphical window with a certain resolution
    display = pygame.display.set_mode((1280, 1024))

    def _reset():
        """loads the seating plan from the input file"""

        with open('input/day11.txt') as f:
            return load_seating_plan(f)

    # load the initial plan
    seating_plan = _reset()

    # record whether the user wants to keep watching the program think, set to False to exit early
    running = True
    # how should we draw the state of the seats on screen in terms of colours
    plan_colours = {
        SeatState.Empty: (100, 100, 255),
        SeatState.Occupied: (255, 100, 100),
    }
    # create a surface to draw our seating plan to
    seating_plan_surface = pygame.Surface(size=(seating_plan.width, seating_plan.height))
    # start the seating plan as all white
    seating_plan_surface.fill((255, 255, 255))

    # whether or not the simulation continues on its own (True) or whether it waits for you to say "next" (False)
    auto_run = True

    # count the number of simulation steps, just because
    step = 0
    # record how many changes were made to the seating plan in the last simulation update
    changes: Optional[int] = None
    # run until there are no changes, and we haven't manually aborted by setting running to False
    while changes != 0 and running:
        # whether the user has requested that we advance the simulation by a frame
        step_pressed = False

        # handle all the input events from the user
        for event in pygame.event.get():
            # has the user pressed the close button or pressed ALT+F4 or anything?
            if event.type == pygame.QUIT:
                # if so, set the flag so that we exit early
                running = False
                break
            # did a keyboard button go from unpressed to pressed just now?
            elif event.type == pygame.KEYDOWN:
                # if it was the right arrow, we want to manually advance to the next simulation step
                if event.key == pygame.K_RIGHT:
                    step_pressed = True
                # if it was the R key, reset the simulation back to the contents of the puzzle input
                elif event.key == pygame.K_r:
                    seating_plan = _reset()
                # if it was the space key, toggle whether the input plays out on its own, or waits for input
                elif event.key == pygame.K_SPACE:
                    auto_run = not auto_run

        # if we're automatically advancing the simulation, or the user manually asked to step the simulation,
        # then update the simulation
        if auto_run or step_pressed:
            step += 1
            print(f"step {step}")

            # update the simulation
            next_seating_plan = update_seating_plan(seating_plan)
            changes = count_differences(seating_plan, next_seating_plan)
            print(f"  {changes} changes")

            # update the seating plan with the result of the simulation step
            seating_plan = next_seating_plan

        # update the drawing of the seating plan
        for y in range(seating_plan.height):
            for x in range(seating_plan.width):
                seat = seating_plan.get(x, y)
                # does the state of this seat have a colour?
                colour = plan_colours.get(seat)
                # if so, draw the colour
                if colour:
                    seating_plan_surface.set_at((x, y), colour)

        # scale up the small seating plan (each pixel is a seat!) so that it fills the display
        pygame.transform.scale(seating_plan_surface, display.get_size(), display)
        # update the screen with the latest drawing
        pygame.display.flip()

    # count how many seats were occupied
    occupied_seats = sum(
        1
        for seat in seating_plan.seats
        if seat == SeatState.Occupied
    )
    print(f"{occupied_seats} occupied seats when equilibrium reached")


if __name__ == "__main__":
    main()
