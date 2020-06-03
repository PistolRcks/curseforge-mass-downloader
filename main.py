# Scrapes the Curse Forge website to download mods from a list--from CLI
import re
import sys
from selenium import webdriver
import requests as rq
from bs4 import BeautifulSoup as bs

# TODO: Will use command line arguments (later)
GAME = "minecraft" # Name of the game, as is shown in the address
CONTENT_TYPE = "mc-mods" # Name of the content, as is shown in the address
MODS = ["chisel"] # Name of the mod(s), as is shown in the address
VERSION = "1.12.2" # Name of the game version

downloadIDs = []
modFilenames = []
versionID = ""

# Load up Firefox using Selenium
wd = webdriver.Firefox()

# Scrape for download URLs
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
wd.quit()

#for i, link in enumerate(downloadIDs):
#    ticker = f"[{i+1}/{len(downloadIDs)}]" # For showing which mod we're on (again)
#
#    print(f"{ticker} Starting download of mod {MODS[i]}...")
#    wd.get(link)
#    print(f"{ticker} Finished downloading mod {MODS[i]}!")
