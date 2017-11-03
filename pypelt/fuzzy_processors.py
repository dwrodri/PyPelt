from pypelt.fuzzy_classes import FuzzyKB
from operator import mul


def fuzzify(inputs: dict, kb: FuzzyKB) -> dict:
    """
    gets crisp input from parser and queries the KB for memberships of respective sets in variable domains
    :param inputs: list of crisp inputs
    :param kb: the fuzzy knowledgebase singleton
    :return: dictionary with antecedent set memberships
    """
    pelts = {}
    for key in inputs:  # query kb for fuzzy values based on crisp inputs for antecedent sets
        pelts.update(kb.get_fuzzy_vals(key, float(inputs[key])))

    return pelts


def infer(rule_stacks: list, pelts: dict, kb: FuzzyKB) -> list:
    """
    fires every rule from the rulebase
    :type pelts: dict
    :param kb: the knowledge base with all the fuzzy variables
    :param rule_stacks: stack of rules from input parser
    :param pelts: degrees of membership of crisp values for each variable
    :return: list of tuples corresponding to weights and fuzzy values in the domain of each rule
    """
    fired_rule_data = []
    for rule in rule_stacks:
        antecedents = []  # temp storage for antecedent data
        consequent_var_name = ''  # temp storage for consequent data
        consequent_set_name = ''
        has_and = False
        has_or = False
        while rule:
            word = rule.pop()
            if word == 'then':  # load name of consequent into memory
                consequent_set_name = rule.pop()
                consequent_var_name = rule.pop()
            elif word == 'is':  # load antecedent fuzzy value onto list
                antecedent_set_name = rule.pop()
                antecedent_var_name = rule.pop()
                antecedents.append(pelts[antecedent_var_name][antecedent_set_name])
            elif word == 'and':
                has_and = True
            elif word == 'or':
                has_or = True
        if has_and:
            weight = min(antecedents)
        elif has_or:
            weight = max(antecedents)
        else:  # handle rules with one antecedent
            weight = antecedents.pop()
        z_value = kb.fuzzy_vars[consequent_var_name].sets[consequent_set_name].get_consequent(weight)
        fired_rule_data.append((weight, z_value))

    return fired_rule_data


def debug_infer(rule_stacks: list, pelts: dict, kb: FuzzyKB) -> list:
    """
     fires every rule from the rulebase and gets influences as opposed to z values for debugging purposes
     :type rule_stacks: list
     :param kb: the knowledge base with all the fuzzy variables
     :param rule_stacks: stack of rules from input parser
     :param pelts: degrees of membership of crisp values for each variable
     :return: list of tuples corresponding to weights and fuzzy values in the domain of each rule
     """
    debug_fired_rule_data = []
    print(rule_stacks)
    for rule in rule_stacks:
        antecedents = []  # temp storage for antecedent data
        consequent_var_name = ''  # temp storage for consequent data
        consequent_set_name = ''
        has_and = False
        has_or = False
        while rule:
            word = rule.pop()
            if word == 'then':  # load name of consequent into memory
                consequent_set_name = rule.pop()
                consequent_var_name = rule.pop()
            elif word == 'is':  # load antecedent fuzzy value onto list
                antecedent_set_name = rule.pop()
                antecedent_var_name = rule.pop()
                antecedents.append(pelts[antecedent_var_name][antecedent_set_name])
            elif word == 'and':
                has_and = True
            elif word == 'or':
                has_or = True
        if has_and:
            weight = min(antecedents)
        elif has_or:
            weight = max(antecedents)
        else:  # handle rules with one antecedent
            weight = antecedents.pop()
        influences = kb.fuzzy_vars[consequent_var_name].sets[consequent_set_name].get_influences(weight)
        debug_fired_rule_data.append((weight, *influences))

    return debug_fired_rule_data


def defuzzify(fired_rule_tuples: list) -> float:
    """
    defuzzify consequent fuzzy values based on weighted average
    :param fired_rule_tuples: list of tuples containing consequent values and matching rule weights
    :return: The weighted average
    """
    print(list(map(lambda x: x[0], fired_rule_tuples)))
    return sum([w*z for w,z in fired_rule_tuples]) / sum(map(lambda x: x[0], fired_rule_tuples))



