# Scrapes the Curse Forge website to download mods from a list--from CLI
import re
import os
import requests as rq
import json

# TODO: Will use command line arguments (later)
PROJECT_IDS = ["235279", "227083", "248787", "228756"] # Project IDs of the mods, as shown on the mod page
VERSION = "1.12.2" # Name of the game version

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
