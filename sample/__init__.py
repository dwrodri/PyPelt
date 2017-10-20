import sys
from sample.input_parser import InputParser

if __name__ == '__main__':
    parser = InputParser('../test1.txt')
    parser.dump_dict()
