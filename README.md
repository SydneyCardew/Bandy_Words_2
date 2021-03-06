# BANDY WORDS 2.0

#### A program by Sydney Cardew

Bandy words is a CLI program for generating interesting, amusing (and
occasionally outrageous) names, album titles, song titles and genres for 
fictious bands, using a hand-crafted and curated set of rules and vocabulary, 
built in Python. It is a reconstruction of one of the first pieces of software
I ever wrote, reworked from the ground up with a much better understanding
of basic programming principles and technologies. 

With the default configuration options, the current version of Bandy Words
is capable of generating 1,573,404,366 unique strings.

---

#### Operation: 

Bandy Words accepts the following arguments:

```Bandy_words.py <type> <number> [--help] [--dictmaker] [--user] [--eleven]```
```[--textsave] [--csvsave] [--quiet] [--log] [--setseed <seed>]```
```[--combocounter] [--showconfig] [--setconfig "<setting>=<value"]``` 
```[--resetconfig] [--version]```

If no arguments are passed, Bandy Words will generate a single band name.

* `type` tells Bandy Words the type of output it is being asked to generate.
The allowable types are as follows (with examples):

    * `band`: generates band names.

    >Machineries of Evening, Joy of the Pagan Time, The Gang of Field, 
    >The Splendid Wheels, The Bards of Helsinki, Dagger for the Age of Exploration, 
    >Glass of the Vast Butterfly, The Rain Guitar, The Advancing Concrete, 
    >House Thirty Seven, Black Yellow Machinery, Land and the Soldiers, 
    >Curse the Astronauts, Cold Highway, The Winter Redemption, 
    >The Meadow Emperors, George and the Russian Wizards, 
    >The Millenium Witch, The Eaters of L.A., Harvesting Hills, Astronaut of Apes.
    
    * `album`: generates album titles    

    >Napoleon's Arousing, The Dreaded Dream, Grave of Smashing, 
    >Autumn Warsaw, The Expected Song, The East of Princesses, 
    >Apocalypse Force, Mars of Mechanics, 
    >Jessica's Shocking, The American High Law, 
    >The Hated Fire, Forest Things, Saturday Wizards, 
    >They Can Desist, Michael's Limb, River Tuesday, 
    >The Beautiful Small Blood, The Screaming Steel, 
    >The Lesbian Scar, Emmanuel's Theatre, Minds of the Yellow Fashion.
 
    * `song`: generates song titles 

    > Hunter of the Fog, A Scar Singing in Bangkok, 
    >The Eater of the Colour, Kissing the Mountains, She Isn't the Egg, 
    >Lucifer's Skulls, Three Quarters Storm, The Man is Sculpting, 
    >The Tidal Red Heat, Jumping South, Yellow Granite, 
    >She Has Lusted for the Priest, Lake Warlords, 
    >Elephant of the Rockets, Our Blues, She Had Been Mourned, 
    >The Night is Leaving, Numbering Teeth, Rider of Field, 
    >Fighting the Masters, Ghost Terrorists.
   
    * `genre`: generates musical genres    

    >Space Ghetto Pop, Freestyle Industrial, Surf Witch Raga, 
    >Thrash Rockabilly, Hop Metal, Rock Core, Modern Bubblegum Psychedelia, 
    >Trance Funk Core, Esoteric Metal Funk, Baroque Hop Rap, Witch Drone Swing, 
    >Constrained Trip Hop Metal, Silver Noise, Baroque Jangle Merengue Wave, 
    >Outsider Punk, Jazz Core, Mumble Retro Pop, Machine Rock, 
    >Progressive Drone Garage, Trance Country, Queer Country.

    * `fullalbum`: generates full albums

    >Nail of Roses
    >
    >01 - Calling the Proud Crow    
    >02 - Jessica's Tune    
    >03 - Bones of Barcelona   
    >04 - Arousing the Colours   
    >05 - The Machinery Division   
    >06 - Silver Set   
    >07 - Shocking Fields   
    >08 - Dying Cries   
    >09 - 57 Baby Lies   
    >10 - Generator in Their Whispers   
    >11 - The Redemption That Accepted Asteroids   
    >12 - Dying the Mind  
    >13 - The Crows   


    * `discog`: generates entire discographies

    >The Opulent Sun    
    >Genre: Third Wave Garage    
    >
    >2 albums    
    >
    >Vixen 12    
    >
    >01 - Angelic She Refined    
    >02 - The Ice Age of the Asteroids   
    >03 - The Creek Warriors    
    >
    >The Cries    
    >
    >01 - Wild Moon Voodoo    
    >02 - The Dreaded Grave    
    >03 - Like a Emerald Nation    
    >04 - The Joy That Feared Devils    
    >05 - Sasha, Empress of Miami   
    >06 - The Phantoms Truly Understanding    
    >07 - Rider of 54    
    >08 - Constrained Spiders    

