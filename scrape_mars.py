# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import datetime as dt

executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
browser = Browser("chrome", **executable_path, headless=False)

# Windows users
# executable_path = {'executable_path': 'chromedriver.exe'}
# browser = Browser('chrome', **executable_path, headless=False)

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
def scrape_mars_weather (browser):
    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)
    html = browser.html
    weather_soup = bs(html, 'html.parser')
    mars_tweet = weather_soup.find("div", attrs={"class": "tweet", "data-name": "Mars Weather"})
    mars_weather = mars_tweet.find("p", "tweet-text").get_text()

    return mars_weather

# Scrape Mars facts
def mars_facts ():
    try:
        mars_df = pd.read_html("https://space-facts.com/mars/")[0]
    except BaseException:
            return None
    mars_df.columns=['Description', 'Values']

    return mars_df.to_html(classes="table table-striped")

# Scrape Mars hemispheres
def mars_hemispheres (browser):
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    hemisphere_image_url = []
    links = browser.find_by_css("a.product-item h3")
    for item in range(len(links)):
        hemisphere = {}
        browser.find_by_css("a.product-item h3")[item].click()
        sample_element = browser.find_link_by_text("Sample").first
        hemisphere["img_url"] = sample_element["href"]
        hemisphere["title"] = browser.find_by_css("h2.title").text
        hemisphere_image_url.append(hemisphere)
        browser.back()
    
    return hemisphere_image_url

def scrape_hemisphere (html_text):
    hemisphere_soup = bs(html_text, 'html.parser')
    try:
        title_element = hemisphere_soup.find("h2", class_="title").get_text()
        sample_element = hemisphere_soup.find("a", text="Sample").get("href")
    except AttributeError:
        title_element = None
        sample_element = None
    hemisphere = {
        "title": title_element,
        "img_url": sample_element
    }

    return hemisphere

# scrape everything
def scrape_all ():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    browser = Browser("chrome", **executable_path, headless=False)

    # Windows users
    # executable_path = {'executable_path': 'chromedriver.exe'}
    # browser = Browser('chrome', **executable_path, headless=False)

    news_title, news_paragraph = mars_news (browser)
    featured_img_url = featured_images (browser)
    mars_weather = scrape_mars_weather (browser)
    facts = mars_facts()
    hemisphere_image_url = mars_hemispheres (browser)
    timestamp = dt.datetime.now()

    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_img_url,
        "mars_weather": mars_weather,
        "mars_facts": facts,
        "hemispheres": hemisphere_image_url,
        "last_modified": timestamp
    }
    browser.quit()
    return data

if __name__ == "__main__":
    print(scrape_all())
