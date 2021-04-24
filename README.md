# 9anime_grabber

About:
- This is a Selenium based 9anime link grabber.
- Currently grabs all episode links for given link, Max grab is 1 to 150 episodes.
- This also uses Ublock-origin to function properly.
- This is designed with firefox browser in mind.
- Remember to put all files in one folder that inclues geckodriver and Ublock-origin .xpi file

Requirements:
1. Firefox Browser, latest version is best.
2. Selenium For Python3 (tested for python3.8)
```python
pip install selenium
```
Note: Download below files according to your OS and architecture. for ublock just download the firefox .xpi file.

3. Firefox Webdriver (geckodriver), which can be download from [here](https://github.com/mozilla/geckodriver/releases). Download the latest for your system.
4. Download the Ublock-origin .xpi file for Firefox from [here](https://github.com/gorhill/uBlock/releases).

How to use:
1. Open 9anime.py and change the following parameters.
- Add folder path where all the files are located to the path variable at line 17. this is the path to ther folder where geckodriver.exe is loacated.
- Add the ublock-origin xpi file name including the .xpi at line 18.
2. For Windows user just double click run.bat file and then paste the link. for other OS users please run the 9anime.py file in your terminal.
3. After pasting link it will open firefox browser and throught each and every episode and when finished the browser window will close by itself
4. In the same folder you will find a .txt file containing all the links. use downloader like Jdownloader2, paste all the links and download.
