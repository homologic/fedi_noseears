# Fediverse Nose Ears bot

Posts the [Nose Ears](https://wuzzy.neocities.org/) comics to the
fediverse. It supports comic titles, images and alt texts. 

## Configuration

To configure this bot, customize the first lines in the `noseears.py`
script to your needs, such as by setting the `instance` varible and
the `datadir` and `credfile` variables to indicate the position where
the bot should store its data and the credentials file
respectively. The credentials file can be generated using the
`mastodon.log_in` method.

## Usage

When supplied with no arguments, `noseears.py` tries to fetch the
latest nose ears comic. When supplied with a number as an argument, it
tries to fetch the comic with said number, and if "random" is passed
as an argument, it tries to fetch a random comic.

## Copyright

Copyright © 2022 Antonia <antonia@antonia.is>, Licensed under GPL
Version 3 or later.
