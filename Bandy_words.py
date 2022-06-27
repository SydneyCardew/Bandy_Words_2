import os
import argparse
import Bandy_functions as bf
import Dict_Maker as dm
from random import choice
from Bandy_classes import Configuration
from Bandy_classes import Discography
from Bandy_classes import Album


def main():
    config = Configuration('DEFAULT')  # retrieves default configuration

    # argument parsing
    parser = argparse.ArgumentParser(prog="Band Namer")
    parser.add_argument("-dm", "--dictmaker", action='store_true', help="runs dict_maker.py first")
    parser.add_argument("-u", "--user", action='store_true', help="uses custom config settings")
    parser.add_argument("-e", "--eleven", action='store_true', help="activates 'eleven' mode")
    parser.add_argument("-ts", "--textsave", action='store_true', help="saves output as a txt file")
    parser.add_argument("-q", "--quiet", action='store_true', help="prevents printing to terminal")
    parser.add_argument("-v", "--version", action='version', version=config.version)
    parser.add_argument("type", help="the type of name to be generated")
    parser.add_argument("number", help="the number of names to be generated")
    args = parser.parse_args()
    bandy_type = args.type.upper()

    if args.user:
        config = Configuration('CUSTOM')

    if args.dictmaker:
        dm.dict_maker()

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
            answer = bf.make_name(rule, vocab_dict, config.bounds)
            if args.eleven:
                answer = bf.eleven_mode(answer, eleven_dict, config.eleven_rarity)
            answer_list.append(answer)
        if not args.quiet:
            bf.out_print(answer_list)
        if args.textsave:
            bf.text_saver(answer_list, config, bandy_type)

    elif bandy_type == 'FULLALBUM':
        for x in range(int(args.number)):
            title = bf.make_name(choice(rules_dict['ALBUM']), vocab_dict, config.bounds)
            answer_list.append(Album(title, rules_dict['SONG'], vocab_dict, config))
        if not args.quiet:
            bf.out_print(answer_list, 'full_album')
        if args.textsave:
            bf.text_saver(answer_list, config, bandy_type, 'full_album')

    elif bandy_type == 'DISCOG':
        for x in range(int(args.number)):
            answer_list.append(Discography(rules_dict, vocab_dict, config))
        if not args.quiet:
            bf.out_print(answer_list, 'discog')
        if args.textsave:
            bf.text_saver(answer_list, config, bandy_type, 'discog')

    else:
        print('Invalid Rule Type')


if __name__ == "__main__":
    main()

