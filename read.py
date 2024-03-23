import csv
import json

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.relative_locator import locate_with
driver = webdriver.Firefox()

with open("media_tracker_wiki.csv", "r") as csv_file:
    csv_reader = csv.DictReader(csv_file)
    # use list() otherwise you get where stored in memory
    # gets list of each media as a dict with headings as keys
    media_list = list(csv_reader)
    # print(media_list[0]) Brainiac

with open("media_tracker_wikipedia.csv") as f:
    rows_done = sum(1 for line in f) - 1

# https://stackoverflow.com/questions/2363731/how-to-append-a-new-row-to-an-old-csv-file-in-python
# start new line in the csv
with open("media_tracker_wikipedia.csv", "a", newline='') as csv_file_2:
    csv_writer = csv.writer(csv_file_2)
    
    final_row_included = -1 + 1500

    #writing the headers for the csv list
    #csv_writer.writerow(["title", "wikipedia_link"])
    
    for media in media_list[rows_done:final_row_included]:
        # print(json.dumps(media, indent=4))

        driver.get("https://en.wikipedia.org/w/index.php?search=")
        search_box = driver.find_element(By.ID, "ooui-php-1")
        search_box.send_keys(media["title"] + "\ue007")
        #search_box.send_keys(media["title"] + " " + media["collection"] + "\ue007") # music
        
        
        while (not driver.current_url.startswith("https://en.wikipedia.org/wiki/")): 
            driver.implicitly_wait(1)
        
        # https://stackoverflow.com/questions/64075830/selenium-cant-find-an-element-by-class-name use dot for compound class names
        # replace for titles like Wallace and Gromit Cracking inventions
        #title = driver.find_element(By.CLASS_NAME, "infobox-above.summary").text.replace("\n", " ") #series films or music single
        #title = driver.find_element(By.CLASS_NAME, "infobox-subheader").text.replace("\n", " ") #anime
        #title = driver.find_element(By.CLASS_NAME, "infobox-above.summary.album").text.replace("\n", " ") #music
        #title = driver.find_element(By.CLASS_NAME, "infobox-above.fn").text.replace("\n", " ") #game
        title = driver.find_element(By.CLASS_NAME, "infobox-title").text.replace("\n", " ") #book

        link, null = driver.current_url.rsplit("?")
        csv_writer.writerow([title, link])

    driver.quit()
        
        


