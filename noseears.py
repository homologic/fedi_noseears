#!/usr/bin/python3

# Copyright (c) 2022 Antonia <antonia@antonia.is>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>


# posts the current nose ears comic to the fediverse




from urllib import request
import sys
from bs4 import BeautifulSoup
import os
from mastodon import Mastodon
import re
import random


instance = "https://botsin.space"
baseurl = "https://wuzzy.neocities.org"
datadir = "data"
credfile= "cred"
cachedir = os.path.join(datadir, "cache")
seendir = os.path.join(datadir, "seen")


if len(sys.argv) > 1 :
    n = sys.argv[1]
    if sys.argv[1] == "random" :
        # try posting a random comic
        l = max([int(i) for i in os.listdir(seendir)])
        n = str(random.randint(1, l))
    page = request.urlopen(baseurl+"/comic/"+n)
else:
    page = request.urlopen(baseurl)
    
soup = BeautifulSoup(page, features="lxml")


## find link to full-size comic

img = None
alt = ""
title = soup.h1.text
for link in soup.find_all("a") :
    href = link["href"]
    if href.startswith("/comics/") and href.endswith(".png") : 
        img = href
        # extract alt text
        alt = link.img["alt"]
        break

if not img :
    print("No image found!")
    sys.exit(1)

number = re.sub("[^0-9]", "", img) # number of comic
permalink = baseurl + "/comic/" + number
## try to fetch comic from url
      
if not os.path.exists(cachedir) :
    os.makedirs(cachedir)
if not os.path.exists(seendir) :
    os.makedirs(seendir)

fname = os.path.join(cachedir,img.split("/")[-1])
seen = os.path.join(seendir, number)
if os.path.exists(seen) :
    sys.exit(0)

# download comic

request.urlretrieve(baseurl+img, fname)

mastodon = Mastodon(
    access_token=credfile,
    api_base_url=instance
)
md = mastodon.media_post(fname, "image/png", description=alt)

mastodon.status_post(title + "\n" + permalink, media_ids=md)

f = open(seen, "w")
f.write("")
f.close()
os.remove(fname)
