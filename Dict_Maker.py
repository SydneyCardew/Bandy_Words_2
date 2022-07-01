"""Dict_Maker is a module that takes the Rules and Vocab Dictionaries stored as txt files in the \\Rules Dictionaries\\
and \\Vocab Dictionaries\\ directories and transforms them into less easily human-readable json files that can be
used by the main Bandy Words program. It can be run independently or called via a command-line argument in Bandy Words
"""

import os


def json_maker(directory, directory_string, target):
    """Creates json file from .txt files"""
    json = open(os.getcwd() + '\\Dictionaries\\' + target, "w", encoding="utf-8")
    json.write("{")
    file_count = 0
    for file in os.listdir(directory):
        file_count += 1
    for file_index, file in enumerate(os.listdir(directory)):
        file_name = str(file).upper()
        dict_name = file_name[:-4]
        count = 0
        with open(directory_string + file_name, "r+") as open_file:
            for line in open_file:
                count += 1
        with open(directory_string + file_name, "r+") as open_file:
            json.write(f'"{dict_name}":[')
            for index, line in enumerate(open_file):
                if line[:3] == "###":
                    pass
                else:
                    entry = line.strip('\n')
                    json.write(f'"{entry}"')
                    if index < (count - 1):
                        json.write(', ')
            json.write("]")
            if file_index < (file_count - 1):
                json.write(',')
            json.write('\n')
    json.write("}")


def dict_maker():
    """main dict_maker logic"""
    directory_strings = [os.getcwd() + "\\Dictionaries\\Vocab Dictionaries\\", os.getcwd() +
                         "\\Dictionaries\\Rules Dictionaries\\"]
    directories = [str(os.fsencode(directory_strings[0]))[2:-1], str(os.fsencode(directory_strings[1]))[2:-1]]
    targets = ('Vocab_Dictionary.json', 'Rules_Dictionary.json')

    for x in range(0, 2):
        json_maker(directory_strings[x], directories[x], targets[x])
    print("Dict_maker has executed successfully.")


def main():
    dict_maker()


if __name__ == "__main__":
    main()

