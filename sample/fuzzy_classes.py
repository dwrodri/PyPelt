import math
from collections import OrderedDict


class FuzzyVariable:
    def __init__(self, name: str, set_data: str):
        self.sets = []
        self.name = name
        for line in set_data:  # create fuzzy sets from text data
            self.sets.append(FuzzySet(line.split()[0], int(line.split()[1]),
                                      int(line.split()[2]), int(line.split()[3]),
                                      int(line.split()[4])))

    def __str__(self) -> str:
        desired = self.name + ':\n'
        for fuzzy_set in self.sets:
            desired = desired + '\t' + str(fuzzy_set) + '\n'

        return desired

    def __repr__(self) -> str:
        return str(self)


class FuzzySet:
    def __init__(self, name: str, a: int, b: int, alpha: int, beta: int):
        self.a = a
        self.b = b
        self.alpha = alpha
        self.beta = beta
        self.name = name

    def fuzzify(self, value) -> float:
        """
        calculates membership of a value to a function
        :param value: value to be mapped to output using MF
        :return: float between 0 and 1
        """
        if value < self.a:
            if value < (self.a-self.alpha):  # return 0 if outside rising crest
                return 0.0
            else:
                return math.sqrt(2) * (value - (self.a-self.alpha))
        elif value > self.b:
            if value > (self.b + self.beta):  # return 0 if outside falling crest
                return 0.0
            else:
                return math.sqrt(2) * ((self.b + self.beta) - value)
        else:
            return 1.0  # return 1 if between a and b

    def __str__(self):
        return '{}: {} {} {} {}'.format(self.name, self.a, self.b, self.alpha, self.beta)

    def __repr__(self):
        return str(self)


class FuzzyKB:
    def __init__(self, parsed_dict: OrderedDict) -> object:
        """
        FuzzyKB contains all the rules and sets used to build the consequence system
        """
        has_rulebase = False  # first flag for rulebase
        self.rule_data = ['', []]  # tuple for rule data
        self.fuzzy_vars = []

        for key in parsed_dict:  # strip rules away and instantiate FuzzyVariable classes
            if not has_rulebase:
                self.rule_data[0] = key
                self.rule_data[1].extend(parsed_dict[key])
                has_rulebase = True
            else:
                self.fuzzy_vars.append(FuzzyVariable(key, parsed_dict[key]))

    def __str__(self) -> str:
        desired = ''
        for variable in self.fuzzy_vars:
            desired = desired + str(variable) + '\n'

        return desired


class InferenceEngine:

    def __init__(self, data: list):
        self.list = data[0]
        self.rule_strings = data[1]

    def make_inference(self, inputs: list) -> list:
        pass





