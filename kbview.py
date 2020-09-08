
import argparse
import arcade
import json
from pynput import keyboard

# command line options
parser = argparse.ArgumentParser(description="Shows keys and if they are pressed in a customizable window")
parser.add_argument("--config", type=str, help="config file path. (default='config.json')", default="config.json")
parser.add_argument("-d", "--debug", help="show debug prints. (default=False)", action='store_true', default=False)
args = parser.parse_args()

keydict = {} # dict of pressed keys in format, {"$KEY": True}
config = {} # user config file, not loaded until later
possiblekeys = [] # keys that have been defined in config
allLowercase = True # if all keys should be read case sensitive (EXPERIMENTAL, BREAKS A LOT)
debug = args.debug

# loads the config file
with open(args.config, "r") as file:
	config = json.loads(file.read())
	print("config:")
	print(config)

# get all possible keys to be pressed
for keyconfig in config["keys"]:
	keylist = keyconfig["key"].split(",")
	for keystr in keylist:
		if not "Key." in keystr and allLowercase:
			keystr = keystr.lower()
		possiblekeys.append(keystr)
print("possible keys:")
print(possiblekeys)

# populate keydict with possible keys
for posskey in possiblekeys:
	keydict[posskey] = False

# updates the keydict with every keypress
def on_press(key):
	key = str(key).replace("'", "")
	if not "Key." in key and allLowercase:
		key = key.lower()
	if key in possiblekeys:
		keydict[key] = True
		if debug:
			print(keydict)

def on_release(key):
	key = str(key).replace("'", "")
	if not "Key." in key and allLowercase:
		key = key.lower()
	if key in possiblekeys:
		keydict[key] = False
		if debug:
			print(keydict)

# adds key listener
listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
listener.start()

class KeyboardView(arcade.Window):

	keyconfigs = config["keys"]

	def __init__(self):
		super().__init__(config["windowwidth"], config["windowheight"], "kbview")
		arcade.set_background_color(self.hextorgb(config["backgroundcolor"]))

	def setup(self):
		pass

	def on_draw(self):
		arcade.start_render()

		try:
			# loops through every key in list
			for keyconfig in self.keyconfigs:
				fillcolor = ()
				textcolor = ()
				labeltext = ""
				labelfs = 0
				keywidth = 0
				keyheight = 0
				xscroll = 0
				yscroll = 0
				
				# draw key unactive backplate
				if "keycolor" in keyconfig:
					fillcolor = self.hextorgb(keyconfig["keycolor"])
				else:
					fillcolor = self.hextorgb(config["keycolor"])

				# draw active key backplate if any possible key is pressed
				posskeys = keyconfig["key"].split(",")
				for posskey in posskeys:
					if posskey in keydict and keydict[posskey] == True:
						if "keycoloractive" in keyconfig:
							fillcolor = self.hextorgb(keyconfig["keycoloractive"])
						else:
							fillcolor = self.hextorgb(config["keycoloractive"])

				# get label of key
				if "label" in keyconfig:
					labeltext = keyconfig["label"]
				else:
					labeltext = keyconfig["key"]

				# label color of key
				if "labelcolor" in keyconfig:
					textcolor = self.hextorgb(keyconfig["labelcolor"])
				else:
					textcolor = self.hextorgb(config["labelcolor"])

				# label font size of key
				if "labelfontsize" in keyconfig:
					labelfs = keyconfig["labelfontsize"]
				else:
					labelfs = config["labelfontsize"]

				# get key width
				if "width" in keyconfig:
					keywidth = keyconfig["width"]
				else:
					keywidth = config["keywidth"]

				# get key height
				if "height" in keyconfig:
					keyheight = keyconfig["height"]
				else:
					keyheight = config["keyheight"]

				# get scroll from config if it exists
				if "xscroll" in config:
					xscroll = config["xscroll"]
				if "yscroll" in config:
					yscroll = config["yscroll"]

				# draw the key background
				arcade.draw_rectangle_filled(
					keyconfig["x"] + (keywidth / 2) + xscroll,
					keyconfig["y"] + (keyheight / 2) + yscroll,
					keywidth,
					keyheight,
					fillcolor)
				
				# draw the key text
				arcade.draw_text(
					labeltext,
					keyconfig["x"] + xscroll,
					keyconfig["y"] + yscroll,
					textcolor,
					labelfs,
					keywidth,
					"center"
				)
		except KeyError:
			print("CONFIG MISSING REQUIRED PARAMETER")
		
		arcade.finish_render()

	# convert hex codes to rgb for use with arcade
	def hextorgb(self, hex):
		hex = hex.replace("#", "")
		return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))

# run arcade window
window = KeyboardView()
window.setup()
arcade.run()