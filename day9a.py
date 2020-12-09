from typing import Iterator, List


def sliding_window_over(collection: Iterator[int], window_size: int) -> Iterator[List[int]]:
    """slides a window of a specified size across a collection, yielding the values within that window"""

    # values in the window
    window = []

    # go through the entire collection to build up the window and yield it when full
    for value in collection:
        # add a value into the window
        window.append(value)
        # if the window isn't full yet, just skip to the next iteration to continue filling it
        if len(window) < window_size:
            continue

        # if the window has too many values in it, remove the oldest values, to keep it at 'window_size'
        if len(window) > window_size:
            window = window[-window_size:]

        # yield the numbers in the current window so the caller can examine it
        # note that this allows the caller to examine the value _before_ we continue this function!
        yield window


def can_sum_to(terms: List[int], target: int) -> bool:
    """determines whether a target number can be constructed by pairs of numbers from the list of terms"""

    # for every number
    for idx, a in enumerate(terms):
        # compare it to every other number we haven't already tried summing it with
        for b in terms[idx+1:]:
            # if the sum of values matches the target, bam, we're done! :)
            if a + b == target:
                return True

    # if we found no sums that match the target, we're done
    return False


def main():
    # load the XMAS numbers from the input file
    with open('input/day9.txt') as f:
        numbers = [
            int(line)
            for line in f
        ]

    # number of numbers that make up the preamble
    preamble_length = 25
    # we're gonna look at the preamble, followed by the number that follows
    numbers_to_consider_at_once = preamble_length + 1
    # look at the numbers in a sliding window
    for window in sliding_window_over(numbers, numbers_to_consider_at_once):
        # split the numbers in the window into the preamble and...
        preamble = window[:preamble_length]
        # ...the final number that must be a sum of any two numbers in the preamble
        number_to_consider = window[-1]

        # if you can't make the target number from the numbers in the preamble, then
        # we've found the first step of the XMAS attack! :O
        if not can_sum_to(preamble, number_to_consider):
            print(f"first number to not be made from preamble numbers: {number_to_consider}")
            break


if __name__ == "__main__":
    main()
