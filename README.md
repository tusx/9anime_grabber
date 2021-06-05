# 9anime_grabber

About:
- This is a Selenium based 9anime link grabber.
- Currently grabs all episode links for given link, Max grab is 1 to 150 episodes and download them to specified location.
- This also uses Ublock-origin to function properly.
- This is designed with firefox browser in mind.
- Remember to put all files in one folder that inclues geckodriver and Ublock-origin .xpi file

Requirements:
- Firefox Browser, latest version is best.
- Selenium For Python3 (tested for python3.8)
- clint module is used to show the download progress
- requests may be already installed but just make sure you have it installed
>Following are the modules that may be needed to installed.
```python
pip install selenium
pip install clint
pip install requests
```
Note: Download below files according to your OS and architecture. for ublock just download the firefox .xpi file.

- Firefox Webdriver (geckodriver), which can be download from [here](https://github.com/mozilla/geckodriver/releases). Download the latest for your system.
- Download the Ublock-origin .xpi file for Firefox from [here](https://github.com/gorhill/uBlock/releases).

How to use:
- Open 9anime.py and change the highlighted parameters before runing the script.
- run the 9anime.py
- when prompted paste the link to the anime you want to download like
>https://domain.to/watch/pokemon-the-series-xy-dub.j2wn/ep-1
- when it starts downloading episodes it will automatically create a folder for it.
- if evrything goes well just sitback and watch it work.
>Note: if the download location remains the same it will skip downloading already downloaded episoded, if a download fails please delete the partially downloaded file and try again

