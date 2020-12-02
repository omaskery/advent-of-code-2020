from typing import List, Optional, Tuple


def find_values_that_sum_to(values: List[int], target: int) -> Optional[Tuple[int, int]]:
    # look at every number in the list of values, but also track the index of this number into the list
    for index, value in enumerate(values):
        # if the value is equal to or greater than the target, there's no point doing any more thinking
        # as we know the numbers are sorted, we know that this number and all after it are larger than the
        # target, so cannot possibly add together to make the target!
        if value >= target:
            break

        # now compare to every other value in the list
        # note: we can start at the value after the current one (this is why it's useful to know the index!)
        #   this is because we know we've checked all number pairs up to this index in previous loops
        for other_value in values[index + 1:]:
            # again, if the other number is as big as the target, there's no point checking numbers after it
            # as we sorted the values we know they only get even more "too big" after here!
            if other_value >= target:
                break

            # do the two numbers we're looking at add to produce our target? if so, we're done! :D
            if value + other_value == target:
                return value, other_value

    # if we get here, we've searched every combination available, so there is no solution somehow! :(
    return None


def main():
    target = 2020

    # load the numbers from our input file
    with open('input/day1.txt') as f:
        values = [int(line) for line in f if line]

    # sort the numbers so we can make some assumptions
    values.sort()

    # either find a solution, or fail
    solution = find_values_that_sum_to(values, target)

    # check to see if we found a solution
    if not solution:
        print(f"could not find two values that sum to {target} :(")
        return

    # since we got a solution, split it out into the two numbers we found
    a, b = solution

    # display the answer
    print(f"{a} + {b} == {target}! {a} * {b} = {a * b}")


if __name__ == '__main__':
    main()
