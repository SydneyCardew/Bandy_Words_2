#!/usr/bin/env python3

"""Combo_Counter is a module that counts the number of possible combinations the current installation of Bandy Words
is capable of generating.
"""

import os
import argparse
import numpy as np
import Bandy_functions as bf
import Dict_Maker as dm
from Bandy_classes import Configuration


def combination_enumerator(rules_dict, vocab_dict, config):
    """counts the total possible combinations that the current Bandy Words installation can generate"""
    all_rules = []
    for key, value in rules_dict.items():
        all_rules.extend(value)
    total_combinations = 0
    for rule in set(all_rules):
        rule_combinations = []
        raw_list = bf.string_partition(rule)
        rule_list = [x for y in raw_list for x in y]  # flattens the raw list
        for word in rule_list:
            if word.isupper():
                if word == 'NUMBER':
                    # the * 2 accounts for the conversion of numbers to letters by the number rule
                    rule_combinations.append((config.bounds[1] - config.bounds[0]) * 2)
                    # this accounts for the insertion of ' by the number rule
                    rule_combinations.append(config.bounds[1] - config.start_apostrophe_year)
                else:
                    rule_combinations.append(len(vocab_dict[word]))
        total_combinations += np.prod(rule_combinations)
    return total_combinations


def combo_counter(config):
    """main logic, callable from other modules"""
    rules_dict = bf.get_json(os.getcwd() + config.rules_path)
    vocab_dict = bf.get_json(os.getcwd() + config.vocab_path)
    display_number = "{:,}".format(combination_enumerator(rules_dict, vocab_dict, config))
    print(f"This installation of Bandy Words can generate {display_number}"
          f" unique strings.")


def main():
    """this function quarantines the argument parsing, and allows Combo_Counter.py to run as a stand-alone module"""
    config = Configuration('DEFAULT')  # retrieves default configuration

    # argument parsing
    parser = argparse.ArgumentParser(prog="Combo Counter")
    parser.add_argument("-dm", "--dictmaker", action='store_true', help="runs dict_maker.py first")
    parser.add_argument("-u", "--user", action='store_true', help="uses custom config settings")
    parser.add_argument("-v", "--version", action='version', version=config.version)
    args = parser.parse_args()

    if args.user:
        config = Configuration('CUSTOM')

    if args.dictmaker:
        dm.dict_maker()

    combo_counter(config)


if __name__ == "__main__":
    main()
