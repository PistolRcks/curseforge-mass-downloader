# Scrapes the Curse Forge website to download mods from a list--from CLI
import sys
import re
from selenium import webdriver
from bs4 import BeautifulSoup as bs

# TODO: Will use command line arguments (later)
GAME = "minecraft" # Name of the game, as is shown in the address
CONTENT_TYPE = "mc-mods" # Name of the content, as is shown in the address
MODS = ["chisel"] # Name of the mod(s), as is shown in the address
VERSION = "1.12.2" # Name of the game version

downloadURLs = []
versionID = ""

# Load up Firefox using Selenium
global wd
wd = webdriver.Firefox()

# Scrape for download URLs
for mod in MODS:
    baseURL = ""
    if versionID != "": baseURL = "https://curseforge.com/" + GAME + "/" + CONTENT_TYPE + "/" + mod + "/files/all?filter-game-version=" + versionID
    else: baseURL = "https://curseforge.com/" + GAME + "/" + CONTENT_TYPE + "/" + mod + "/files/all"
    print(f"Loading page for mod name {mod}...")
    page = wd.get(baseURL)
    wd.implicitly_wait(100) # Have to implicitly wait or else it's a no-no
    print("Initializing BeautifulSoup...")
    soup = bs(wd.page_source, 'html.parser')
    print("Found mod " + soup.find("h2", class_="font-bold text-lg break-all").string)

    # Find the version selector dropdown and get the version ID (if it hasn't already been found)
    if versionID == "":
        versionSelector = soup.find("select")
        versionID = re.sub(r":", r"%3A", versionSelector.find("option", text = re.compile(VERSION))["value"]) # Get the ID (and fix it up so it works)
        print(f"Found version ID {versionID}, reloading page")
        page = wd.get(baseURL + "?filter-game-version=" + versionID)
        print(page) # Returns None. Why?

    dl = page.find("a", class_="button button--hollow mr-2 button--icon-only")["href"] + "/file"
    print(f"Found download link {dl}")
    downloadURLs.append(dl)
