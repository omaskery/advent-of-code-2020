from typing import IO, Dict, Optional
from dataclasses import dataclass
import re


@dataclass
class BagContentRule:
    """rule indicating, for a bag of a given colour, how many bags of other colours it can contain"""

    bag_colour: str
    can_contain: Dict[str, int]


# rule to match an optionally numbered bag colour
BAG_CONTENT_RULE_REGEX = re.compile(
    r'((\d+)\s+)?(\w+\s+\w+)\s*bags?'
)


def parse_bag_content_rule_file(f: IO) -> Dict[str, BagContentRule]:
    """loads bag content rules from a file"""

    def parse_line(line) -> Optional[BagContentRule]:
        matches = BAG_CONTENT_RULE_REGEX.findall(line)

        # if there aren't at least two matches (the outer bag colour, and at least one contains or 'no bags')
        # then this is some kind of invalid line!
        if len(matches) < 2:
            return None

        # the first match is the outer bag colour, it has no count associated with it
        _, _, bag_colour = matches[0]
        # if the next match is no other, then this bag can not contain any other bags
        if matches[1][2] == 'no other':
            can_contain = {}
        # otherwise we can now determine what coloured bags this can contain
        else:
            # create a dictionary
            can_contain = {
                # map the colour of the contained bag to the number of times it may be stored in the outer bag
                match[2]: int(match[1])
                # for each match in the list of matches, skipping the first match (as that's the outer bag)
                for match in matches[1:]
            }

        return BagContentRule(
            bag_colour=bag_colour,
            can_contain=can_contain,
        )

    # map each rule to the outer bag colour
    return {
        # map the outer bag colour to the bag contents rule
        parsed.bag_colour: parsed
        # for each line in the file
        for line in f
        # if the result of parsing the line (stored in parsed) is truthy (aka, not None in this instance)
        if (parsed := parse_line(line))
    }


def bags_contained_by(rules: Dict[str, BagContentRule], outer_bag_colour: str) -> int:
    """determine how many bags are contained within a given bag colour based on the given rules"""

    # try and get the rules associated with the bag colour
    rule_for_outer_bag = rules.get(outer_bag_colour)
    if not rule_for_outer_bag:
        raise Exception(f"invalid bag colour: '{outer_bag_colour}'")

    bags_stored = 0

    # tally up how many bags are stored inside the bags inside us
    for bag_colour, count in rule_for_outer_bag.can_contain.items():
        # record how many of this bag colour we can store directly
        bags_stored += count
        # here we utilise recursion to count how many bags are inside this bag,
        # noting that we can store 'count' bags of this colour, so however many bags
        # it contain, we can store 'count' times that!
        bags_stored += bags_contained_by(rules, bag_colour) * count

    return bags_stored


def main():
    # load the rules from the input file
    with open('input/day7.txt') as f:
        bag_content_rules = parse_bag_content_rule_file(f)

    # the colour of our fabulous bag
    our_bag_colour = 'shiny gold'

    # how many bags do we need inside our bag?
    bags_required = bags_contained_by(bag_content_rules, our_bag_colour)

    print(f"for a {our_bag_colour} bag you'd need {bags_required} individual bags")


if __name__ == '__main__':
    main()
