from bs4 import BeautifulSoup
import requests
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import pprint

def scrape():

    mars_dict = {}

    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    ## ---------------------------- NASA Mars News ----------------------------

    print("\n\n...... NASA Mars News")
    url = "https://redplanetscience.com/"
    browser.visit(url)

    html = browser.html

    soup = BeautifulSoup(html, 'html.parser')
    # print(soup.prettify())

    results = soup.find_all("div", class_="content_title")
    # print(results)
    news_title = results[0].text
    # print("Title: ", news_title)

    print("PART 1 of 2: News Title retrieved...")

    results = soup.find_all("div", class_="article_teaser_body")
    # print(results)
    news_p = results[0].text
    # print(" News: ", news_p)

    print("PART 2 of 2: News Paragraph retrieved...\n")

    mars_dict = {"news_title": news_title, "news_p": news_p}

    ## ---------------------------- JPL Mars Space Images - Featured Image ----------------------------

    print("...... JPL Mars Space Images - Featured Image")
    # Target
    # featured_image_url = "https://spaceimages-mars.com/image/featured/mars2.jpg"

    url = "https://spaceimages-mars.com/"
    browser.visit(url)

    html = browser.html

    # browser.links.find_by_text(" FULL IMAGE").click()

    soup = BeautifulSoup(html, 'html.parser')

    results = soup.find_all("img", class_="headerimage")[0].attrs['src']
    # print(results)

    featured_image_url = url+results
    # print(featured_image_url)

    print("PART 1 of 1: Featured Image URL retrieved...\n")

    mars_dict["featured_image_url"] = featured_image_url

    ## ---------------------------- Mars Facts ----------------------------

    print("...... Mars Facts")
    url = "https://galaxyfacts-mars.com/"
    # browser.visit(url)

    # html = browser.html

    tables = pd.read_html(url)
    mars_table = tables[0]
    mars_table.columns = mars_table.iloc[0]
    mars_table = mars_table.drop(mars_table.index[0])
    mars_table

    mars_table.to_html("Missions_to_Mars/mars_table.html", index=False)

    mars_dict["mars_table"] = mars_table.to_html(index=False)

    print("PART 1 of 1: Mars Table retrieved...\n")

    ## ---------------------------- Mars Hemispheres ----------------------------

    print("...... Mars Hemispheres")

    url = "https://marshemispheres.com/"
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    results = soup.find_all('a', class_="itemLink product-item")

    hemispheres = []
    for result in results:
        
        try:
            hemispheres.append(result.find("h3").text)
            
        except AttributeError as e:
            pass
            # print(e)
        
    # print(hemispheres)


    hemisphere_image_urls = []

    for i in range(4):
        
        browser.links.find_by_partial_text(hemispheres[i]).click()
        
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        
        image = soup.find_all("img", class_="wide-image")[0].attrs['src']
    #     print(image)
        
        
        hemisphere_image_urls.append({"title": hemispheres[i], "img_url": url+image})
        
        browser.links.find_by_partial_text(hemispheres[4]).click()

        print(f"PART {i+1} of 4: {hemispheres[i]} URL retrieved...")
        
    # print(hemisphere_image_urls)    
    
    mars_dict["hemisphere_image_urls"] = hemisphere_image_urls

    # print(mars_dict)

    print("\n\n\n...... SCRAPE COMPLETED ......")

    return mars_dict

# test = scrape()
# print("\n\n\n---------------------------------------------------------------\n")
# pprint.pprint(test)