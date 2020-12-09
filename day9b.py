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


def main():
    # load the XMAS numbers from the input file
    with open('input/day9.txt') as f:
        numbers = [
            int(line)
            for line in f
        ]

    # the invalid sum that we're trying to find terms to sum up to
    target_number = 70639851

    # try different sizes of number groups, starting at 2 numbers, working up to almost every number in the set
    for window_size in range(2, len(numbers)-2):
        print(f"testing for {window_size} sized groups of numbers")

        # for every contiguous group of numbers in the entire set
        for window in sliding_window_over(numbers, window_size):
            # try summing all those numbers, and see if they match the target number
            if sum(window) == target_number:
                print(f"you can sum {len(window)} numbers to produce {target_number}")
                biggest, smallest = max(window), min(window)
                print(f"the largest number is {biggest} and the smallest is {smallest}")
                print(f"the encryption weakness is the sum of these numbers: {smallest + biggest}")

                # exit the function now we've found a solution
                return


if __name__ == "__main__":
    main()
