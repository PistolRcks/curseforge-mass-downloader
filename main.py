# Scrapes the Curse Forge website to download mods from a list--from CLI
import re
import os
import requests as rq
import json
import sys


# Load project IDs and version number
manifest = ""
# Make sure the manifest file was given
# See https://github.com/PistolRcks/curseforge-mass-downloader/wiki/Structuring-manifest.json for more info
try: assert sys.argv[1]
except:
    print("Manifest file not provided. Please provide a modlist in .json format.\nSee https://github.com/PistolRcks/curseforge-mass-downloader/wiki/Structuring-manifest.json for more info.")
    sys.exit()
# Make sure the manifest file exists and is a json file
try: assert os.path.isfile(sys.argv[1]) and not re.search(r"\.json$", sys.argv[1]) == None
except:
    print(f"Manifest file {sys.argv[1]} does not exist and/or is not in .json format. Please provide a modlist in .json format.\nSee https://github.com/PistolRcks/curseforge-mass-downloader/wiki/Structuring-manifest.json for more info.")
    sys.exit()
# Open the thing
with open(sys.argv[1], "r") as f:
    manifest = json.load(f)

PROJECT_IDS = [file["projectID"] for file in manifest["files"]] # Project IDs of the mods, as shown on the mod page
VERSION = manifest["minecraft"]["version"] # Name of the game version


# Download mods
for i, id in enumerate(PROJECT_IDS):
    ticker = f"[{i+1}/{len(PROJECT_IDS)}]" # For showing which mod we're on

    # Get mod name, so it looks nice
    data = json.loads(rq.get(f"https://curse.nikky.moe/api/addon/{id}").content) # Put the request's data into a Python-readable format
    modName = data["name"]

    # Get mod's latest version for this game version
    print(f"{ticker} Getting mod download link for mod {modName} (ID: {id})...")
    data = json.loads(rq.get(f"https://curse.nikky.moe/api/addon/{id}/files").content)
    # Get the latest mod version which supports the game version (which is last in the list)
    latestVersion = [candidate for candidate in data if VERSION in candidate["gameVersion"]][-1]
    print(f"{ticker} Found latest mod version for mod {modName} (ID: {id})!")

    # Download the mod
    if os.path.isfile("mods/" + latestVersion["fileName"]): # Don't redownload mods we may already have downloaded
        print(f"{ticker} Mod {modName} (ID: {id}) already downloaded! Skipping.")
    else:
        print(f"{ticker} Starting download of mod {modName} (ID: {id})...")
        download = rq.get(latestVersion["downloadUrl"])
        assert download.status_code == 200 # Make sure we're good
        with open("mods/" + latestVersion["fileName"], "wb") as f:
            f.write(download.content)
        print(f"{ticker} Finished downloading mod {modName} (ID: {id})!")

print(f"Finished downloading all {len(PROJECT_IDS)} mods!")
