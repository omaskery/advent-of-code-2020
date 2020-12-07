from dataclasses import dataclass
from typing import Set, IO, List, Dict, Optional
import string
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


def can_contain(rules: Dict[str, BagContentRule], outer_bag_colour: str, colour_of_bag_to_store: str) -> bool:
    """determine whether, given a ruleset, a bag of a given colour can be stored in an outer bag of a given colour"""

    # try and get the rules associated with the outer bag
    rule_for_outer_bag = rules.get(outer_bag_colour)
    if not rule_for_outer_bag:
        raise Exception(f"invalid bag colour: '{outer_bag_colour}'")

    # if this bag is directly capable of storing the bag to store, we're done!
    if colour_of_bag_to_store in rule_for_outer_bag.can_contain:
        return True

    # otherwise, see if we can store the bag indirectly in one of the bags we can contain
    for bag_colour in rule_for_outer_bag.can_contain:
        # here we utilise recursion to test whether we can store the target bag in this inner bag, or any of
        # the bags that are inside that one! if any can, we're done, because we indirectly can store the bag!
        if can_contain(rules, bag_colour, colour_of_bag_to_store):
            return True

    # if we cannot store the bag directly, and if we can't store it indirectly inside one of our contained
    # bags, then we cannot store the target bag
    return False


def main():
    # load the rules from the input file
    with open('input/day7.txt') as f:
        bag_content_rules = parse_bag_content_rule_file(f)

    # the colour of our fabulous bag
    our_bag_colour = 'shiny gold'

    # count how many bags could contain our bag
    how_many_can_store_our_bag = len([
        # it doesn't matter what we store here, we only need the length of the list, but:
        # record the colour of the bag
        bag_colour
        # for every bag colour described in the rules
        for bag_colour in bag_content_rules
        # if it could, directly or indirectly, contain our bag colour
        if can_contain(bag_content_rules, bag_colour, our_bag_colour)
    ])
    print("there are {} bags that could, directly or indirectly, store our {} bag".format(
        how_many_can_store_our_bag,
        our_bag_colour,
    ))


if __name__ == '__main__':
    main()
