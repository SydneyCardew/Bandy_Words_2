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
        self.discog_size = randint(1, self.config.max_discog_size)
        self.band_name = bf.make_name(choice(self.band_rules),
                                      self.vocab_dict, self.config.bounds, 'band')
        self.band_genre = bf.make_name(choice(self.genre_rules),
                                       self.vocab_dict, self.config.bounds, 'genre')
        self.album_list = []
        for x in range(self.discog_size + 1):
            self.title = bf.make_name(choice(self.album_rules),
                                      self.vocab_dict, self.config.bounds, 'album')
            self.album_list.append(Album(self.title, self.song_rules,
                                         self.vocab_dict, self.config))

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
                 f"{self.discog_size + 1} " \
                 f"{'albums' if self.discog_size > 1 else 'album'}\n\n"
        for album in self.album_list:
            string += str(album)
        return string

    def __repr__(self):
        return self.view()

    def __str__(self):
        return self.view()


class Album:
    """The Album class stores"""
    def __init__(self, title, song_rules, vocab_dict, config):
        self.config = config
        self.vocab_dict = vocab_dict
        self.title = title
        self.song_rules = song_rules
        self.album_length = randint(1, self.config.max_album_length)
        self.track_list = []
        for x in range(self.album_length + 1):
            self.track_list.append(bf.make_name(choice(self.song_rules),
                                                self.vocab_dict, self.config.bounds, 'album'))

    def csv(self):
        return f"{self.title},{','.join(self.track_list)},\n"

    def view(self):
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
        self.config = conf.ConfigParser()
        self.config.read(os.getcwd() + '\\Settings\\Config.ini')
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
        self.max_album_length = int(self.config[(config_seg)]['max_album_length'])
        self.bounds = [self.lower_bound, self.upper_bound]

    def store_seed(self, seed):
        self.seed = seed
