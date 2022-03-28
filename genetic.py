import itertools
from enums import Society
# Notes for next time
# Create a lookup table for the history string comparisons (4^6 if doing memory-3), something like -
# enumerate(itertools.product(list(Society), repeat=6))
# will need to switch it so the index isnt the key and is instead the value i.e.
# for i v, make it v i

# Agent:
# History (e.g. last 3 games) length 6 - BBVSFB
# Strategy (Chromosome) - length of 4^6 with evolving outputs for the lookup table (BVFBSFSBFB....)
# will use index from lookup table to get the gene which relates to the 'learned' choice to switch society

# May not use if defining index as base 4


def generate_lookup_dictionary():
    '''Generates the dictionary which maps all possible memories of previous encounters to an index which is used to 
        select a gene from the chromosome which will be the decided society to switch to.'''
    lookup_dict = {y: x for x, y in dict(
        enumerate(itertools.product(list(Society), repeat=6))).items()}

    return lookup_dict
