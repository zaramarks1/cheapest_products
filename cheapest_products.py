from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import pandas as pd
from geopy.geocoders import Nominatim
import geocoder
import re

products = []
prices = []
ratings =[]
stores =[]

def set_up(product):

    #SET UP SELENIUM

    url_walmart = f'https://www.walmart.com/search?q={product}&sort=price_low'
    url_target = f'https://www.target.com/s?searchTerm={product}&sortBy=PriceLow&moveTo=product-list-grid'

    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')

    options.add_experimental_option(
    # this will disable image loading
    "prefs", {"profile.managed_default_content_settings.images": 2}
)

    my_location= geocoder.ip('me')
    latitude= my_location.geojson['features'][0]['properties']['lat']
    longitude = my_location.geojson['features'][0]['properties']['lng']

    # latitude = 36.169941
    # longitude = -115.139832

    print(latitude, longitude)

    browser = webdriver.Chrome('/Users/zaramarks/Desktop/Zara/prog/drivers/chromedriver', chrome_options=options)

  #  browser.execute_cdp_cmd("Emulation.setGeolocationOverride", {
   #         "latitude": latitude,
    #        "longitude": longitude,
    #        "accuracy": 100
   # })

    browser.get(url_walmart)

    soap = BeautifulSoup(browser.page_source, 'lxml')

    transform(soap)

    return soap

def transform(soap):
   
    #Walmart redering
    #products.append(soap.find_all('a', class_ = 'absolute w-100 h-100 z-1 hide-sibling-opacity', limit =1)[0].find('span', class_ = 'w_Be').string)
    products.append(soap.find_all('a', class_ = 'absolute w-100 h-100 z-1 hide-sibling-opacity', limit =1)[0].find('span').string)
    prices.append( soap.find('div', class_='mr1 mr2-xl lh-copy b black f5 f4-l').string.replace('$', ''))
    ratings.append(soap.find('div', class_= 'flex items-center mt2').find('span', string = re.compile('Stars')).string)
    stores.append('Walmart')

    df = pd.DataFrame({'Product Name':products,'Price':prices,'Rating':ratings, 'Store':stores})

    return print(df)


c = set_up('pencil+sharpener')

