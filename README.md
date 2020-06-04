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
Yes, I do realize that Twitch does have an API for this. I sadly found that out right at the end of when I got it to work. I'll change it later, because the current webscraping method is slow (then I can remove the Selenium and geckodriver requirements).
