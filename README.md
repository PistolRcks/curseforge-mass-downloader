# CurseForge Webscraper
*A Python script to scrape the web for mods on the website CurseForge*

## Dependencies
* Python 3.6 or above
* [Requests](https://pypi.org/project/requests/)
* [BeautifulSoup 4](https://pypi.org/project/beautifulsoup4/)
* [Selenium](https://pypi.org/project/selenium/)
* [geckodriver](https://github.com/mozilla/geckodriver/releases)

  * NB: `geckodriver` is featured in many Linux distributions, such as Arch Linux (`sudo pacman -S geckodriver`) and Ubuntu 18.04+ (`sudo apt install firefox-geckdriver`). You will need to add `geckodriver` to your path manually if you are not using repositories.

## Usage
```
python main.py
```
(currently there are no commandline options; this will be fleshed out later)

## Addendum
This branch is slow, and the main idea was to download modpacks from CurseForge. The CurseProxy API is faster at this, so it will be used from now on. This branch remains for archival purposes, and may or may not be updated.
