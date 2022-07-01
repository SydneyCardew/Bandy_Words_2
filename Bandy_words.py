import os
import argparse
import Bandy_functions as bf
import Dict_Maker as dm
import Combo_Counter as cc
from random import choice
from random import seed
from Bandy_classes import Configuration
from Bandy_classes import Discography
from Bandy_classes import Album


def main():
    config = Configuration('DEFAULT')  # retrieves default configuration

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
    parser.add_argument("type", help="the type of name to be generated. Allowed types are: album, band, genre"
                                     "song, fullalbum, discog.")
    parser.add_argument("number", help="the number of names to be generated")
    args = parser.parse_args()
    bandy_type = args.type.upper()

    if args.user:
        config = Configuration('CUSTOM')

    if args.dictmaker:
        dm.dict_maker()

    if args.combocounter:
        cc.combo_counter(config)

    if args.setseed:
        seed(args.setseed)
        config.store_seed(args.setseed)
    else:
        random_seed = bf.random_source()
        seed(int(random_seed))
        config.store_seed(random_seed)

    log = []

    # retrieves rule and vocab dictionaries
    rules_dict = bf.get_json(os.getcwd() + config.rules_path)
    vocab_dict = bf.get_json(os.getcwd() + config.vocab_path)
    eleven_dict = bf.get_json(os.getcwd() + config.eleven_path)

    # main logic
    answer_list = []
    if bandy_type in rules_dict.keys():
        for x in range(int(args.number)):
            rule_list = rules_dict[bandy_type]
            rule = choice(rule_list)
            answer = bf.make_name(rule, vocab_dict, config.bounds, bandy_type)
            if args.eleven:
                answer = bf.eleven_mode(answer, eleven_dict, config.eleven_rarity)
            answer_list.append(answer)
            log.append((rule, answer))
        if not args.quiet:
            bf.out_print(answer_list)
        if args.txtsave:
            bf.text_saver(answer_list, config, bandy_type)
        if args.csvsave:
            bf.csv_saver(answer_list, config, bandy_type)
        if args.log:
            bf.make_log(log, config)

    elif bandy_type == 'FULLALBUM':
        for x in range(int(args.number)):
            title = bf.make_name(choice(rules_dict['ALBUM']), vocab_dict, config.bounds)
            answer_list.append(Album(title, rules_dict['SONG'], vocab_dict, config))
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
            answer_list.append(Discography(rules_dict, vocab_dict, config))
        if not args.quiet:
            bf.out_print(answer_list, 'discog')
        if args.txtsave:
            bf.text_saver(answer_list, config, bandy_type, 'discog')
        if args.csvsave:
            bf.csv_saver(answer_list, config, bandy_type, 'discog')
        if args.log:
            bf.make_log(log, config, 'discog')

    else:
        bf.error_state('bad_rule')


if __name__ == "__main__":
    main()

