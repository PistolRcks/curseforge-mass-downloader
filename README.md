# CurseForge Mass Downloader
*A Python script to download Minecraft mods from the CurseForge website using the [CurseProxy API](https://github.com/NikkyAI/CurseProxy)*

# Nota Bene
***This project now no longer works due to an update in the CurseForge API [and, therefore, the CurseProxy API](https://github.com/NikkyAI/CurseProxy/issues/9).***

***PLEASE DO NOT USE THIS FOR ACTUALLY DOWNLOADING MODPACKS. PLEASE USE THE EXCELLENT [MultiMC](https://multimc.org/) IF YOU LEGITIMATELY DO NOT WANT TO USE THE CURSEFORGE LAUNCHER.***

This was more of a personal project for me, and I made this before I realized MultiMC exists.

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
