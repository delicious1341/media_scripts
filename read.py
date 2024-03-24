import csv # get_tracker()
import json # print_row_attribute

# append_media_wikipedia()
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.relative_locator import locate_with

def main():

    LATEST_COMPLETED_TRACKER = "media_tracker_2_wikipedia.csv"
    CURRENT_INCOMPLETE_TRACKER = "media_tracker_type_copy.csv"

    LAST_CSV_ROW_TO_APPEND = 1424

    # create list of dicts from latest completed tracker, since it has all media
    completed_tracker_list = get_tracker(LATEST_COMPLETED_TRACKER)

    # count csv rows in the current incomplete tracker to see progress
    print("rows in latest complete tracker:", total_csv_rows(LATEST_COMPLETED_TRACKER))
    print("rows in current incomplete tracker:", total_csv_rows(CURRENT_INCOMPLETE_TRACKER))
    
    # print_media_attribute(completed_tracker_list, total_csv_rows(CURRENT_INCOMPLETE_TRACKER), "title")

    # append the current incomplete tracker with wikipedia data using the completed_tracker_list for search terms 
    append_media_wikipedia(CURRENT_INCOMPLETE_TRACKER, completed_tracker_list, LAST_CSV_ROW_TO_APPEND)

    

def get_tracker(filename: str):
    with open(filename, "r") as csv_file:
        csv_reader = csv.DictReader(csv_file)
     
        # use list() otherwise you get where stored in memory
        # returned is a list of each media_tracker row as a dict with the csv headings as keys:
        # [{'title': 'Brainiac: Science Abuse', ...}, {'title': 'Horrible Histories', ...}
        # row 2 in the csv "Brainiac", is list[0] in the returned list
        return list(csv_reader)


def list_index(csv_row):
    # row 2 in the csv "Brainiac", is list[0] in the returned list
    return csv_row - 2

def print_media_attribute(tracker_list, csv_row: int, heading: str):
    
    # if no specific attribute specified or "all" is specified, print all the attributes in JSON format
    if heading != "all":
        print(tracker_list[list_index(csv_row)][heading])
    else:
        print(json.dumps(tracker_list[list_index(csv_row)], indent=4))


def total_csv_rows(filename):
    with open(filename) as f:
        
        # count all the rows of the csv
        return sum(1 for line in f)


def append_media_wikipedia(filename, tracker_list, final_csv_row_to_include):
    
    # https://stackoverflow.com/questions/2363731/how-to-append-a-new-row-to-an-old-csv-file-in-python
    # start new line in the csv
    with open(filename, "a", newline='') as csv_file_2:
        csv_writer = csv.writer(csv_file_2)

        # new media to index is after the currently done rows 
        first_new_media_index = list_index(total_csv_rows(filename)) + 1
        # iteration doesn't include the final number/slice, so plus one
        last_new_media_index_plus_one = list_index(final_csv_row_to_include) + 1

        # CLASS_NAMEs of wikipedia html elements that are present for each particular media type 
        media_type_wikipedia_element = {
            "series": "infobox-above.summary",
            "film": "infobox-above.summary",
            "series anime": "infobox-subheader",
            "music single": "infobox-above.summary",
            "music": "infobox-above.summary.album",
            "game": "infobox-above.fn",
            "book": "infobox-title",
            }

        # launch firefox
        driver = webdriver.Firefox()

        for media in tracker_list[first_new_media_index: last_new_media_index_plus_one]:
            
            # launch wikipedia search and in the search box type in the title and press enter
            driver.get("https://en.wikipedia.org/w/index.php?search=")
            search_box = driver.find_element(By.ID, "ooui-php-1")
            search_box.send_keys(media["title"] + "\ue007")
            # search_box.send_keys(media["title"] + " " + media["collection"] + "\ue007") # for music add artist name
        
            # wait until an article page is selected and loaded
            while (not driver.current_url.startswith("https://en.wikipedia.org/wiki/")): 
                driver.implicitly_wait(1)
            
            try:
                # get the title from the correct html element as per media type
                # for long titles that wrap, replace new line with a space
                title = driver.find_element(By.CLASS_NAME, media_type_wikipedia_element[media["media_type"]]).text.replace("\n", " ")
            
                # split the url for the article to get rid of tracking terms
                link, null = driver.current_url.rsplit("?")
            
            # if a dedicated article and/or title isn't automatically found, log it into the csv
            except Exception:
                message = "Dedicated Wikipedia article for " + media["title"] + " couldn't be found"
                print(message)
                title = "unofficial title: " + media["title"]
                link = message

            # append the incomplete csv with a new row consisting of the official media title and its relevant wikipedia link
            csv_writer.writerow([title, link])

        driver.quit()


if __name__ == "__main__":
    main()