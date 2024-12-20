
Just a simple Python script to manage Wine prefixes and programs.

# Installation
1. Clone the repository to a folder (e.g ~/Documents/). Take note of the directory/folder `main.py` is in.
2. Edit the `config.json` file.
	1. `"WINE_BIN_PATH"`: Place the directory where your `wine` binary is (e.g `/opt/homebrew/bin`). You can install wine using `brew` or you can get them from [Gcenx](https://github.com/Gcenx/macOS_Wine_builds)
	2. `WINE_D3D_BIN_PATH`: Place the directory where your Game Porting Toolkit `wine64` binary is. You can either compile GPTK yourself and provide the `/bin` path (e.g `$(brew --prefix game-porting-toolkit)/bin/`) or just get prebuilt binaries from [Gcenx](https://github.com/Gcenx/game-porting-toolkit/)and provide the path (e.g `~/Downloads/Game Porting Toolkit.app/Contents/Resources/wine/bin`)
	3. `PREFIX_PATH`: Place the directory where you will want to store your prefixes (e.g `~/Documents/Wine Prefixes`)
	4. `ROOT_PATH`: Place the root file (the directory `main.py` is in)
3. You should also clear the `settings.json` file. This file contains the settings for the programs and prefixes that the script will manage. The script will automatically populate the file when you do stuff. If you have any existing prefixes you can write them into `config.json` as is shown.
## EXTRA NOTE
---
Whenever you copy your paths, they have to be absolute (e.g /Users/username/... not ~/...)
 The repository contains a copy of [DXVK for MacOS](https://github.com/Gcenx/DXVK-macOS). However you can place your own DLLs from the link provided. Just make sure to replace the x32 and x64 directories in the `dxvk` directory completely. DO NOT RENAME THE FOLDER.
 While not necessary you can place a pre built GPTK binary from Gcenx into the directory of `main.py`.

# Usage
Execute `main.py`. 

## Managing Prefixes
If you have existing prefixes, you can provide their paths in `settings.json` according to the reference provided:
```
"prefixes" {
	"Age of Empires II": "aoe2"
}
```
The script will display the prefix name as "Age of Empires II". The key's value is the name of the directory relative to the PREFIX_ROOT provided in `config.json`. In this case, the prefix is located at `~/Documents/Wine Prefixes/aoe2` if you provided `~/Documents/Wine Prefixes/` as your PREFIX_ROOT.

To create new prefixes, launch `main.py ` and select `2. Manage Prefixes`, then `1. Create a prefix`. Enter the name of your prefix and the script will create your prefix. The script will name the folder the same name as provided. The script will launch Wine Configuration. You can change any settings now, but you can always do it later from the Manage Prefixes menu. You don't have to do DLL overrides for `d3d10core.dll` or `d3d11.dll` because the script automatically does this when it executes the shell command (via. `WINEDLLOVERRIDES`).

You can also delete prefixes through `2. Manage Prefixes` > `Delete Prefixes`. The script will list all prefixes listed in `settings.json` (because these are the prefixes recognised by the script) and will ask you to type in the name of the prefix. You must do this exactly (case sensitive and spaces included) or the script won't be able to delete that prefix. 

## Managing Shortcuts
You can add shortcuts to your programs through `3. Manage shortcuts` > `1. Create a shortcut`.  The script will ask you to provide a name for the shortcut, the prefix to use and the absolute path to the .EXE file and the graphics backend to use (DXVK or D3DMetal, type anything other than these to not use either). The script will write these settings to `settings.json`. 

You can likewise delete shortcuts through `3. Manage shortcuts` > `2. Delete a shortcut`. The script will list all shortcuts and ask you to type the name of the shortcut. The script will not delete the .EXE and will only delete it from `settings.json` so that it is not recognised by the script.

You can also manage the graphics backend used through the menus. 

## Running Programs
You can run a program by selecting `1. Run a program`. The script will list all the shortcuts and you must type the name exactly. You can also pass any arguments for the .EXE. 

# Why?
I am aware of existing Wine managers for MacOS like [Whisky](https://github.com/Whisky-App/Whisky) and [CrossOver](https://www.codeweavers.com/crossover). These programs are much better and more intuitive than what I wrote and it is recommended you use them rather than my script. I was just tinkering with Wine because I couldn't get Age of Empires II HD to work on either and was getting tired of having to manually write out each command to run my games so I decided to write this program to make it easier. There are many more things needed to be implemented to reach parity with Whisky or CrossOver, and perhaps in the future it could be a viable alternative but as of now it's just a script for convenience. 

If you look at the code you will very quickly realise that my programming knowledge is very primitive and you're right. I spent more time on StackOverflow than in VS Code lmao so obviously it's not the fastest or more optimised. It's also not the prettiest thing to use. 

If you're an experienced developer you always welcome to contribute to the code.
