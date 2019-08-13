# Spencer Aeschliman. August 2019
# My first spotipy tinkering. A simple reading of a user's top artists, plus some albut art

import spotipy
import spotipy.util as util
import sys
import os
import json
import inquirer
import urllib.request
from PIL import Image
import math
import numpy as np


# authorization for scope of the program
username = sys.argv[1] # enter the username after the script name in the terminal
scope = 'user-top-read' # we can get the user's top artists + the info that goes with that
try:
	token = util.prompt_for_user_token(username,scope)
except:
	os.remove(f".cache-{username}")
	token = util.prompt_for_user_token(username,scope)

# create spotify object
sp = spotipy.Spotify(auth=token)

# generate list of the user's top x artists
questions = [
  		inquirer.List('size',
                	message="How many artists would you like?",
                	choices=['4', '9', '16','25'],
           	 ),
	]
lim = inquirer.prompt(questions)


top_results = sp.current_user_top_artists(limit=lim['size'])

artwork_list =[]
print("Your top ", lim, " artists are: ")

# parse the json file + create our list of artists
for artist in top_results["items"]:
	print(artist["name"])
	artwork_list.append(artist["images"][0]["url"]) # get the url for the top image of the artist

# download artist images
n = 1
for pic in artwork_list:
	urllib.request.urlretrieve(pic,"number_%d.jpg" % n)
	n += 1

# keep track of image names
dim = int(math.sqrt(len(artwork_list)))
names = []
s = 1
for i in range(len(artwork_list)):
	names.append("number_{}.jpg".format(s))
	s += 1

# create collage parameters
mode = 'RGB'
size = (660,660)
color = (255,255,255)
blank = Image.new(mode,size,color=0)
ind_size = int(660/dim)

# make the collage
x_offset = 0
y_offset = 0

for img in names:
	raw = Image.open(img)
	correct_size = raw.resize((ind_size,ind_size))
	blank.paste(correct_size, (x_offset, y_offset, x_offset + ind_size, y_offset + ind_size))
	if x_offset < 660:
		x_offset += ind_size
	else:
		x_offset = 0
		y_offset += ind_size

blank.show()
blank.save("Top_Artists.jpg")
