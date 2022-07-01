import json
import os
import sys
import requests
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


def error_state(code, bandy_type=None, word=None):
    """This reports errors to the console and exits the program"""
    if code == 'dict_typo':
        sys.exit(f"FATAL: Error \'{word}\' in Rule_Dictionary.json. Please check "
                 f"\\Dictionaries\\Rules Dictionaries\\{bandy_type}.txt for typo and recompile")
    elif code == 'bad_rule':
        sys.exit('FATAL: Invalid rule type. See README.md or use -h for details of allowed rules.')
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
    """makes a log file"""
    log_path = os.getcwd() + config.output_path + "\\Logs\\"
    if not os.path.exists(log_path):
        os.mkdir(log_path)
    increment = 1
    while os.path.exists(f"{log_path}log - {str(increment).zfill(3)}.txt"):
        increment = increment + 1
    file_name = f"log - {str(increment).zfill(3)}.txt"
    with open(log_path + file_name, "w") as log_file:
        log_file.write(f"Log by Bandy Words {config.version} on {date.today()} at {time.strftime('%H:%M:%S')} \n"
                       f"{file_name} containing {len(log)} entries.\n"
                       f"Entries are paired with the rule used to create them.\n"
                       f"Seed: {config.seed}\n\n")
        if mode == 'normal':
            for item in log:
                log_file.write(f"{item[0]}\n"
                               f"{item[1]}\n\n")
        else:
            log_file.write("Full logs are only available for band, album, song and genre generation.")


def make_name(rule, vocab_dictionary, bounds, bandy_type=None):
    """makes a name from a rule"""
    new_string = ''
    rule_words = rule.split(" ")
    for index, word in enumerate(rule_words):
        if word.isupper():
            # this try/except throws an error if there is a spelling mistake in one of the rules. ie,
            # 'NUON' instead of 'NOUN'.
            try:
                if word == 'NUMBER':
                    number = randint(bounds[0], bounds[1])
                    selector = randint(1, 3)
                    number = str(number)
                    if selector == 1:
                        number = get_text_number(number)
                    if number.isnumeric() and int(number) > 50 and int(number) < 100:
                        selector = randint(1, 3)
                        if selector == 1:
                            new_string += "'"
                    new_string += number
                else:
                    word_list = vocab_dictionary[word]
                    new_word = choice(word_list)
                    new_string += new_word
            except KeyError:
                error_state('dict_typo', bandy_type, word)
        else:
            new_string += word
        if index < len(rule_words) - 1:
            new_string += ' '
    return (new_string[0].upper() + new_string[1:]).strip()


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


def random_source():
    random = requests.get(
        'https://www.random.org/integers/?num=1&min=1&max=999999&col=1&base=10&format=plain&rnd=new')
    if random.status_code == 200:
        for line in random:
            random_output = int(str(line)[2:-3])
    else:
        error_state('random_fail')
        seed()
        random_output = randint(1, 999999)
    return random_output


def text_saver(answer_list, config, type, mode='normal'):
    """saves the output in a txt file"""
    output_path = os.getcwd() + config.output_path
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    type_dict = get_type_dict()
    # these lines increment the file name
    increment = 1
    while os.path.exists(f"{output_path}{config.output_name} - {str(increment).zfill(3)}.txt"):
        increment = increment + 1
    file_name = f"{config.output_name} - {str(increment).zfill(3)}.txt"
    # this section writes the txt file
    with open(output_path + file_name, "w") as save_file:
        save_file.write(f"Generated by Bandy Words {config.version} on {date.today()} at {time.strftime('%H:%M:%S')} \n"
                        f"{file_name} containing {len(answer_list)} {type_dict[type]}.\n"
                        f"Seed: {config.seed}\n\n")
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
        'FULLALBUM': 'full albums',
        'DISCOG': 'discographies'
    }
    return type_dict
