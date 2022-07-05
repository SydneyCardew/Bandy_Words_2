"""This module contains functions used by the Bandy_Words and Combo_counter modules"""

import json
import os
import sys
import requests
import re
import configparser
from random import choice
from random import randint
from random import seed
from datetime import date
import time


def csv_saver(answer_list, config, type, mode='normal'):
    """saves the output in a csv file"""
    output_path = os.getcwd() + config.output_path
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    type_dict = get_type_dict()
    if type not in type_dict.keys():  # this handles situations in which a user has created a new rules
        type = 'OTHER'
    # these lines increment the file name
    increment = 1
    while os.path.exists(f"{output_path}{config.output_name} - {str(increment).zfill(3)}.csv"):
        increment = increment + 1
    file_name = f"{config.output_name} - {str(increment).zfill(3)}.csv"
    # this section writes the txt file
    with open(output_path + file_name, "w") as save_file:
        save_file.write((f"Generated by Bandy Words {config.version} on {date.today()} "
                         f"at {time.strftime('%H:%M:%S')}, {file_name} containing {len(answer_list)} "
                         f"{type_dict[type]}, Seed: {config.seed}\n"))
        for index, item in enumerate(answer_list):
            if mode == 'normal':
                if index < len(answer_list) - 1:
                    save_file.write(f"{item},\n")
                else:
                    save_file.write(f"{item}")
            elif mode == 'discog':
                save_file.write(str(item.csv()))
            elif mode == 'full_album':
                save_file.write(str(item.csv()))


def eleven_mode(string, eleven_dict, eleven_rarity):
    """processes strings to apply the 'eleven' mode"""
    output = ''
    for letter in string:
        if letter in eleven_dict.keys():
            selector = randint(1, eleven_rarity)
            if selector == 1:
                output += eleven_dict[letter]
            else:
                output += letter
        else:
            output += letter
    return output


def error_state(code, config=None, bandy_type=None, word=None):
    """This reports errors to the console and exits the program"""
    if code == 'dict_typo':
        sys.exit(f"FATAL: Error \'{word}\' in Rule_Dictionary.json. Please check "
                 f"\\Dictionaries\\Rules Dictionaries\\{bandy_type.lower()}.txt for typo and recompile.")
    elif code == 'bad_rule':
        sys.exit('FATAL: Invalid rule type. See README.md or use -h for details of allowed rules.')
    elif code == 'too_much':
        sys.exit('FATAL: String generation is capped at 999999. Please input a lower number.')
    elif code == 'random_fail':
        print('WARNING: Retrieval of seed from online source was unsuccessful.\n'
              'Bandy Words will generate random numbers from clock time.')
    elif code == 'album_length':
        sys.exit(f"FATAL: Min album length ({config.min_album_length}) exceeds Max album length"
                 f"{config.max_album_length}. Change values in \\Settings\\Config.ini.")
    elif code == 'bad_setting_syntax':
        sys.exit(f"FATAL: Incorrect setting syntax '{'='.join(bandy_type)}'. Must be '<setting>=<value>'.")
    elif code == 'bad_setting_name':
        sys.exit(f"FATAL: No setting parameter '{bandy_type}'. Consult README.md for valid parameters.")
    elif code == 'bad_settings':
        sys.exit(f"FATAL: A setting in {config} is in an incorrect format. Please reset or consult README.md for"
                 f"correct settings formats.")
    else:
        sys.exit('FATAL: An unknown error has occurred.')


def get_json(path):
    """Pulls a dictionary from the json file"""
    with open(path, 'r+', encoding="utf-8") as dictionary_json:
        dictionary = json.load(dictionary_json)
    return dictionary


def get_text_number(number):
    """retrieves numbers as text"""
    length = len(str(number))
    count = length // 3 if length % 3 == 0 else length // 3 + 1
    copy = count
    words = []
    for i in range(length - 1, -1, -3):
        words.append(process(str(number)[0 if i - 2 < 0 else i - 2: i + 1], copy - count))
        count -= 1
    final_words = ''
    for s in reversed(words):
        temp = s + ' '
        final_words += temp
    return final_words.rstrip()


