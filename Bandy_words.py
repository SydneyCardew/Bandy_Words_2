#!/usr/bin/env python3

"""Bandy words is a module for generating interesting, amusing (and occasionally outrageous) names, album titles,
song titles and genres for fictious bands. For more information see README.MD
"""

import os
import argparse
import sys
import Bandy_functions as bf
import Dict_Maker as dm
import Combo_Counter as cc
from random import choice
from random import seed
from Bandy_classes import Configuration
from Bandy_classes import Discography
from Bandy_classes import Album


def main():
    """main program function"""
    config = Configuration('MAIN')  # retrieves default configuration

    # argument parsing
    parser = argparse.ArgumentParser(prog="Bandy Words")
    parser.add_argument("-dm", "--dictmaker", action='store_true', help="runs dict_maker.py first")
    parser.add_argument("-u", "--user", action='store_true', help="uses custom config settings")
    parser.add_argument("-e", "--eleven", action='store_true', help="activates 'eleven' mode")
    parser.add_argument("-ts", "--txtsave", action='store_true', help="saves output as a txt file")
    parser.add_argument("-cs", "--csvsave", action='store_true', help="saves output as a csv file")
    parser.add_argument("-q", "--quiet", action='store_true', help="prevents printing to terminal")
    parser.add_argument("-v", "--version", action='version', version=config.version)
    parser.add_argument("-l", "--log", action='store_true', help="enables logging of rules")
    parser.add_argument("-ss", "--setseed", type=int, help="enter a seed number")
    parser.add_argument("-cc", "--combocounter", action='store_true', help="runs combo counter")
    parser.add_argument("-sc", "--showconfig", action='store_true', help="shows current configuration settings")
    parser.add_argument("-set", "--setconfig", type=str, help="change a config setting")
    parser.add_argument("-reset", "--resetconfig", action='store_true', help="resets user settings to default")
    parser.add_argument("type", help="the type of name to be generated. Allowed types are: album, band, genre"
                                     "song, fullalbum, discog.", default='band', nargs='?', type=str)
    parser.add_argument("number", help="the number of names to be generated", default=1, nargs='?', type=int)
    args = parser.parse_args()

    if args.user:  # over-writes default configuration if the 'user' argument is set.
        config = Configuration('CUSTOM')

    config.store_arg_string(args)

    if args.setconfig:
        bf.set_config(config, args.setconfig)

    if args.resetconfig:
        bf.set_config(config)

    bandy_type = args.type.upper()

    if args.showconfig:
        sys.exit(config)

    if args.dictmaker:  # runs Dict_Maker.py if the 'dictmaker' argument is set.
        dm.dict_maker()

    if args.combocounter:  # runs Combo_Counter.py if the 'combocounter' argument is set.
        cc.combo_counter(config)

    if args.setseed:  # stores a user-defined seed in the config file, if present.
        seed(args.setseed)
        config.store_seed(args.setseed)
    else:  # or retrieves a random seed
        random_seed = bf.random_source(config)
        seed(int(random_seed))
        config.store_seed(random_seed)

    log = []  # pairs of rules and their resultant strings are stored in the log array as tuples.

    # retrieves rule and vocab dictionaries
    rules_dict = bf.get_json(os.getcwd() + config.rules_path)
    vocab_dict = bf.get_json(os.getcwd() + config.vocab_path)
    eleven_dict = bf.get_json(os.getcwd() + config.eleven_path)

    # main logic
    answer_list = []
    if int(args.number) > 999999:
        bf.error_state('too_much', config)
    if bandy_type in rules_dict.keys():
        for x in range(int(args.number)):
            rule_list = rules_dict[bandy_type]
            rule = choice(rule_list)
            answer = bf.make_name(rule, vocab_dict, config, bandy_type)
            if args.eleven:  # if the 'eleven' argument is set, this processes the string to add umlauts.
                answer = bf.eleven_mode(answer, eleven_dict, config.eleven_rarity)
            answer_list.append(answer)
            log.append((rule, answer))
        if not args.quiet:  # default behaviour is to print the output of Bandy Words to the console.
            # The 'quiet' argument suppresses this behaviour
            bf.out_print(answer_list)
        if args.txtsave:  # outputs a text file if the 'txtsave' argument is set.
            bf.text_saver(answer_list, config, bandy_type)
        if args.csvsave:  # outputs a csv file if the 'csvsave' argument is set
            bf.csv_saver(answer_list, config, bandy_type)
        if args.log:  # outputs a log file if the 'log' argument is set
            bf.make_log(log, config, bandy_type)

    elif bandy_type == 'FULLALBUM':
        for x in range(int(args.number)):
            title = bf.make_name(choice(rules_dict['ALBUM']), vocab_dict, config)
            new_album = Album(title, rules_dict['SONG'], vocab_dict, config)
            answer_list.append(new_album)
            log.append(new_album.log)
        # see the first 'if' statement to this 'elif' for an explanation of the following.
        if not args.quiet:
            bf.out_print(answer_list, 'full_album')
        if args.txtsave:
            bf.text_saver(answer_list, config, bandy_type, 'full_album')
        if args.csvsave:
            bf.csv_saver(answer_list, config, bandy_type, 'full_album')
        if args.log:
            bf.make_log(log, config, 'full_album')

    elif bandy_type == 'DISCOG':
        for x in range(int(args.number)):
            new_discog = Discography(rules_dict, vocab_dict, config)
            answer_list.append(new_discog)
            log.append(new_discog.log)
        # see the first 'if' statement to this 'elif' for an explanation of the following.
        if not args.quiet:
            bf.out_print(answer_list, 'discog')
        if args.txtsave:
            bf.text_saver(answer_list, config, bandy_type, 'discog')
        if args.csvsave:
            bf.csv_saver(answer_list, config, bandy_type, 'discog')
        if args.log:
            bf.make_log(log, config, 'discog')

    else:
        bf.error_state('bad_rule', config)


if __name__ == "__main__":
    main()

