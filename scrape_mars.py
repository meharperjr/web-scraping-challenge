# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
from pprint import pprint
from time import sleep

def scrape():

    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=True)
    
    
    news_title, news_paragraph = mars_news(browser)
    
  
    results = {
        "title": news_title,
        "paragraph": news_paragraph,
        "image_URL": jpl_image(browser),
        "weather": mars_weather_tweet(browser),
        "hemispheres": mars_hemis(browser),
    }

   
    browser.quit()
    return results

def mars_news(browser):
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    news_soup = BeautifulSoup(html, "html.parser")
    slide_element = news_soup.select_one("ul.item_list li.slide")
    news_title = slide_element.find("div", class_="content_title").get_text()
    news_paragraph = slide_element.find("div", class_="article_teaser_body").get_text()
    return news_title , news_paragraph

def jpl_image(browser):
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    
    browser.click_link_by_partial_text('FULL IMAGE')
    sleep(1)
    browser.click_link_by_partial_text('more info')

    html = browser.html
    image_soup = BeautifulSoup(html, 'html.parser')

  
    feat_img_url = image_soup.find('figure', class_='lede').a['href']
    feat_img_full_url = f'https://www.jpl.nasa.gov{feat_img_url}'
    return feat_img_full_url

def mars_weather_tweet(browser):
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    html = browser.html
    tweet_soup = BeautifulSoup(html, 'html.parser')
    
 
    mars_weather  = tweet_soup.find('p', class_='TweetTextSize').text
    return mars_weather 
    
    
def mars_hemis(browser):
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    hemisphere_image_urls = []

# Get a List of All the Hemispheres
    links = browser.find_by_css("a.product-item h3")
    for item in range(len(links)):
        hemisphere = {}
    
    # Find Element on Each Loop to Avoid a Stale Element Exception
        browser.find_by_css("a.product-item h3")[item].click()
    
    # Find Sample Image Anchor Tag & Extract <href>
        sample_element = browser.find_link_by_text("Sample").first
        hemisphere["img_url"] = sample_element["href"]
    
    # Get Hemisphere Title
        hemisphere["title"] = browser.find_by_css("h2.title").text
    
    # Append Hemisphere Object to List
        hemisphere_image_urls.append(hemisphere)
    
        return hemisphere_image_urls