# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
from pprint import pprint
from time import sleep

def scrape():

    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=True)
    
    
    first_title, first_paragraph = mars_news(browser)
    
  
    results = {
        "title": first_title,
        "paragraph": first_paragraph,
        "image_URL": jpl_image(browser),
        "weather": mars_weather_tweet(browser),
        "facts": mars_facts(),
        "hemispheres": mars_hemis(browser),
    }

   
    browser.quit()
    return results

def mars_news(browser):
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    mars_news_soup = BeautifulSoup(html, 'html.parser')

    
    first_title = mars_news_soup.find('div', class_='content_title').text
    first_paragraph = mars_news_soup.find('div', class_='article_teaser_body').text
    return first_title, first_paragraph

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
    
 
    first_tweet = tweet_soup.find('p', class_='TweetTextSize').text
    return first_tweet
    
def mars_facts():
    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    df = tables[0]
    df.columns = ['Property', 'Value']
   
    df.set_index('Property', inplace=True)
    
 
    return df.to_html()
    
def mars_hemis(browser):
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    
    html = browser.html
    hemi_soup = BeautifulSoup(html, 'html.parser')

    hemi_strings = []
    links = hemi_soup.find_all('h3')
    
    for hemi in links:
        hemi_strings.append(hemi.text)

=
    hemisphere_image_urls = []

    
    for hemi in hemi_strings:
       
        hemi_dict = {}
        

        browser.click_link_by_partial_text(hemi)
        
        hemi_dict["img_url"] = browser.find_by_text('Sample')['href']
        
        
        hemi_dict["title"] = hemi
        
 
        hemisphere_image_urls.append(hemi_dict)
    
        pprint(hemisphere_image_urls)
    
       
        browser.click_link_by_partial_text('Back')
    
    return hemisphere_image_urls