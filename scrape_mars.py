# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as import pd
import datetime as dt

executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
browser = Browser("chrome", **executable_path, headless=False)

# scrape news
def mars_news (browser):
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=0.5)
    html = browser.html
    mars_news = bs(html, 'html.parser')

    try:
        slide_element = mars_news.select_one("ul.item_list li.slide")
        slide_element.find("div", class_="content_title")
        news_title = slide_element.find("div", class_="content_title").get_text()
        news_paragraph = slide_element.find("div", class_="article_teaser_body").get_text()
    except AttributeError:
        return None, None
    return news_title, news_paragraph

# scrape images
def featured_images (browser):
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    full_image_button = browser.find_by_id("full_image")
    full_image_button.click()
    browser.is_element_present_by_text("more info", wait_time=1)
    more_info_element = browser.find_link_by_partial_text("more info")
    more_info_element.click()
    html = browser.html
    image_soup = bs(html, 'html.parser')
    featured_img = image_soup.select_one("figure.lede a img")
    try:
        featured_img_url = featured_img.get("src")
    except AttributeError:
        return None
    featured_img_url = f"https://www.jpl.nasa.gov{featured_img_url}"
    return featured_img_url

# Scrape Mars Weather from Twitter
def mars_weather (browser):
    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)
    html = browser.html
    weather_soup = bs(html, 'html.parser'
    mars_tweet = weather_soup.find("div", attrs={"class": "tweet", "data-name": "Mars Weather"})
    mars_weather = mars_tweet.find("p", "tweet-text").get_text()

    return mars_weather


