from collections import OrderedDict


class InputParser:
    file_data_dict = OrderedDict()
    input_values = {}
    rule_stacks = []

    def __init__(self, input_file: OrderedDict) -> object:

        """
        Reads text files and separates data into two structures: a dictionary for sets and rules
        :rtype: InputParser
        """
        new_entry_mode = True  # Toggle between create mode and define mode
        current_entry_title = ''  # the title of the element

        # NOTE: file_data_dict = {{element_name : [defining_line1, defining_line2...]}, {element2_name ... }} NOTE:

        with open(input_file) as file_stream:
            for line in file_stream:

                if line == '\n':  # empty line used to switch modes
                    new_entry_mode = not new_entry_mode  # switch modes
                    continue
                else:
                    line = line.strip('\n')  # get rid of pesky newline character for lines that matter

                if new_entry_mode:  # create new entry in dict
                    if '=' in line:  # if the name line has an equals sign in it, it's an input value
                        self.input_values.setdefault(line.split()[0], line.split()[-1])

                    elif line in self.file_data_dict:  # check for re-used entry names
                        exit(1)

                    else:  # add new entry to dict
                        self.file_data_dict.setdefault(line, [])
                        current_entry_title = line

                else:  # if not in create mode, add line to current entry
                    self.file_data_dict[current_entry_title].append(line)

        # NOTE: the first element will be the rule base, which is then popped, and parsed into an array of reverse
        # polish command stacks

        for rule in list(self.file_data_dict.items())[0][1]:
            antecedent, consequent = rule[len('Rule # If the '):].split(
                'then the ')  # split the string and cut off the first two words
            parsed_stack = []  # stack that has been arranged in reverse polish notation
            holding_stack = []  # temporary holding space for words
            has_and = None  # flag determining whether antecendent is uses "and" or "or". None throws an error
            for word in antecedent.split():  # reformat rule into reverse polish notation
                if word == 'or':
                    has_and = False
                elif word == 'and':
                    has_and = True
                elif word == 'is':
                    holding_stack.append(word)
                elif word == 'the':
                    continue
                else:
                    parsed_stack.append(word)
                    if holding_stack:  # check holding stack to see if it's holding an operator
                        parsed_stack.append(holding_stack.pop())  # push operator to stack if there is one waiting

            if has_and:  # append set operator to be used
                parsed_stack.append('and')
            else:
                parsed_stack.append('or')

            parsed_stack.extend(consequent.split(' will be '))  # push consequent to stack
            parsed_stack.append('then')
            self.rule_stacks.append(parsed_stack)  # add the rule stack to the list

        del self.file_data_dict[list(self.file_data_dict.items())[0][0]]  # remove rules from dict

    def dump_dict(self) -> None:

        """
        Prints the dictionary collected from reading the input file.
        """
        for key in self.file_data_dict:
            print('Entry Name: ' + key)
            for value in self.file_data_dict[key]:
                print('\t' + value)
