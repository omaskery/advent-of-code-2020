from typing import Dict, List, Optional, Iterable


def ways_to_combine_adapters_after(possibilities: Dict[int, List[int]], value: int,
                                   cache: Optional[Dict[int, int]] = None) -> int:
    """work out how many adapter arrangements are after the specified adapter"""

    # if we don't have somewhere to remember our answers, make somewhere, this code is slow
    if cache is None:
        cache = {}

    # have we worked out the answer before?
    result = cache.get(value)
    # if so, return it now
    if result is not None:
        return result

    # how many things can this adapter connect to?
    can_connect_to = possibilities[value]
    # if it can't connect to anything then there's only one "arrangement" of this adapter
    if not can_connect_to:
        return 1

    # otherwise, sum up the possible ways to arrange all the adapters we can choose from
    result = sum(
        ways_to_combine_adapters_after(possibilities, v, cache)
        for v in can_connect_to
    )
    # remember the result so we don't work it out again in future!
    cache[value] = result

    return result


def main():
    # load adapter jolt ratings from the input file
    with open('input/day10.txt') as f:
        adapter_ratings = [
            int(line)
            for line in f
        ]

    # an adapter can tolerate values slightly lower than its rated output
    max_tolerance = 3
    # we're given the effective joltage of the charging outlet
    effective_charger_outlet_joltage = 0
    # we know that the device can take 3 more than the highest adapter rating we own
    device_charging_joltage = max(adapter_ratings) + 3
    print(f"device charging voltage is {device_charging_joltage}")

    # make a sorted list of all relevant joltages involved
    sorted_ratings = [
        # first we have the outlet of the charging port
        effective_charger_outlet_joltage,
        # sort the adapter ratings, then "unpack" the resulting list into this list
        # (the asterisk is what "unpacks" the sorted list so that its elements are
        # inserted into the outer list)
        *sorted(adapter_ratings),
        # finally we have the device charging voltage
        device_charging_joltage,
    ]

    # record the possible choices exist at each step
    possibilities = {}
    # go through each rating
    for idx, value in enumerate(sorted_ratings):
        branches = []
        # how many different adapters could we connect to?
        for next_value in sorted_ratings[idx+1:]:
            if next_value - value <= max_tolerance:
                branches.append(next_value)

        # remember what adapters this adapter could connect to
        possibilities[value] = branches

    combinations = ways_to_combine_adapters_after(possibilities, effective_charger_outlet_joltage)
    print(f"there are {combinations} distinct ways to arrange the adapters")


if __name__ == "__main__":
    main()
