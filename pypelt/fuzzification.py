from pypelt.fuzzy_classes import FuzzyKB
import matplotlib.pyplot as plt


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


def infer(rule_stacks: list) -> list:
    pass


def visualize_system(kb: FuzzyKB, inputs: dict, rule_stacks: list):
    """
    A function that renders the fuzzy rulebase in matplotlib.
    :type rule_stacks: parsed rulebase in stack matrix form
    :param kb: FuzzyKB storing sets to be visualized
    :param inputs: crisp inputs that will be x
    :param rule_stacks: rulebase in stack matrix form
    """
    # get fuzzified values for inputs
    pelts = fuzzify(inputs, kb)

    # define parameters for subplots
    rows = len(rule_stacks)
    cols = int((len(max(rule_stacks, key=len)) - 1) / 3)  # amount of cols = amount of most amount of vars referred to

    current_rule_counter = 0  # iteration tracker used for picking subgraphs

    plt.figure()
    for current_rule in rule_stacks:
        current_rule_counter += 1
        current_set_counter = 0  # select rightmost subgraph in row
        while current_rule:
            current_word = current_rule.pop()  # get top of stack

            if current_word == 'then':  # parse consequent
                print(current_set_counter * current_rule_counter)
                current_target_set_name = current_rule.pop()
                current_var = kb.fuzzy_vars[current_rule.pop()]

                for set_key in current_var.sets:  # pick subgraph and load sets
                    set_data = current_var.sets[set_key].dump_points()
                    plt.subplot(rows, cols, current_rule_counter * cols - current_set_counter)
                    plt.title(current_var.name)
                    if set_key == current_target_set_name:
                        plt.plot(set_data, [0, 1, 1, 0], "b-")  # plot the consequent set
                    else:
                        plt.plot(set_data, [0, 1, 1, 0], "k-")  # plot the rest of the sets in the domain
                current_set_counter += 1  # move to left subgraph

            elif current_word == 'is':  # parse antecedent set
                current_target_set_name = current_rule.pop()
                current_var = kb.fuzzy_vars[current_rule.pop()]
                for set_key in current_var.sets:  # pick subgraph and load sets
                    set_data = current_var.sets[set_key].dump_points()
                    plt.subplot(rows, cols, current_rule_counter * cols - current_set_counter)
                    plt.title(current_var.name)
                    if set_key == current_target_set_name:
                        plt.plot(set_data, [0, 1, 1, 0], "r-")  # plot the antecedent set
                        plt.plot(inputs[current_var.name], pelts[current_var.name][current_target_set_name], "ro")
                        #  plot fuzzy point
                    else:
                        plt.plot(set_data, [0, 1, 1, 0], "k-")  # plot the rest of the sets in that domain 
                current_set_counter += 1
            else:
                continue  # this will be where I parse the logic operator, if I don't feel like parsing it in preview
    plt.show()
