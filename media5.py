from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.relative_locator import locate_with
driver = webdriver.Firefox()

def wikipedia_release_dates(media_type, link):
    # go to wikipedia page
    driver.get(link)

    # get the wikipedia infobox headers
    info_box = driver.find_elements(By.TAG_NAME, "th")

    # iterate through the headers to get the release row
    INFO_BOX_HEADERS = {"film": "Release dates", "series": "Release", "book": "Published", "game": "Release", "music": "Released"}
    for i in info_box:
            if i.text == INFO_BOX_HEADERS[media_type]: 
                # heading changes depending on media type
                release_box = i

    # get the data from the corresponding release row
    date_locator = driver.find_element(locate_with(By.TAG_NAME, "td").to_right_of(release_box))
    return(date_locator.text)

def wikipedia_imdb_link(link):
    # go to wikipedia page
    driver.get(link)

    # get the "external links" heading and then the IMDb inteifier
    external_heading = driver.find_element(By.ID, "External_links")
    imdb_identifier = driver.find_elements(locate_with(By.TAG_NAME, "a").below(external_heading))
    for i in imdb_identifier:
        link = i.get_attribute("href")
        if "www.imdb.com" in link:
            return(link)

def imdb_parental(link):
    # go to imdb page with parental information
    driver.get(link + "parentalguide")
    
    driver.implicitly_wait(2)

    # get the age certifications
    certs = driver.find_elements(By.CLASS_NAME, "ipl-inline-list__item")
    
    # create list of certifications
    relevant_certs = []
    
    # if no UK certificates, then check other countries according to heirachy
    countries = ["United Kingdom", "United States", "Canada", "Australia", "Singapore", "South Korea"]
    
    for country in countries:
        print(country)
        for i in certs:
            if (country in i.text) and ("Not Rated" not in i.text):
                relevant_certs.append(i.text)
        if relevant_certs:
            return(relevant_certs)

def main():
    series_link="https://en.wikipedia.org/wiki/Courage_the_Cowardly_Dog"
    film_link="https://en.wikipedia.org/wiki/Dune_(2021_film)"
    book_link="https://en.wikipedia.org/wiki/Dune_(novel)"
    game_link="https://en.wikipedia.org/wiki/Super_Mario_Kart"
    music_link="https://en.wikipedia.org/wiki/Vultures_1"

    #print(wikipedia_release_dates("music", music_link))
    #print(wikipedia_imdb_link(series_link))
    
    imdb_link="https://www.imdb.com/title/tt13433812/"
    
    print(imdb_parental(imdb_link))
    
    driver.quit()

if __name__ == "__main__":
    main()
