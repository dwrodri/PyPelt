import sys
from sample.input_parser import InputParser
from sample.fuzzy_classes import *

if __name__ == '__main__':
    parser = InputParser("../input_files/test1.txt")
    kb = FuzzyKB(parser.file_data_dict)
    print(kb)