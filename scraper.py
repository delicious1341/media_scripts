from selenium.webdriver.common.by import By
from selenium.webdriver.support.relative_locator import locate_with

def wikipedia(media: dict, driver):

    # launch wikipedia search and in the search box type in the title and press enter
    driver.get("https://en.wikipedia.org/w/index.php?search=")
    search_box = driver.find_element(By.ID, "ooui-php-1")
    
    search_terms = media["title"] + " " + media["media_type"] + " "

    # add the author/comedian/musician's name
    match media["media_type"]:
        case "Book" | "Comedy Special" | "Music":
            search_terms += media ["collection"]

    search_box.send_keys(search_terms + "\ue007")

    # wait until an article page is selected and loaded
    while (not driver.current_url.startswith("https://en.wikipedia.org/wiki/")): 
        driver.implicitly_wait(1)

    # get the title from the correct html element as per media type
    try:
        # split the url for the article to get rid of tracking terms
        media["wikipedia_link"], null = driver.current_url.rsplit("?")
    
    # if a dedicated article and/or title isn't automatically found, log it into the csv
    except Exception:
        print("Dedicated Wikipedia article for " + media["title"] + " couldn't be found")
        media["wikipedia_link"] = "N/A"

    

def release(media, driver):

    INFO_BOX_HEADERS = {
        "Film": ["Release dates"],
        "TV Series": ["Release", "Original Run"],
        "Book": ["Published", "Publication date"],
        "Game": ["Release"],
        "Comedy Special": ["Release"],
        "Music": ["Released"],
        }

    try:

        # go to wikipedia page
        driver.get(media["wikipedia_link"])

        # get the wikipedia infobox headers
        info_box = driver.find_elements(By.TAG_NAME, "th")

        # iterate through the headers to get the release row, if multiple raise exception
        release_box = None
        
        for i in info_box:
                
                if i.text in INFO_BOX_HEADERS[media["media_type"]]:
                    if release_box == None: 
                        release_box = i
                        
                    else:
                        raise ValueError("Multiple release dates scraped")
                    

        # get the data from the corresponding release row
        media["release_date"] = driver.find_element(locate_with(By.TAG_NAME, "td").to_right_of(release_box)).text.replace("\n", " ")
        
    except Exception:
        print("Release date for " + media["title"] + " couldn't be found")
        media["release_date"] = "N/A"


def critics(media, driver):
    try:
        match media["media_type"]:
            case "Film":
                # letterboxd search for film
                driver.get("https://letterboxd.com/search/" + media["title"])
                
                # wait until an film page is selected and loaded
                while (not driver.current_url.startswith("https://letterboxd.com/film/")): 
                    driver.implicitly_wait(1)
                
                # get rating
                detailed_rating = driver.find_element(By.CLASS_NAME, "display-rating").get_attribute("data-original-title")
                extracted_rating = detailed_rating.removeprefix("Weighted average of ")[0:4]
                processed_rating = float(extracted_rating)*2

                media["critics'_score"] = processed_rating

            case "TV Series" | "Comdey Special":
                # imdb search for tv series
                driver.get("https://www.imdb.com/find/?q=" + media["title"])
                
                while (not driver.current_url.startswith("https://www.imdb.com/title/")): 
                    driver.implicitly_wait(1)
                
                media["critics'_score"] = driver.find_element(By.CLASS_NAME, "sc-bde20123-1").text
            
            case "Book":
                # goodreads search for book
                driver.get("https://www.goodreads.com/search?q=" + media["title"])

                while (not driver.current_url.startswith("https://www.goodreads.com/book/")): 
                    driver.implicitly_wait(1)
                
                media["critics'_score"] = driver.find_element(By.CLASS_NAME, "RatingStatistics__rating").text
            
            case "Game":
                # metacritic search for game
                driver.get("https://www.metacritic.com/search/" + media["title"])

                while (not driver.current_url.startswith("https://www.metacritic.com/game/")): 
                    driver.implicitly_wait(1)
                
                media["critics'_score"] = float(driver.find_element(By.CLASS_NAME, "c-siteReviewScore").text)/10

            case "Music":
                pass
            
        media["critics'_link"] = driver.current_url
    
    except Exception:
        print("Critics' score and link for " + media["title"] + " couldn't be found")
        media["critics'_score"] = "N/A"
        media["critics'_link"] = "N/A"
    

def art(media, driver):
    pass