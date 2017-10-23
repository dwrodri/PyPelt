import sys
from pypelt.input_parser import InputParser
from pypelt.fuzzy_classes import *
from pypelt.fuzzification import fuzzify

if __name__ == '__main__':
    parser = InputParser("../input_files/test1.txt")
    kb = FuzzyKB(parser.file_data_dict)
    print(fuzzify(parser.input_values, kb))
