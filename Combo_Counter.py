import os
import argparse
import numpy as np
import Bandy_functions as bf
import Dict_Maker as dm
from Bandy_classes import Configuration


def combination_enumerator(rules_dict, vocab_dict, config):
    all_rules = []
    for key, value in rules_dict.items():
        all_rules.extend(value)
    total_combinations = 0
    for rule in set(all_rules):
        rule_combinations = []
        for word in rule.split():
            if word.isupper():
                if word == 'NUMBER':
                    rule_combinations.append(config.bounds[1] - config.bounds[0])
                else:
                    rule_combinations.append(len(vocab_dict[word]))
        total_combinations += np.prod(rule_combinations)
    return total_combinations


def combo_counter(config):
    rules_dict = bf.get_json(os.getcwd() + config.rules_path)
    vocab_dict = bf.get_json(os.getcwd() + config.vocab_path)
    print(f"This installation of Bandy Words can generate {combination_enumerator(rules_dict, vocab_dict, config)}"
          f" unique strings.")


def main():
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
