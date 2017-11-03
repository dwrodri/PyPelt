import sys
import matplotlib.pyplot as plt
from pypelt.input_parser import InputParser
from pypelt.fuzzy_classes import *
from pypelt.fuzzy_processors import *
from copy import deepcopy


def visualize_system(knowledgebase: FuzzyKB, inputs: dict, rule_stacks: list) -> None:
    """
    A function that renders the fuzzy rulebase in matplotlib.
    :type rule_stacks: parsed rulebase in stack matrix form
    :param knowledgebase: FuzzyKB storing sets to be visualized
    :param inputs: crisp inputs that will be x
    :param rule_stacks: rulebase in stack matrix form
    """
    # get fuzzified values for inputs
    pelts = fuzzify(deepcopy(inputs), knowledgebase)

    # get influences
    debug_inferences = debug_infer(deepcopy(rule_stacks), deepcopy(pelts), knowledgebase)

    # get production values
    fixed_inferences = infer(deepcopy(rule_stacks), deepcopy(pelts), knowledgebase)

    # print defuzzified answer
    print(defuzzify(deepcopy(fixed_inferences)))

    # define parameters for subplots
    rows = len(rule_stacks)
    cols = (len(max(rule_stacks, key=len)) - 1)//3  # amount of cols = amount of most amount of vars referred to

    current_rule_counter = 0  # iteration tracker used for picking subgraphs

    plt.figure()
    for current_rule in rule_stacks:
        current_rule_counter += 1
        current_set_counter = 0  # select rightmost subgraph in row
        while current_rule:
            current_word = current_rule.pop()  # get top of stack

            if current_word == 'then':  # parse consequent
                current_target_set_name = current_rule.pop()
                current_var = knowledgebase.fuzzy_vars[current_rule.pop()]

                for set_key in current_var.sets:  # pick subgraph and load sets
                    set_data = current_var.sets[set_key].dump_points()
                    plt.subplot(rows, cols, current_rule_counter * cols - current_set_counter)
                    plt.title(current_var.name)
                    if set_key == current_target_set_name:
                        plt.plot(set_data, [0, 1, 1, 0], "b-")  # plot the consequent set
                        temp = debug_inferences.pop(0)
                        print(temp)
                        plt.plot(temp[-1], temp[0], "bo")  # left point
                        plt.plot(temp[1], temp[0], "bo")  # right point
                        plt.plot(fixed_inferences.pop(0)[-1], temp[0], "yo")
                    else:
                        plt.plot(set_data, [0, 1, 1, 0], "k-")  # plot the rest of the sets in the domain
                current_set_counter += 1  # move to left subgraph

            elif current_word == 'is':  # parse antecedent set
                current_target_set_name = current_rule.pop()
                current_var = knowledgebase.fuzzy_vars[current_rule.pop()]
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


if __name__ == '__main__':
    parser = InputParser(sys.argv[1])  # parse file
    kb = FuzzyKB(parser.fuzzy_vars_dict)  # generate knowledgebase with fuzzy sets and variables
    # fuzzy_vals = fuzzify(parser.input_values, kb)  # get fuzzy values from KB
    # inferences = infer(deepcopy(parser.rule_stacks), deepcopy(fuzzy_vals), kb)  # make inference in consequent domain
    visualize_system(kb, deepcopy(parser.input_values), deepcopy(parser.rule_stacks))



