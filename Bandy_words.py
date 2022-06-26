import os
import argparse
import Bandy_functions as bf
from random import choice
from Bandy_classes import Configuration
from Bandy_classes import Discography


parser = argparse.ArgumentParser(prog="Band Namer")
parser.add_argument("-l", "--log", action='store_true', help="saves a log")
parser.add_argument("-u", "--user", action='store_true', help="uses custom config settings")
parser.add_argument("-e", "--eleven", action='store_true', help="activates 'eleven' mode")
parser.add_argument("-s", "--save", action='store_true', help="saves this configuration to the custom config settings")
parser.add_argument("type", help="the type of name to be generated")
parser.add_argument("number", help="the number of names to be generated")
args = parser.parse_args()

if args.user:
    config_seg = 'CUSTOM'
else:
    config_seg = 'DEFAULT'

config = Configuration(config_seg)

rules_dict = bf.get_json(os.getcwd() + config.rules_path)
vocab_dict = bf.get_json(os.getcwd() + config.vocab_path)
eleven_dict = bf.get_json(os.getcwd() + config.eleven_path)

answer_list = []
if args.type.lower() in rules_dict.keys():
    for x in range(int(args.number) + 1):
        rule_list = rules_dict[args.type.lower()]
        rule = choice(rule_list)
        answer = bf.make_name(rule, vocab_dict, config.bounds)
        if args.eleven:
            answer = bf.eleven_mode(answer, eleven_dict, config.eleven_rarity)
        answer_list.append(answer)
    bf.out_print(answer_list)
elif args.type == 'discog':
    for x in range(int(args.number) + 1):
        answer_list.append(Discography(rules_dict, vocab_dict, config))
    bf.out_print(answer_list, 'discog')
else:
    print('Invalid Rule Type')


