import json
from random import choice
from random import randint


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
    return final_words


def out_print(answer_list, mode='normal'):
    for index, item in enumerate(answer_list):
        if mode == 'normal':
            if index < len(answer_list) - 1:
                print(f"{item}, ", end="")
            else:
                print(f"{item}.", end="")
        elif mode == 'discog':
            print(item)


def process(number, index):
    """helps convert numbers into text"""
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
        'Nine')
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
        'Nineteen')
    tens = (
        'Twenty',
        'Thirty',
        'Forty',
        'Fifty',
        'Sixty',
        'Seventy',
        'Eighty',
        'Ninety',
        'Hundred')
    suffixes = (
        '',
        'Thousand',
        'Million',
        'Billion')
    if number == '0':
        return 'Zero'
    number = number.zfill(3)
    words = ''
    hdigit = int(number[0])
    tdigit = int(number[1])
    odigit = int(number[2])
    words += '' if number[0] == '0' else ones[hdigit]
    words += ' Hundred ' if not words == '' else ''
    if (tdigit > 1):
        words += tens[tdigit - 2]
        words += ' '
        words += ones[odigit]
    elif (tdigit == 1):
        words += twos[(int(tdigit + odigit) % 10) - 1]
    elif (tdigit == 0):
        words += ones[odigit]
    if (words.endswith('Zero')):
        words = words[:-len('Zero')]
    else:
        words += ' '
    if (not len(words) == 0):
        words += suffixes[index]
    return words.rstrip()


def make_name(rule, vocab_dictionary, bounds):
    """makes a name from a rule"""
    new_string = ''
    rule_words = rule.split(" ")
    for index, word in enumerate(rule_words):
        if word.isupper():
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
        else:
            new_string += word
        if index < len(rule_words) - 1:
            new_string += ' '
    return new_string.strip()
