"""
The MIT License (MIT)

Copyright (c) 2020 PistolRcks

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
# Downloads mods from a CurseForge modpack's manifest.json file and puts them in a folder (for now)
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

FILE_IDS = [file["fileID"] for file in manifest["files"]]
PROJECT_IDS = [file["projectID"] for file in manifest["files"]] # Project IDs of the mods, as shown on the mod page
VERSION = manifest["minecraft"]["version"] # Name of the game version

# Create the mods folder if we don't already have it
if not os.path.isdir("mods"):
    os.mkdir("mods")


# TODO: Allow for other modloaders
# Download Forge installer
# Get the first primary Forge version, and extract the version number
FORGE_VERSION = re.sub(r"forge-", "", [version["id"] for version in manifest["minecraft"]["modLoaders"] if version["primary"]][0])
print(f"Getting Forge version {FORGE_VERSION}...")
modloader = rq.get(f"https://files.minecraftforge.net/maven/net/minecraftforge/forge/{VERSION}-{FORGE_VERSION}/forge-{VERSION}-{FORGE_VERSION}-installer.jar")
with open(f"forge-{VERSION}-{FORGE_VERSION}-installer.jar", "wb") as f:
    f.write(modloader.content)
print(f"Forge version {FORGE_VERSION} downloaded!")

print("Starting download of mods...")
# Download mods (should be the same length as the file ids
for i, id in enumerate(PROJECT_IDS):
    ticker = f"[{i+1}/{len(PROJECT_IDS)}]" # For showing which mod we're on

    # Get mod name, so it looks nice
    data = json.loads(rq.get(f"https://curse.nikky.moe/api/addon/{id}").content) # Put the request's data into a Python-readable format
    modName = data["name"]

    # Get mod's latest version for this game version
    print(f"{ticker} Getting mod download link for mod {modName} (ID: {id})...")
    data = json.loads(rq.get(f"https://curse.nikky.moe/api/addon/{id}/files").content)
    # Get the correct version matching the file ID for this mod
    correctVersion = {}
    try:
        correctVersion = [candidate for candidate in data if FILE_IDS[i] == candidate["id"]][0]
        print(f"{ticker} Found correct mod version (File ID: {FILE_IDS[i]} for mod {modName} (ID: {id})!")
    except:
        print(f"{ticker} Couldn't find a matching file ID ({FILE_IDS[i]}) for mod {modName} (ID: {id}). Downloading latest version for the current forge version...")
        correctVersion = [candidate for candidate in data if VERSION == candidate["gameVersion"][0]]
    
    
    
    # Download the mod
    try:
        if os.path.isfile("mods/" + correctVersion["fileName"]): # Don't redownload mods we may already have downloaded
            print(f"{ticker} Mod {modName} (ID: {id}) already downloaded! Skipping.")
        else:
            print(f"{ticker} Starting download of mod {modName} (ID: {id})...")
            download = rq.get(correctVersion["downloadUrl"])
            assert download.status_code == 200 # Make sure we're good
            with open("mods/" + correctVersion["fileName"], "wb") as f:
                f.write(download.content)
            print(f"{ticker} Finished downloading mod {modName} (ID: {id})!")
    except: # The fileID isn't available
        print(f"{ticker} [ERROR] Couldn't download mod {modName} (ID: {id})! The mod's fileID contained within the manifest does not exist, and there exists no mod download compatible with your Minecraft version. Please contact the modpack maintainer for more info.\nQuitting.")
        sys.exit()

print(f"Finished downloading all {len(PROJECT_IDS)} mods!")
