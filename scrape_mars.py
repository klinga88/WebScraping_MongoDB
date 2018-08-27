import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
import pymongo
from splinter import Browser
from selenium import webdriver
import os
import re
import time

project_path = os.path.join("C:/","Users","kling","UNCC - Homework for Data Analytics","WebScraping_MongoDB")
nasa_url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
twitter_url = "https://twitter.com/marswxreport?lang=en"
facts_url="https://space-facts.com/mars/"
usgs_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
db = client.mars_db
collection = db.articles




def scrape():
    #setup
    response = {}   
    
    executable_path = {'executable_path': os.path.join("C:/","Users","kling","UNCC Data Analytics","chromedriver.exe")}
    browser = Browser('chrome', **executable_path, headless=False)
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("--test-type") 
    browser = Browser('chrome', **executable_path, headless=False)
    #retrieve text news about mars
    browser.visit(nasa_url)
    #get first article and follow link
    article_link = browser.find_link_by_partial_href('/news/')[0].click()
    html = browser.html
    soup = bs(html, "html.parser")
    news_title = soup.find("title").text
    news_title = news_title.strip('\n')
    #Get all paragraphs from article, strip tags and add them together into one block of text
    news_p = soup.find_all("p")
    news_p = news_p[:-4]
    paragraph=""
    for i in range(len(news_p)):
        paragraph = paragraph + news_p[i].get_text(' ', strip=True)
    response['paragraph'] = paragraph

    #get featured image
    driver = webdriver.Chrome(chrome_options=options)
    driver.get(jpl_url)
    link = driver.find_element_by_partial_link_text("FULL IMAGE").click()
    time.sleep(2)
    images = driver.find_elements_by_class_name('fancybox-image')
    for image in images:
        image_url = image.get_attribute('src')
        print(image_url)

    respone['featured_img'] = image_url
    # img=requests.get(image_url)#fetch image
    # with open('featured_image.jpg','wb') as writer:#open for writing in binary mode
    #     writer.write(img.content)#write the image

    #Retrieve weather data
    driver = webdriver.Chrome(chrome_options=options)
    driver.get(twitter_url)
    tweet = driver.find_element_by_css_selector('p.tweet-text').text
    response['weather'] = tweet

    #Get Mars facts
    facts = pd.read_html(facts_url)[0]
    response['facts'] = facts

    return(response)
