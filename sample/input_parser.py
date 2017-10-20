class InputParser:
    file_data_dict = {}
    input_values = []

    def __init__(self, inputFile):

        new_entry_mode = True  # Toggle between create mode and define mode
        current_entry_title = ''  # the title of the element

        # NOTE: file_data_dict = {{element_name : [defining_line1, defining_line2...]}, {element2_name ... }}
        # NOTE: the first element will be the rule base
        # NOTE: sets with weights defined at the end will have the weight definition at the very end.

        with open(inputFile) as file_stream:
            for line in file_stream:

                if line == '\n':  # empty line used to switch modes
                    new_entry_mode = not new_entry_mode  # switch modes
                    continue
                else:
                    line = line.strip('\n') #get rid of pesky newline character

                if new_entry_mode:  # create new entry in dict
                    if '=' in line:  # if the name line has an equals sign in it, it's an input value
                        self.input_values.append(line)

                    elif line in self.file_data_dict:  # check for re-used entry names
                        exit(1)

                    else:  # add new entry to dict
                        self.file_data_dict.setdefault(line, [])
                        current_entry_title = line

                else:  # if not in create mode, add line to current entry
                    self.file_data_dict[current_entry_title].append(line)

    def dump_dict(self):
        for key in self.file_data_dict:
            print('Entry Name: ' + key)
            for value in self.file_data_dict[key]:
                print('\t' + value)