* `number` tells Bandy Words how many examples of the `type` it should output.
The maximum number of examples Bandy Words can generate at any one time is
999,999.

* ```--help``` or `-h` accesses hints in the terminal

* ```--dictmaker``` or `-dm` runs `Dict_Maker.py` before running Bandy Words

* ```--user``` or `-u` tells Bandy Words to use the alternative user-defined
settings in the Config.ini file

* ```--eleven``` or `-e` puts Bandy Words into 'Eleven mode'. In this mode, the
program is 'turned up to 11' and ??mlauts are add??d rand??mly to a
c??rtain proport??on of vow??ls.

* ```--txtsave``` or `-ts` saves the output of Bandy Words to a txt file.

* ```--csvsave``` or `-cs` saves the output of Bandy words to a csv file.

* ```--quiet``` or `-q` prevents the output of Bandy Words being sent to the 
terminal.

* ```--log``` or `-l` causes Bandy Words to generate a log file, which records 
which rule was used to generate each item of output. This is intended as a 
development tool for refining dictionaries.

* ```--setseed <seed>``` or `-ss <seed>` allows the user to define a seed manually.
The seed must be an integer number between 1 and 999999. If no seed is set, 
Bandy Words will attempt to retrieve a random number based on atmospheric noise
from an online source*. If it is unable to do so, it will revert to a pseudorandom 
number generated from the system time by Python's inbuilt `random` module.

* ```--combocounter``` or ```-cc``` runs `Combo_Counter.py`, which outputs
the number of unique strings Bandy Words is capable of creating to the terminal.
This utility can also be run as a standalone script.

The following arguments will execute without running the rest of Bandy Words: 

* ```--showconfig``` or ```-sc``` will display the current configuration settings in the 
terminal.

* ```--setconfig "<setting=value>"``` or ```-set "<setting=value>"``` allows one ore more
of the user-defined settings to be set from the terminal. Settings must be in the
format `"setting=value"`, for example `"min_album_length = 3"`. You can set 
multiple settings by seperating these entries with commas. For example 
`"min_album_length=1,max_album_length=14"`.

* ```--resetconfig``` or ```-reset``` will reset the custom user settings to match those in the 
default.

* ```--version``` or `-v` displays the current version of Bandy Words in the terminal. 
 
\* https://www.random.org/integers/?num=1&min=1&max=999999&col=1&base=10&format=plain&rnd=new

---

#### Dictionary files:

Bandy Words uses two type of dictionary files, which can be found in plain
text form in the *..\Dictionaries\Rules Dictionaries* and *..\Dictionaries\Vocab Dictionaries*
folders. 

**Rules Dictionaries** contain the rules used for the generation of a particular
name or title, for example:

```NOUN and the ADJECTIVE COLLECTIVE```

The program will select rules from the approrpiate dictionary at random and replace the 
CAPITALISED words with random selections from the appropriate **Vocab Dictionaries** 
(i.e. `NOUN`, `ADJECTIVE`, `COLLECTIVE`):

```Heartbreak and the Fabulous Orphans```

It is very simple to modify the text files to add or delete rules and
vocabulary. You can even add new types of words, as long as you create
a new text file with a name that corresponds to that type. For example
you might add the rule:

```FOO for the BAR```

You would then need to create txt files called ```FOO.txt``` and ```BAR.txt```
and populate them with at least one rule. Note that capitalisation of file names is not 
actually necessary, though they must be correctly named. 

Each rule or vocabulary item must be on its own line. If you wish to increase 
the frequency with which a certain rule or vocabulary item appears, repeat it.

Bandy Words will by default capitalise the first letter of a name
or title in the output string, and will capitalise the letter 'i' on its own. 
This allows you to use rules like `a NOUN` and receive output such as `A Skull`,
without having to define a dictionary just for 'A'. These behaviours can be 
turned off in the config file (see below). 

##### Punctuation

