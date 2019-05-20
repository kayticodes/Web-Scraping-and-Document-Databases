
from bs4 import BeautifulSoup as bs
from splinter import Browser 

#Create a path to open a chrome window
def scrape():

    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    mars_document = {}

    url = 'https://mars.nasa.gov/news'
    browser.visit(url)
    soup = bs(browser.html, 'html.parser')
    mars_document["news_title"] = soup.find('div', class_ ="content_title").get_text() 
    mars_document["news_paragraph"] = soup.find('div', class_='article_teaser_body').get_text()

    url_img ='https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url_img)
    featured_image_html = browser.html
    img_Butn = browser.find_by_xpath('//*[@id="full_image"]')
    img_Butn.click()
    browser.is_element_not_present_by_xpath('//*[@id="fancybox-lock"]/div/div[2]/div/div[1]/a[2]')
    more_button = browser.find_by_xpath('//*[@id="fancybox-lock"]/div/div[2]/div/div[1]/a[2]')
    more_button.click()
    featured_img_url = browser.find_by_xpath('//*[@id="page"]/section[1]/div/article/figure/a')['href']
    mars_document["Featured_Image"] = featured_img_url

    url_twit = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url_twit)
    weather_html= browser.html
    soup = bs(weather_html, 'html.parser')
    tweet = soup.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')
    mars_document["mars_weather"] = tweet.text
   
    hemisperes_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemisperes_url)
    hemisperes_html = browser.html
    soup = bs(hemisperes_html, 'html.parser')
    items = soup.find_all('div', class_= 'item')
    hemisperes_img_urls=[]
    hemisperes_main_url = 'https://astrogeology.usgs.gov'
    for item in items:
        title = item.find('h3').text
        #Gather the link that will take us to the full image
        partial_img_url = item.find('a', class_='itemLink product-item')['href']
        #Visit the page with the full image using the main url and the partial url 
        browser.visit(hemisperes_main_url + partial_img_url)
        #Save html object for the mars information page 
        partial_img_url = browser.html 
        #Parse html since we're now on a new page
        soup = bs(partial_img_url, 'html.parser')
        #Save the image url source
        img_url = hemisperes_main_url + soup.find('img', class_ = 'wide-image')['src']
        #Put all our gathered information as a dictionary into the empty list we made earlier 
        hemisperes_img_urls.append({'title':title, 'img_url':img_url})
    mars_document["hemisperes_urls"] = hemisperes_img_urls

    return mars_document
