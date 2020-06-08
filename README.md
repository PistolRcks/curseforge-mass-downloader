# CurseForge Mass Downloader
*A Python script to download Minecraft mods from the CurseForge website using the [CurseProxy API](https://github.com/NikkyAI/CurseProxy)*

## Dependencies
* Python 3.6 or above
* [Requests](https://pypi.org/project/requests/)

## Usage
```
python main.py [modlist-manifest]
```
* `modlist-manifest` - "manifest.json" file found in a CurseForge modpack .zip file. You can make your own by following [the file's  (ongoing) documentation.](https://github.com/PistolRcks/curseforge-mass-downloader/wiki/Structuring-manifest.json)

## TODO
* Dependency resolution
* Modloaders other than forge
* Auto-installation
