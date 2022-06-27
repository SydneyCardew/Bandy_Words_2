#BANDY WORDS 2.0

####A program by Sydney Cardew

Bandy words is a CLI program for generating outrageous names, 
album titles, song titles and genres for fictious bands, using
a hand-crafted and curated set of rules and vocabulary, built in
Python. It is a reconstruction of one of the first pieces of software
I ever wrote, reworked from the ground up with a much better understanding
of basic programming principles and technologies. 

---

####Operation: 

Bandy Words requires at least two arguments:

```Bandy_words.py <type> <number> [--user] [--eleven] [--textsave]```

`type` tells Bandy Words the type of output it is being asked to generate.
The allowable types are as follows (with examples):

* `band`: generates band names.

>Machineries of Evening, Joy of the Pagan Time, The Gang of Field, 
>The Splendid Wheels, The Bards of Helsinki, Dagger for the Age of Exploration, 
>Glass of the Vast Butterfly, The Rain Guitar, The Advancing Concrete, 
>House Thirty Seven, Black Yellow Machinery, Land and the Soldiers, 
>Curse the Astronauts, Cold Highway, The Winter Redemption, 
>Meadow Emperors, George and the Russian Wizards, 
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

>Kissing Helsinki   
Genre: Acoustic Future Drone Metal
>
>2 albums
>
>Rivers of Emo
>
>01 - The Theatre of Eagles  
>02 - Machine Things 
>03 - The Erotic Men   
>04 - Little Soldiers
>
>Earth and the Redemption
>
>01 - Body of the Revolution   
>02 - The Planet Kisses   
>03 - The Winter Dirge   
>04 - Monkeys Mourning   
>05 - Fabulous Mercy for Roads  
>06 - A Underground Hammering in Rome   
>07 - A Dismal Madrigal  
>08 - Ruby Stonehenge  

`number` tells Bandy Words how many examples of the `type` it should output.

```--help``` or `-h` accesses hints in the terminal

```--dictmaker``` or `-dm` runs `Dict_Maker.py` before running Bandy Words

```--user``` or `-u` tells Bandy Words to use the alternative user-defined
settings in the Config.ini file

```--eleven``` or `-e` puts Bandy Words into 'Eleven mode'. In this mode, the
program is 'turned up to 11' and ümlauts are addëd randömly to a
cërtain proportïon of vowëls.

```--textsave``` or `-ts` saves the output of Bandy Words to a text file.

```--quiet``` or `-q` prevents the output of Bandy Words being sent to the 
terminal.

```--version``` or `-v` displays the current version of Bandy Words 
 
---

####Dictionary files:

Bandy Words uses two type of dictionary files, which can be found in plain
text form in the *..\Dictionaries\Rules Dictionaries* and *..\Dictionaries\Vocab Dictionaries*
folders. 

**Rules Dictionaries** contain the rules used for the generation of a particular
name or title, for example:

```NOUN and the ADJECTIVE COLLECTIVE```

The program will then replace the CAPITALISED words with random selections
from the appropriate **Vocab Dictionaries** (ie `NOUN`, `ADJECTIVE`, 
`COLLECTIVE`):

```Heartbreak and the Fabulous Orphans```

It is very simple to modify these text files to add or delete rules and
vocabulary. You can even add new types of words, as long as you create
a new text file with a name that corresponds to that type. For example
you might add the rule:

```FOO for the BAR```

You would then need to create txt files called ```FOO.txt``` and ```BAR.txt```
and populate them with at least one rule. Note that capitalisation of file names is not actually necessary, though
they must be correctly named. Each rule or vocabulary item must be on its own line.

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

###Settings

The ```Config.ini``` file in the *Settings* folder contains a number of
settings relevant to the operation of Bandy Words. If you wish to tweak these 
settings it is strongly recommended that you modify the settings in the 
```[CUSTOM]``` section and run Bandy Words in ```--user``` mode.

The settings are:

* `version` - the version of bandy words 
* `rules_path` - the path to the rules dictionary json 
* `vocab_path` - the path to the vocab dictionary json
* `eleven_path` - the path to the eleven mode json
* `eleven_rarity`\* - this controls the rarity of umlauts in eleven mode. The
higher the number, the rarer umlauts become; it is essentially the denominator
of a ratio which has a numerator of one. For example, setting this to '4' will
cause 1/4 of vowels to be replaced, setting it to '6' will cause 1/6 of vowels
to be replaced, and so on. Setting this to '1' will cause
all vowels to be replaced with umlauts.
* `upper_bound`\* - The upper limit on the numbers generated by the `NUMBER` rule (see above).
* `lower_bound`\* - The lower limit on the numbers generated by the `NUMBER` rule
* `max_discog_size`\* - The maximum number of albums generated by the `discog` function
* `max_album_length`\* - The maximum length of the tracklist of albums generated
by the `discog` function.

**NOTE:** Settings marked with a \* must be integers.

---

####Version history:

2.0.0: First functional version   
2.1.0: Added text saving, full album generation and other feature improvements.

---

####Future development:

Planned additional features include piping, output to csv files,
options to use a non pseudo-random seed source, full logging, an option to run
Dict_Maker.py as part of normal Bandy Words operation, and eventually
packaging Bandy Words into a web app form, as well as properly packaging it
to run without a Python installation.