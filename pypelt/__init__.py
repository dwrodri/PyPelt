import sys
from pypelt.input_parser import InputParser
from pypelt.fuzzy_classes import *
import pypelt.fuzzification

if __name__ == '__main__':
    parser = InputParser(sys.argv[1])
    kb = FuzzyKB(parser.file_data_dict)
    pypelt.fuzzification.visualize_system(kb, parser.input_values, parser.rule_stacks)

