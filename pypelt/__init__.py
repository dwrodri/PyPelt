import sys
from pypelt.input_parser import InputParser
from pypelt.fuzzy_classes import *
import pypelt.fuzzification

if __name__ == '__main__':
    parser = InputParser(sys.argv[1])  # parse file
    kb = FuzzyKB(parser.fuzzy_vars_dict)  # generate knowledgebase with fuzzy sets and variables
    pypelt.fuzzification.visualize_system(kb, parser.input_values, parser.rule_stacks)

