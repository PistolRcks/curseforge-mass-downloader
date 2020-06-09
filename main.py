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
# Scrapes the Curse Forge website to download mods from a list--from CLI
import re
import sys
import os
from selenium import webdriver
import requests as rq
from bs4 import BeautifulSoup as bs

# TODO: Will use command line arguments (later)
GAME = "minecraft" # Name of the game, as is shown in the address
CONTENT_TYPE = "mc-mods" # Name of the content, as is shown in the address
MODS = ["chisel", "baubles", "appleskin", "iron-chests"] # Name of the mod(s), as is shown in the address
VERSION = "1.12.2" # Name of the game version

downloadIDs = []
modFilenames = []
versionID = ""

# Load up Firefox using Selenium
wd = webdriver.Firefox()

# Scrape for download IDs and filenames using Selenium
for i, mod in enumerate(MODS):
    ticker = f"[{i+1}/{len(MODS)}]" # For showing which mod we're on

    baseURL = ""
    if versionID != "": baseURL = "https://curseforge.com/" + GAME + "/" + CONTENT_TYPE + "/" + mod + "/files/all?filter-game-version=" + versionID
    else: baseURL = "https://curseforge.com/" + GAME + "/" + CONTENT_TYPE + "/" + mod + "/files/all"
    print(f"{ticker} Loading page for mod name {mod}...")
    wd.get(baseURL)
    soup = bs(wd.page_source, 'html.parser')
    print(f"{ticker} Found mod {soup.find('h2', class_='font-bold text-lg break-all').string}")

    # Find the version selector dropdown and get the version ID (if it hasn't already been found)
    if versionID == "":
        versionSelector = soup.find("select")
        versionID = re.sub(r":", r"%3A", versionSelector.find("option", text = re.compile(VERSION))["value"]) # Get the ID (and fix it up so it works)
        print(f"Found version ID {versionID}, reloading page")
        wd.get(baseURL + "?filter-game-version=" + versionID)
        soup = bs(wd.page_source, 'html.parser')

    # Find download ID
    id = re.findall(r"(?:[^/](?!/))+$", soup.find("a", class_="button button--hollow mr-2 button--icon-only")["href"])[0] # Gets the id from the end of the address
    print(f"{ticker} Found download ID {str(id)}")
    downloadIDs.append(id)

    #Find filename
    wd.get("https://curseforge.com/" + GAME + "/" + CONTENT_TYPE + "/" + mod + "/files/" + id)
    soup = bs(wd.page_source, 'html.parser')
    filenameDiv = soup.find("div", class_="flex flex-row md:flex-col mr-2 justify-between md:flex-col md:w-full md:justify-between")
    filename = filenameDiv.find_all("span", class_="text-sm")[1].string
    print(f"{ticker} Found filename {filename}")
    modFilenames.append(filename)

# We're going to need requests after this (because downloading in Selenium isn't supported)
print("Quitting Selenium...")
wd.quit()

# Put mods into folder called `mods`
if not os.path.isdir("mods"):
    os.mkdir("mods")

# Download files using requests
for i, id in enumerate(downloadIDs):
    ticker = f"[{i+1}/{len(downloadIDs)}]" # For showing which mod we're on (again)
    if os.path.isfile("mods/" + modFilenames[i]): # Don't redownload mods we may already have downloaded
        print(f"{ticker} Mod {MODS[i]} already downloaded! Skipping.")
    else:
        print(f"{ticker} Starting download of mod {MODS[i]}...")
        link = "https://edge.forgecdn.net/files/" + re.sub(r"(.{4})", r"\1/", id) + "/" + modFilenames[i] # Add a slash after the first four numbers in the id
        download = rq.get(link)
        assert download.status_code == 200 # Make sure we're good
        with open("mods/" + modFilenames[i], "wb") as f:
            f.write(download.content)
        print(f"{ticker} Finished downloading mod {MODS[i]}!")

print("Finished downloading all mods!")
