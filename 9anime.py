import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import os
import time
from pathlib import Path
import requests
from clint.textui import progress
import threading



#=======================================================================
#=======================================================================
# Important, below parameters must be set first before using this script
#=======================================================================
#=======================================================================

driver_path = "/usr/local/bin" # this is the path to ther folder where geckodriver file is loacated
extension_path = '/home/tusx/code/9anime_grabber-main/uBlock0_1.35.0.firefox.xpi'  # Must be the full path to an XPI file! of ublock origin
download_path = '/media/tusx/nam/downloads' # give the full path to where you want your downloads to go
max_threads = 10 # this is the max number of simultaneous downloads that can happen at once. when limit is reached it will wait for a download to finish before starting another one
delay = 5 # seconds, adjust the seconds if you are on slower connection or if the episode loading is taking too much time
thread_num = 0 # this is the starting download number, every download is +1 to this number. no need to change this


#=======================================================================
#=======================================================================
#=======================================================================
#=======================================================================





def write_link(link):
    path = Path(fname+".txt")
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


       


def getdownlink(link):
    browser.get(link)
    try:
        myElem = WebDriverWait(browser, 3).until(EC.presence_of_element_located((By.CLASS_NAME, 'plyr-container')))
        print("Page is ready!")
    except TimeoutException:
        print("Loading took too much time! now retrying")
        getdownlink(link)
    select_play_btn= browser.find_elements_by_class_name("plyr-container")

    for pbtn in select_play_btn:
        pbtn.click()
    time.sleep(2)
    for pbtn in select_play_btn:
        pbtn.click()

    select_video= browser.find_elements_by_id("mainvideo")
    for sv in select_video:
        link = sv.get_attribute("src")
        
    return link

def update_thread(num):
    global thread_num
    thread_num = num

def already_downloaded(path_n):
    my_file = Path(path_n)
    if my_file.is_file():
        result = 'no'
    else:
        result = 'yes'
        
    return result


def download(url,path):
    try:
        total_thread = thread_num + 1
        update_thread(total_thread)
        r = requests.get(url, stream=True)
        with open(path, 'wb') as f:
            total_length = int(r.headers.get('content-length'))
            for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1): 
                if chunk:
                    f.write(chunk)
                    f.flush()
        
        new_thread_num = thread_num - 1
        update_thread(new_thread_num)
        
    except:
        new_thread_num = thread_num - 1
        update_thread(new_thread_num)

def get_links(name):
    file1 = open(name,'r')
    link_list = []
    for line in file1:
        link_list.append(line)
    file1.close() 
    return link_list

def download_thread(url,path):
    if thread_num < max_threads:
        x = threading.Thread(target=download, args=(url,path))
        x.start()
    else:
        print(thread_num," threads reached, now waiting some to be finished. recheck will happen in 30 sec.")
        
        time.sleep(30)
        download_thread(url,path)

def down_start():

    links = get_links(filename)

    #make downloader folder if not exists
    downloadFolder = filename.split('.txt')
    downloadFolder = downloadFolder[0]
    folder_path = download_path+'/'+downloadFolder
    Path(folder_path).mkdir(parents=True, exist_ok=True)

    #Now we will get the download links for every episode
    count = 0
    for link in links:
        count +=1
        #making episode name
        episodeNumber = str(count)
        episodeName = downloadFolder+'-E'+episodeNumber+".mp4"

        # Full Download path
        fullDownloadPath = folder_path+'/'+episodeName

        # Check if already downloaded or not
        what_to_do = already_downloaded(fullDownloadPath)
        if what_to_do == 'yes':
            # Now we are getiing the download link
            downLink = getdownlink(link)
            # Multi-Thread Downloading 
            print("Downloading :",episodeName)
            download_thread(downLink,fullDownloadPath)
        else:
            print("Already Downloaded:",fullDownloadPath)

def do_click(where):
    try:
        where.click()
        #wait for iframe tag to appear
        time.sleep(delay)
        link = get_link()
        return link

    except:
        do_click(where)

def main_start():

    global fname
    global browser

    url9 = input("9anime.to url starting with http or https: ") 
    # url9 = "https://9anime.to/watch/strike-witches-road-to-berlin-dub.yynp/ep-1"
    link = ""
    name = url9.split("/")
    fname = name[4].split(".")
    fname = fname[0]



    print("opening firefox..")
    browser = webdriver.Firefox(driver_path)

    print("installing ublock origin")
    browser.install_addon(extension_path, temporary=True)

    browser.get(url9)

    #delay to let the episodes be loaded, sorced from 
    #https://stackoverflow.com/questions/26566799/wait-until-page-is-loaded-with-selenium-webdriver-for-python
    #=======================================================================


    try:
        myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.ID, 'server40')))
        print("Page is ready!")
    except TimeoutException:
        print("Loading took too much time!")

    #select the streamtap server
    try:
        select_ser = browser.find_elements_by_id("server40")
        # print(select_ser)
        for serv in select_ser:
            serv.click()
    except:
        print("server select failed try increasing the delay")
        browser.quit()
        

    #get all episodes 
    episo = browser.find_elements_by_class_name("episodes")
    for ep in episo:
        single_ep = ep.find_elements_by_tag_name("li")

        for s_ep in single_ep:
            link = do_click(s_ep)
            #write link
            write_link(link)

    global filename
    filename = fname+'.txt'

    down_start() # this function will start the download from a .txt file that is create

    # this will delete the .txt file after downloading whol season
    if os.path.exists(filename):
        os.remove(filename)
    else:
        print("The file does not exist") 

    print("closing firefox..")

    browser.quit()

    print(fname,"grab Complete")
    


if __name__ == "__main__":
    main_start()
