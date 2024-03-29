from os import listdir # for csv_name setter
from csv import DictReader, DictWriter # for read_csv_data() and write_csv_data()
from selenium import webdriver # for scrape()

import scraper

class Tracker:
    PATH = "D://drive_live/projects/media_consumption/media_scripts"
    
    def __init__(self, csv_name: str):
        
        # .csv filename
        self.csv_name = csv_name

        # process the .csv into python data
        self.read_csv_data()

    # Getter for csv_name
    @property
    def csv_name(self):
        return self._csv_name

    # Setter for csv_name
    @csv_name.setter
    def csv_name(self, csv_name):
        
        # list of all .csv files in PATH
        csv_list = [f for f in listdir(self.PATH) if f.endswith(".csv")]

        # error handling to confirm .csv file is in the directory
        if csv_name not in csv_list:
            raise ValueError(f"{csv_name} not found in PATH")
        
        self._csv_name = csv_name
    
    def read_csv_data(self):
        
        with open(self.PATH + "/" + self.csv_name, "r") as csv_file:
            csv_reader = DictReader(csv_file)

            # use list() otherwise you get where stored in memory
            # returned is a list of each media_tracker row as a dict with the csv headings as keys:
            # [{'title': 'Brainiac: Science Abuse', ...}, {'title': 'Horrible Histories', ...}
            # row 2 in the csv "Brainiac", is list[0] in the returned list
            self.data =  list(csv_reader)
            self.headings = list(self.data[0].keys())
    
    # find data that needs scraping for media
    def scrape(self):
        
        # store new data
        self.new_data = self.data
        
        # start browser for scraping
        driver = webdriver.Firefox()

        for media in self.new_data[0:5]: # test
            if not media["wikipedia_link"]:
                scraper.wikipedia(media, driver)
            
            if not media["release_date"]:
                scraper.release(media, driver)
            
            if not media["critics'_score"]:
                scraper.critics(media, driver)
            
            if not media["art"]:
                scraper.art(media, driver)
        
        driver.quit()    

    # write the new data into a csv file
    def write_csv_data(self):

        # need newline="" due to issue with windows
        with open(self.PATH + "/" + self.csv_name, "w", newline="") as csv_file:
            csv_writer = DictWriter(csv_file, fieldnames=self.headings)

            csv_writer.writeheader()
            csv_writer.writerows(self.new_data)