Bandy Words will ignore common punctuation marks and other non-alphabetical
symbols when interpeting the rules, reinserting them back into the ouput 
string at their proper place. So this rule:

```FIRSTNAME, TITLE of PLACE```

Might become:

```Robin, Imperatrix of the Meadow```

The allowable punctuation marks are:

```,.!?:;#+/\()[]{}-&*=%??$@~|```

Using other non-alphabetical symbols in rule dictionaries may cause unexpected
behaviour. You can use any symbols you like within vocab dictionaries.

##### Compiling

In order for your changes to these dictionaries to be reflected in Bandy Words,
it is necessary to run the script `Dict_Maker.py`. This can be done seperately
or as an optional command line argument for Bandy Words. This will convert 
all the text dictionaries to the json format that Bandy Words
uses. `Dict_Maker.py` will ignore any line beginning with `###`: 
these can be used for commenting your dictionary files.

**NOTE**: `NUMBER` is a special rule; it is not associated with a dictionary,
but instead generates a random integer number. One third of these numbers
will be converted to a written out form, and any remaining integer numbers
between the numbers 50 and 99 have a chance to have `'` added to their front
(i.e. `Barbarians of '89`).

---

### Settings

The ```Config.ini``` file in the *Settings* folder contains a number of
settings relevant to the operation of Bandy Words. If you wish to tweak these 
settings it is strongly recommended that you modify the settings in the 
```[CUSTOM]``` section *only* and run Bandy Words in ```--user``` mode.

The settings are:

* `version` - the version of bandy words 
* `rules_path` - the path to the rules dictionary json 
* `vocab_path` - the path to the vocab dictionary json
* `eleven_path` - the path to the eleven mode json
* `output_path` - the path to the output directory
* `output_name` - the name to be used for output files
* `eleven_rarity`\* - this controls the rarity of umlauts in eleven mode. The
higher the number, the rarer umlauts become; it is essentially the denominator
of a ratio which has a numerator of one. For example, setting this to '4' will
cause 1/4 of vowels to be replaced, setting it to '6' will cause 1/6 of vowels
to be replaced, and so on. Setting this to '1' will cause
all vowels to be replaced with umlauts.
* `upper_bound`\* - The upper limit on the numbers generated by the `NUMBER` rule (see above).
* `lower_bound`\* - The lower limit on the numbers generated by the `NUMBER` rule
* `max_discog_size`\* - The maximum number of albums generated by the `discog` function
* `min_album_length`\* - The minimum length of the tracklist of albums generated
by the `discog` function.
* `max_album_length`\* - The maximum length of the tracklist of albums generated
by the `discog` function.
* `capitalise_first_letter`\*\* - Controls whether the first letter of the output
strings is automatically capitalised.
* `capitalise_lone_i`\*\* - Controls whether lone letter i's are automatically
capitalised.
* `word_number_rarity` \* - Controls the rate at which words are converted into
numbers. Operates in the same way as `eleven_rarity`.
* `start_apostrophe_year` \* - The lowest two digit number which can have an apostrophe
added to it to give it the appearance of a year.
* `apostrophe_rarity` \* - Controls the rate at which apostrophes are added to 
numbers. Operates in the same way as `eleven_rarity`.

**NOTE:** Settings marked with a \* must be integers. Settings marked with \*\* must
be booleans (`True` or `False`).

---

#### Version history:

##### 2.0.0    
* First functional version.
  
##### 2.1.0     
* Text saving.
* Full album generation.
* Refactoring and other feature improvements.   

##### 2.2.0    
* csv saving.
* full logging.
* input custom seeds.
* combination counter.
* improved randomness.
* better error communication .
* refactoring and commenting.
* extensive refinement and expansion of rules and vocab dictionaries.

##### 2.2.1
* bugfixes and improved commenting

##### 2.3.0
* reworked the name generator to fully support rules with natural punctuation.
* full logging now available for 'fullalbum' and 'discog' modes.
* logs now record settings and arguments.
* added new config settings to control the NUMBERS rule.
* added command line arguments to edit the settings.
* corrected a major bug when creating custom rule dictionaries.
* further refinement of dictionaries.
* added a default behaviour if Bandy Words is run without arguments.
* many minor code improvements and changes.

##### 2.3.1
* minor bugfix

---

#### Future development:

The creation of Bandy Words 2 has been conducted largely as a preliminary
exercise in order to develop the software into a web app.