"""This module contains classes used by the Bandy_Words and Combo_Counter modules"""

import Bandy_functions as bf
from random import randint
import os
import configparser as conf
from random import choice


class Discography:
    """The Discography class both stores and generates a discography object,
    and produces the string representation output to the terminal or txt file.
    """
    def __init__(self, rules_dict, vocab_dict, config):
        """generates the discography object from basic Bandy Words dictionaries"""
        self.config = config
        self.rules_dict = rules_dict
        self.vocab_dict = vocab_dict
        self.band_rules = rules_dict['BAND']
        self.album_rules = rules_dict['ALBUM']
        self.genre_rules = rules_dict['GENRE']
        self.song_rules = rules_dict['SONG']
        self.discog_size = randint(1, self.config.max_discog_size) + 1
        self.log = []
        self.band_rule = choice(self.band_rules)
        self.band_name = bf.make_name(self.band_rule, self.vocab_dict, self.config, 'band')
        self.log.append((self.band_rule, self.band_name))
        self.genre_rule = choice(self.genre_rules)
        self.band_genre = bf.make_name(self.genre_rule, self.vocab_dict, self.config, 'genre')
        self.log.append((self.genre_rule, self.band_genre))
        self.album_list = []
        for x in range(self.discog_size):
            self.album_name_rule = choice(self.album_rules)
            self.title = bf.make_name(self.album_name_rule, self.vocab_dict, self.config, 'album')
            self.new_album = Album(self.title, self.song_rules, self.vocab_dict, self.config)
            self.album_list.append(self.new_album)
            self.log.extend(self.new_album.log)

    def csv(self):
        """generates the representation of the object for csv output"""
        csv_string = f"{self.band_name},\n{self.band_genre},\n"
        for album in self.album_list:
            csv_string += album.csv()
        return csv_string

    def view(self):
        """generates the output string and passes it to __repr__ and __str__"""
        string = f"{self.band_name}\n" \
                 f"Genre: {self.band_genre}\n\n" \
                 f"{self.discog_size} " \
                 f"{'albums' if self.discog_size > 1 else 'album'}\n\n"
        for album in self.album_list:
            string += str(album)
        return string

    def __repr__(self):
        return self.view()

    def __str__(self):
        return self.view()


class Album:
    """The Album class stores the album title and track-listing."""
    def __init__(self, title, song_rules, vocab_dict, config):
        self.config = config
        self.vocab_dict = vocab_dict
        self.title = title
        self.song_rules = song_rules
        try:
            self.album_length = randint(self.config.min_album_length, self.config.max_album_length)
        except ValueError:
            bf.error_state('album_length', self.config)
        self.track_list = []
        self.log = []
        for x in range(self.album_length + 1):
            song_rule = choice(self.song_rules)
            song_title = bf.make_name(song_rule, self.vocab_dict, self.config, 'song')
            self.track_list.append(song_title)
            self.log.append((song_rule, song_title))

    def csv(self):
        """generates the representation of the object for csv output"""
        return f"{self.title},{','.join(self.track_list)},\n"

    def view(self):
        """generates the output string and passes it to __repr__ and __str__"""
        string = f"{self.title}\n\n"
        for index, item in enumerate(self.track_list):
            string += f"{str((index + 1)).zfill(2)} - {item}\n"
        string += "\n"
        return string

    def __repr__(self):
        return self.view()

    def __str__(self):
        return self.view()


class Configuration:
    """stores the config settings as a convenient object so that reading the config file can be minimised"""
    def __init__(self, config_seg):
        self.config_seg = config_seg
        try:
            self.retrieve_settings(config_seg)
        except ValueError:
            bf.error_state('bad_settings', config_seg)

    def retrieve_settings(self, config_seg):
        self.config = conf.ConfigParser()
        self.config.read(os.getcwd() + '\\Settings\\Config.ini')
        self.program_name = self.config[(config_seg)]['program_name']
        self.version = self.config[(config_seg)]['version']
        self.rules_path = self.config[(config_seg)]['rules_path']
        self.vocab_path = self.config[(config_seg)]['vocab_path']
        self.eleven_path = self.config[(config_seg)]['eleven_path']
        self.output_path = self.config[(config_seg)]['output_path']
        self.output_name = self.config[(config_seg)]['output_name']
        self.eleven_rarity = int(self.config[(config_seg)]['eleven_rarity'])
        self.upper_bound = int(self.config[(config_seg)]['upper_bound'])
        self.lower_bound = int(self.config[(config_seg)]['lower_bound'])
        self.max_discog_size = int(self.config[(config_seg)]['max_discog_size'])
        self.min_album_length = int(self.config[(config_seg)]['min_album_length'])
        self.max_album_length = int(self.config[(config_seg)]['max_album_length'])
        self.capitalise_first_letter = bool(self.config[(config_seg)]['capitalise_first_letter'])
        self.capitalise_lone_i = bool(self.config[(config_seg)]['capitalise_lone_i'])
        self.word_number_rarity = int(self.config[(config_seg)]['word_number_rarity'])
        self.start_apostrophe_year = int(self.config[(config_seg)]['start_apostrophe_year'])
        self.apostrophe_rarity = int(self.config[(config_seg)]['apostrophe_rarity'])
        self.bounds = [self.lower_bound, self.upper_bound]

    def store_seed(self, seed):
        """stores the seed in the config object"""
        self.seed = seed

    def store_arg_string(self, args):
        """stores the arg string in the config object"""
        self.raw_args = vars(args)
        self.arg_list = []
        for key, value in self.raw_args.items():
            self.arg_list.append(f"{key} : {value}")
        self.args_string = "\n".join(self.arg_list)

    def view(self):
        """generates the config output string and passes it to __repr__ and __str__"""
        string = f"Current configuration settings for {self.program_name} v.{self.version}.\n" \
                 f"Consult README.md for more details.\n\n" \
                 f"Reading from {self.config_seg}\n\n" \
                 f"rules_path: {self.rules_path}\n" \
                 f"vocab_path: {self.vocab_path}\n" \
                 f"eleven_path: {self.eleven_path}\n" \
                 f"output_path: {self.output_path}\n" \
                 f"output_name: {self.output_name}\n" \
                 f"eleven_rarity: {self.eleven_rarity}\n" \
                 f"upper_bound: {self.upper_bound}\n" \
                 f"lower_bound: {self.lower_bound}\n" \
                 f"max_discog_size: {self.max_discog_size}\n" \
                 f"min_album_length: {self.min_album_length}\n" \
                 f"max_album_length: {self.max_album_length}\n" \
                 f"capitalise_first_letter: {self.capitalise_first_letter}\n" \
                 f"capitalise_lone_i: {self.capitalise_lone_i}\n" \
                 f"word_number_rarity: {self.word_number_rarity}\n" \
                 f"start_apostrophe_year: {self.start_apostrophe_year}\n" \
                 f"apostrophe_rarity: {self.apostrophe_rarity}\n"
        return string

    def __repr__(self):
        return self.view()

    def __str__(self):
        return self.view()
