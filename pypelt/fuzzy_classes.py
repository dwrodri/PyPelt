import math
from collections import OrderedDict

class FuzzySet:
    def __init__(self, name: str, a: int, b: int, alpha: int, beta: int):
        self.a = a
        self.b = b
        self.alpha = alpha
        self.beta = beta
        self.name = name

    def get_membership(self, value: float) -> float:
        """
        calculates membership of a value to a function
        :return: float
        :param value: value to be mapped to output using MF
        """
        desired = -1.0
        if value < self.a:
            if value < (self.a-self.alpha):  # return 0 if outside rising crest
                desired = 0.0
            else:
                desired = (value - self.a + self.alpha) / self.alpha
        elif value > self.b:
            if value > (self.b + self.beta):  # return 0 if outside falling crest
                desired = 0.0
            else:
                desired = (self.b + self.beta - value) / self.beta
        else:
            desired = 1.0  # return 1 if between a and b

        return desired

    def __str__(self):
        return '{}: {} {} {} {}'.format(self.name, self.a, self.b, self.alpha, self.beta)

    def __repr__(self):
        return str(self)


class FuzzyVariable:
    def __init__(self, name: str, set_data: str):
        self.sets = []
        self.name = name
        for line in set_data:  # create fuzzy sets from text data
            self.sets.append(FuzzySet(line.split()[0], int(line.split()[1]),
                                      int(line.split()[2]), int(line.split()[3]),
                                      int(line.split()[4])))

    def fuzzify(self, input_value: float)->dict:
        """
        gets the degrees of memberships of every fuzzy set in the domain of the variable
        :param input_value:
        :return: list of membership values
        """
        memberships = {}
        for fuzzy_set in self.sets:
            memberships.setdefault(fuzzy_set.name, fuzzy_set.get_membership(input_value))

        return memberships

    def __str__(self) -> str:
        desired = self.name + ':\n'
        for fuzzy_set in self.sets:
            desired = desired + '\t' + str(fuzzy_set) + '\n'

        return desired

    def __repr__(self) -> str:
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

    def parse_query(self, var_name: str, crisp_val: float) -> dict:
        """
        recieves query from fuzzifier and returns data pertaining to variable
        :type var_name: str
        :param var_name: fuzzy variable name
        :param crisp_val: crisp value to be assessed in each set of the variable
        :return: dicitionary entry with membership to each set in the variable
        """

        variable_states = {}
        # dict structure = {variable_name : {set_name : membership , set_name : membership...}, variable_name:...}

        for variable in self.fuzzy_vars:  # get degrees of membership for antecedent vars based on input
            if variable.name == var_name:
                variable_states.setdefault(var_name, variable.fuzzify(crisp_val))

        return variable_states