def make_log(log, config, mode='normal'):
    """makes a log file, allowing the user to see which rule created which output string."""
    log_path = os.getcwd() + config.output_path + "\\Logs\\"
    if not os.path.exists(log_path):
        os.mkdir(log_path)
    increment = 1
    while os.path.exists(f"{log_path}log - {str(increment).zfill(3)}.txt"):
        increment = increment + 1
    file_name = f"log - {str(increment).zfill(3)}.txt"
    type_dict = get_type_dict()
    if type not in type_dict.keys():  # this handles situations in which a user has created a new rules
        type = 'OTHER'
    with open(log_path + file_name, "w") as log_file:
        log_file.write(f"Log by Bandy Words {config.version} on {date.today()} at {time.strftime('%H:%M:%S')} \n"
                       f"{file_name} containing {len(log)} {type_dict[mode.upper()]}.\n"
                       f"Entries are paired with the rule used to create them.\n"
                       f"Seed: {config.seed}\n\n"
                       f"Arguments:\n{config.args_string}\n\n"
                       f"{config}\n"
                       f"---\n\n")
        if mode == 'full_album' or mode == 'discog':
            for entry in log:
                for item in entry:
                    log_file.write(f"{item[0]}\n"
                                   f"{item[1]}\n\n")
        else:
            for item in log:
                log_file.write(f"{item[0]}\n"
                               f"{item[1]}\n\n")


def make_name(rule, vocab_dictionary, config, bandy_type=None):
    """makes a name from a rule"""
    new_string_array = []
    rule_words = string_partition(rule)
    for word in rule_words:
        sub_array = []
        for sub_word in word:
            if sub_word.isupper():
                # this try/except throws an error if there is a spelling mistake in one of the rules. ie,
                # 'NUON' instead of 'NOUN'.
                try:
                    if sub_word == 'NUMBER':
                        number = randint(config.bounds[0], config.bounds[1])
                        if config.word_number_rarity > 0:
                            selector = randint(1, config.word_number_rarity)
                        else:
                            selector = 2
                        number = str(number)
                        if selector == 1:
                            number = get_text_number(number)
                        if number.isnumeric() and int(number) > config.start_apostrophe_year and int(number) < 100:
                            if config.apostrophe_rarity > 0:
                                selector = randint(1, config.apostrophe_rarity)
                            else:
                                selector = 2
                            if selector == 1:
                                sub_array.append("'")
                        sub_array.append(number)
                    else:
                        word_list = vocab_dictionary[sub_word]
                        new_word = choice(word_list)
                        sub_array.append(new_word)
                except KeyError:
                    error_state('dict_typo', config, bandy_type, word)
            else:
                if sub_word == 'i' and config.capitalise_lone_i:  # capitalises i's
                    sub_array.append(sub_word.upper())
                else:
                    sub_array.append(sub_word)
        new_string_array.append("".join(sub_array))
    new_string = " ".join(new_string_array)
    if config.capitalise_first_letter:  # capitalises first letter if the appropriate config is set.
        return (new_string[0].upper() + new_string[1:]).strip()
    else:
        return new_string.strip()


def out_print(answer_list, mode='normal'):
    """prints the output to the terminal"""
    for index, item in enumerate(answer_list):
        if mode == 'normal':
            if index < len(answer_list) - 1:
                print(f"{item}, ", end="")
            else:
                print(f"{item}.", end="")
        elif mode == 'discog' or 'fullalbum':
            print(item)


def process(number, index):
    """helps convert integer numbers into text strings"""
    ones = (
        'Zero',
        'One',
        'Two',
        'Three',
        'Four',
        'Five',
        'Six',
        'Seven',
        'Eight',
        'Nine'
        )
    twos = (
        'Ten',
        'Eleven',
        'Twelve',
        'Thirteen',
        'Fourteen',
        'Fifteen',
        'Sixteen',
        'Seventeen',
        'Eighteen',
        'Nineteen'
        )
    tens = (
        'Twenty',
        'Thirty',
        'Forty',
        'Fifty',
        'Sixty',
        'Seventy',
        'Eighty',
        'Ninety',
        'Hundred'
        )
    suffixes = (
        '',
        'Thousand',
        'Million',
        'Billion'
        )
    if number == '0':
        return 'Zero'
    number = number.zfill(3)
    words = ''
    hundreds_digit = int(number[0])
    tens_digit = int(number[1])
    ones_digit = int(number[2])
    words += '' if number[0] == '0' else ones[hundreds_digit]
    words += ' Hundred ' if not words == '' else ''
    if (tens_digit > 1):
        words += tens[tens_digit - 2]
        words += ' '
        words += ones[ones_digit]
    elif (tens_digit == 1):
        words += twos[(int(tens_digit + ones_digit) % 10) - 1]
    elif (tens_digit == 0):
        words += ones[ones_digit]
    if (words.endswith('Zero')):
        words = words[:-len('Zero')]
    else:
        words += ' '
    if (not len(words) == 0):
        words += suffixes[index]
    return words.rstrip()


def random_source(config):
    """retrieves a truly random seed number to initiate pseudorandom number generation"""
    random = requests.get(
        'https://www.random.org/integers/?num=1&min=1&max=999999&col=1&base=10&format=plain&rnd=new')
    if random.status_code == 200:  # checks if the request was successful
        for line in random:
            random_output = int(str(line)[2:-3])
    else:  # reports to console and resorts to a pseudorandom number generated by the 'random' module
        error_state('random_fail', config)
        seed()
        random_output = randint(1, 999999)
    return random_output


