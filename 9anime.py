from selenium import webdriver
import selenium
import sys
import time
import pathlib

url9 = input("9anime.to season url: ") 

print("setting up firefox")
print("installing ublock origin")
print("opening firefox..")
link = ""
name = url9.split("/")
fname = name[4].split(".")
fname = fname[0]

path = r"C:\Users\amrin\Desktop\python"
browse = webdriver.Firefox(path)
extension_path = path+r'\uBlock0_1.30.7b5.firefox.signed.xpi'  # Must be the full path to an XPI file!
browse.install_addon(extension_path, temporary=True)
browse.get(url9)

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
    elements = browse.find_elements_by_id("player")
    for e in elements:
        myframe = e.find_element_by_tag_name("iframe")
        link = myframe.get_attribute("src")
        return link+"\n"

#select the streamtap server
select_ser = browse.find_elements_by_id("server40")
for serv in select_ser:
    serv.click()

    

#get all episodes 
episo = browse.find_elements_by_class_name("episodes")
for ep in episo:
    single_ep = ep.find_elements_by_tag_name("li")

    for s_ep in single_ep:
        s_ep.click()
        #wait for iframe tag to appear
        time.sleep(5)
        #lets get those link real quick
        link = get_link()
        #write link
        write_link(link)

print("closing firefox..")
browse.quit()

print(fname+".txt created with links")