# kbview
kbview is a small python script to show your keyboard presses in a customizable window. All the config is stored in json format.

![](https://raw.githubusercontent.com/rokie95/kbview/master/docs/config.json.png)

```
usage: kbview.py [-h] [--config CONFIG] [-d]

Shows keys and wether they are pressed in a customizable window

optional arguments:
  -h, --help       show this help message and exit
  --config CONFIG  config file path. (default='config.json')
  -d, --debug      show debug prints. (default=False)
```

## Configuration
Configs can be any file but defaults to ```config.json```, if you want to use a different file use the ```--config``` option. You can view the config.json for the image about [here](https://raw.githubusercontent.com/rokie95/kbview/master/config.json)

## Writing a configuration file
Configs have 2 main parts, the global configs and key specific configs. If you do not have all of the ```(REQUIRED)``` tagged config options there will be an error. If a config option is tagged ```(EITHER)``` it is still required by can be put in either the global or key config, if both are available then the key specific option is used. ```(OPTIONAL)``` is optional.


#### Global Configs:
 - ```windowwidth``` - the width of the window ```(REQUIRED)```
 - ```windowheight``` - the height of the window ```(REQUIRED)```
 - ```backgroundcolor``` - the background color of the window in hex ```(REQUIRED)```
 - ```keycolor``` - the color of the key in hex ```(EITHER)```
 - ```keycoloractive``` - the color of the key when it is pressed in hex ```(EITHER)```
 - ```labelfontsize``` - the font size of the label ```(EITHER)```
 - ```keywidth``` - the width of the key drawing ```(EITHER)```
 - ```keyheight``` - the height of the key drawing ```(EITHER)```
 - ```xscroll``` - a x value that is added to all keys, defaults to 0 ```(OPTIONAL)```
 - ```yscroll``` - a y value that is added to all keys, defaults to 0 ```(OPTIONAL)```

#### Key Configs:
Key configs are stored in a list and in the list are json objects, the below key configs apply to each json object. If this sounds confusing look at the default config.json [here](https://raw.githubusercontent.com/rokie95/kbview/master/config.json)
 - ```key``` - the key that makes it switch to the active color, can be multiple keys seperated by commas ```(REQUIRED)```
 - ```x``` - the x position of the key graphic ```(REQUIRED)```
 - ```y``` - the y position of the key graphic ```(REQUIRED)```
 - ```label``` - the text that shows on the key in the window, if not provided it will use ```key``` ```(OPTIONAL)```
