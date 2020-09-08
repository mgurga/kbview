
import argparse
import arcade
import json
from pynput import keyboard

# command line options
parser = argparse.ArgumentParser(description="Shows keys and wether they are pressed in a customizable window")
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

		# loops through every key in list
		for keyconfig in self.keyconfigs:
			fillcolor = ()
			textcolor = ()
			labeltext = ""
			labelfs = 0
			
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

			# draw the key background
			arcade.draw_rectangle_filled(
				keyconfig["x"] + (keyconfig["width"] / 2) + config["xscroll"],
				keyconfig["y"] + (keyconfig["height"] / 2) + config["yscroll"],
				keyconfig["width"],
				keyconfig["height"],
				fillcolor)
			
			# draw the key text
			arcade.draw_text(
				labeltext,
				keyconfig["x"] + config["xscroll"],
				keyconfig["y"] + config["yscroll"],
				textcolor,
				labelfs,
				keyconfig["width"],
				"center"
			)
		
		arcade.finish_render()

	# convert hex codes to rgb for use with arcade
	def hextorgb(self, hex):
		hex = hex.replace("#", "")
		return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))

# run arcade window
window = KeyboardView()
window.setup()
arcade.run()