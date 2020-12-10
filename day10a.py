
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

    # we'll keep track of how many times we've seen each value of differences
    differences = {}
    # go through each rating pair-wise
    for prev_value, value in zip(sorted_ratings[:-1], sorted_ratings[1:]):
        # calculate the difference
        difference = value - prev_value
        # get the current count or default it to 0
        count = differences.setdefault(difference, 0)
        # update the count
        differences[difference] = count + 1

    # get the differences we've been asked for, defaulting to 0 if they're missing
    one_jolt_differences = differences.get(1, 0)
    three_jolt_differences = differences.get(3, 0)

    print("1-jolt differences ({}) x 3-jolt differences ({}) = {}".format(
        one_jolt_differences,
        three_jolt_differences,
        one_jolt_differences * three_jolt_differences,
    ))


if __name__ == "__main__":
    main()