def make_config_from_dict(config_dict):
    """makes a configparser config object from a dict"""
    new_config = configparser.ConfigParser()
    for section, parameters in config_dict.items():
        new_config[section] = {}
        for parameter, setting in parameters.items():
            new_config[section][parameter] = setting
    return new_config


def set_config(config_class, config_string=None):
    """allows user to alter the settings using command line arguments"""
    #  reads the current state of config.ini
    config = configparser.ConfigParser()
    config.read(os.getcwd() + '\\Settings\\Config.ini')
    config_dict = {s: dict(config.items(s)) for s in config.sections()}  # constructs a dict from the current Config.ini
    new_config = make_config_from_dict(config_dict)
    #  if there is no config_string, the function runs in 'reset' mode
    if config_string:
        #  Processes the input string from the argument
        if '=' not in config_string:
            error_state('bad_setting_syntax', config_class)
        raw_list = config_string.split(',')
        processed_list = []
        for entry in raw_list:
            processed_list.append(entry.strip().split('='))
        for entry in processed_list:
            if len(entry) > 2:
                error_state('bad_setting_syntax', config_class, entry)
        #  Changes the settings and reports to the terminal
        for entry in processed_list:
            if entry[0] in new_config['CUSTOM']:
                new_config['CUSTOM'][entry[0]] = entry[1]
            else:
                error_state('bad_setting_name', config_class, entry[0])
            print(f"'{entry[0]}' in User Settings set to '{entry[1]}'")
    # this handles resetting
    else:
        confirmation = input("This will reset user settings to default. Enter [Y] to confirm:")
        if confirmation.upper() != 'Y':
            sys.exit('User settings unchanged.')
        else:
            for parameter, setting in config_dict['MAIN'].items():
                config_dict['CUSTOM'][parameter] = setting
            new_config = make_config_from_dict(config_dict)
            print('User settings reset to defaults.')
    with open(os.getcwd() + '\\Settings\\Config.ini', "w") as config_file:
        new_config.write(config_file)
    sys.exit('Settings changed successfully.')


def string_partition(string):
    """partitions string into usable sub-arrays using regex. the regexr object combines positive look-aheads and
    positive look-behinds, allowing punctuation marks to be quarantined from the rest of the rules string and then
    reinserted in their correct positions.
    """
    regexr = re.compile(r"(?=[,.!?:;#+/\\()\[\]{\}\-&*=%£$@~|]+)|(?<=[,.!?:;#+/\\()\[\]{\}\-&*=%£$@~|])")
    test_array = string.split(" ")
    string_array = []
    for each in test_array:
        sub_array = []
        split_string = (regexr.split(each))
        for unit in split_string:
            if unit != '':  # ignores any empty strings
                sub_array.append(unit)
        string_array.append(sub_array)
    return string_array


def text_saver(answer_list, config, type, mode='normal'):
    """saves the output in a txt file"""
    output_path = os.getcwd() + config.output_path
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    type_dict = get_type_dict()
    if type not in type_dict.keys():  # this handles situations in which a user has created a new rules
        type = 'OTHER'
    # these lines increment the file name
    increment = 1
    while os.path.exists(f"{output_path}{config.output_name} - {str(increment).zfill(3)}.txt"):
        increment = increment + 1
    file_name = f"{config.output_name} - {str(increment).zfill(3)}.txt"
    # this section writes the txt file
    with open(output_path + file_name, "w") as save_file:
        save_file.write(f"Generated by Bandy Words {config.version} on {date.today()} at {time.strftime('%H:%M:%S')} \n"
                        f"{file_name} containing {len(answer_list)} {type_dict[type]}.\n"
                        f"Seed: {config.seed}\n\n"
                        f"---\n\n")
        for index, item in enumerate(answer_list):
            if mode == 'normal':
                if index < len(answer_list) - 1:
                    save_file.write(f"{item}\n")
                else:
                    save_file.write(f"{item}")
            elif mode == 'discog' or 'fullalbum':
                save_file.write(str(item))
                if index < len(answer_list) - 1:
                    save_file.write("---\n\n")


def get_type_dict():
    """returns an appropriate string for labelling txt and csv files"""
    type_dict = {
        'ALBUM': 'album titles',
        'BAND': 'band names',
        'SONG': 'song names',
        'GENRE': 'musical genres',
        'OTHER': 'strings from a user-created rule',
        'FULLALBUM': 'full albums',
        'DISCOG': 'discographies'
    }
    return type_dict
