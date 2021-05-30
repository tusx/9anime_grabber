from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from pathlib import Path
from clint.textui import progress
import time
import requests
import threading

max_threads = 12

filename = 'pokemon-the-series-sun-moon-dub.txt'
extension_path = '/home/tusx/code/9anime_grabber-main/uBlock0_1.35.0.firefox.xpi'
download_path = '/media/tusx/nam/downloads'


print("opening firefox..")
browser = webdriver.Firefox()

print("installing ublock origin")
browser.install_addon(extension_path, temporary=True)



thread_num = 0




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

def download(url,path):
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

def get_links(name):
    file1 = open(name,'r')
    link_list = []
    for line in file1:
        link_list.append(line)

    return link_list

def download_thread(url,path):
    if thread_num < max_threads:
        x = threading.Thread(target=download, args=(url,path))
        x.start()
    else:
        print(thread_num," threads reached, now waiting to be freed")
        time.sleep(30)
        download_thread(url,path)

def start():

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

        # Now we are getiing the download link
        downLink = getdownlink(link)

        # Multi-Thread Downloading 
        print("Downloading :",episodeName)
        download_thread(downLink,fullDownloadPath)
        
        
        

        
    
    browser.close()




start()