from splinter import Browser
from bs4 import BeautifulSoup as bs
import time

def scrape():
    
    executable_path = {"executable_path": "chromedriver"}
    browser = Browser("chrome", **executable_path, headless=False)

    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    time.sleep(2)

    html = browser.html
    soup = bs(html, "html.parser")

    news_title_all = soup.findAll("div", {"class": "content_title"})
    news_p_all = soup.findAll("div", {"class": "article_teaser_body"})

    for title in news_title_all:
        news_title = news_title_all[0].text
        
    for paragraph in news_p_all:
        news_p = news_p_all[0].text

    url_pic = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url_pic)

    fullimage = browser.find_by_id('full_image')
    fullimage.click()

    browser.is_element_present_by_text('more info', wait_time=2)
    more_info = browser.links.find_by_partial_text('more info')
    more_info.click()

    html = browser.html
    moreinfo_soup = bs(html, 'html.parser')

    image_title = moreinfo_soup.find('h1', class_='article_title')

    image_title = str(image_title.text)

    image_title = image_title.replace('\n', '')
    image_title = image_title.replace('\t', '')

    image_title

    image_url = moreinfo_soup.select_one('.main_image').get('src')

    image_url

    full_image_url = f'https://www.jpl.nasa.gov{image_url}'

    twitter_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(twitter_url)
    time.sleep(2)

    html = browser.html
    twitter_soup = bs(html, "html.parser")

    try:
        for x in twitter_soup.find('p', class_ ="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text"):
            mars_weather = x
            break
    except: TypeError

    import pandas as pd
    fact_url = 'https://space-facts.com/mars/'
    browser.visit(fact_url)
    time.sleep(2)

    fact_table = pd.read_html(fact_url)
    df = fact_table[0]

    html_table = df.to_html()
    print(html_table)

    hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemisphere_url)

    html = browser.html
    hemisphr_soup = bs(html, "html.parser")

    hemisphr_image_urls = []

    hemisphr_soup.find_all('img')

    browser.quit()

    scraped_data = {

        "news_title": news_title,
        "news_paragraph": news_p,
        "image_url": full_image_url,
        "mars_info":mars_weather

    }

    import pymongo

    conn = "mongodb://127.0.0.1:27017"
    client = pymongo.MongoClient(conn)

    db = client.mission_mars
    collection = db.info_mars


    db.collection.insert_many(
        [{
        "news_title": news_title,
        "news_paragraph": news_p,
        "image_url": full_image_url,
        "mars_info": mars_weather
        }])


    return scraped_data
    # # MongoDB and Flask 

    # import pymongo
    # conn = "mongodb://127.0.0.1:27017"
    # client = pymongo.MongoClient(conn)

    # db = client.mission_mars

    # collection = db.collection

    # db.collection.insert_many(
    #         [{
    #             "news_title": news_title,
    #             "news_paragraph": news_p,
    #             "image_url": full_image_url,
    #             "weather": mars_weather
    #         }])