from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import selenium
import sys
import time
import pathlib

#=======================================================================
#=======================================================================
# Important, below parameters must be set first before using this script
#=======================================================================
#=======================================================================

path = r"D:\code\9anime_grabber-main" # this is the path to ther folder where geckodriver.exe is loacated
extension_path = path+r'\uBlock0_1.35.0.firefox.xpi'  # Must be the full path to an XPI file!

#=======================================================================
#=======================================================================

url9 = input("9anime.to season url starting with http or https: ") 
link = ""
name = url9.split("/")
fname = name[4].split(".")
fname = fname[0]

print("opening firefox..")
browser = webdriver.Firefox(path)

print("installing ublock origin")
browser.install_addon(extension_path, temporary=True)

browser.get(url9)

#delay to let the episodes be loaded, sorced from 
#https://stackoverflow.com/questions/26566799/wait-until-page-is-loaded-with-selenium-webdriver-for-python
#=======================================================================

# adjust the seconds if you are on slower connection
delay = 5 # seconds
try:
    myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.ID, 'server40')))
    print("Page is ready!")
except TimeoutException:
    print("Loading took too much time!")


def write_link(link):
    path = pathlib.Path(fname+".txt")
    if(path.exists()):
        f = open(fname+".txt", "a")
        f.write(link)
        f.close()
    else:        
        f = open(fname+".txt", "w+")
        f.write(link)
        f.close()

def get_link():
    elements = browser.find_elements_by_id("player")
    for e in elements:
        myframe = e.find_element_by_tag_name("iframe")
        link = myframe.get_attribute("src")
        return link+"\n"

#select the streamtap server
try:
    select_ser = browser.find_elements_by_id("server40")
    print(select_ser)
    for serv in select_ser:
        serv.click()
except:
    ptint("server select failed try increasing the delay")
    browser.quit()
    

#get all episodes 
episo = browser.find_elements_by_class_name("episodes")
for ep in episo:
    single_ep = ep.find_elements_by_tag_name("li")

    for s_ep in single_ep:
        s_ep.click()
        #wait for iframe tag to appear
        time.sleep(delay)
        #lets get those link real quick
        link = get_link()
        #write link
        write_link(link)

print("closing firefox..")

browser.quit()

print(fname+".txt created with links")
