from typing import List, Optional, Tuple


def find_values_that_sum_to(values: List[int], target: int) -> Optional[Tuple[int, int, int]]:
    # look at every number in the list of values, but also track the index of this number into the list
    for index, first_value in enumerate(values):
        # if the value is equal to or greater than the target, there's no point doing any more thinking
        # as we know the numbers are sorted, we know that this number and all after it are larger than the
        # target, so cannot possibly add together to make the target!
        if first_value >= target:
            break

        # now compare to every other value in the list
        # note: we can start at the value after the current one (this is why it's useful to know the index!)
        #   this is because we know we've checked all number pairs up to this index in previous loops
        for inner_index, second_value in enumerate(values[index + 1:]):
            # again, if the other number is as big as the target, there's no point checking numbers after it
            # as we sorted the values we know they only get even more "too big" after here!
            if second_value >= target:
                break

            # same idea as above, but looking at possible third numbers
            for third_value in values[inner_index+1:]:
                # again, if it's too big, no point checking the bigger numbers after it
                if third_value >= target:
                    break

                # do the three numbers we're looking at add to produce our target? if so, we're done! :D
                if first_value + second_value + third_value == target:
                    return first_value, second_value, third_value

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
        print(f"could not find three values that sum to {target} :(")
        return

    # since we got a solution, split it out into the two numbers we found
    a, b, c = solution

    # display the answer
    print(f"{a} + {b} + {c} == {target}! {a} * {b} * {c} = {a * b * c}")


if __name__ == '__main__':
    main()
