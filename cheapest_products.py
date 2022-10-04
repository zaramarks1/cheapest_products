from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import pandas as pd

products = []
prices = []
ratings =[]
stores =[]

def set_up(product):

    url_walmart = f'https://www.walmart.com/search?q={product}'

    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')

    options.add_experimental_option(
    # this will disable image loading
    "prefs", {"profile.managed_default_content_settings.images": 2}
)


    browser = webdriver.Chrome('/Users/zaramarks/Desktop/Zara/prog/drivers/chromedriver', chrome_options=options)

    browser.get(url_walmart)

    soap = BeautifulSoup(browser.page_source, 'lxml')

    return soap

def extract_target(product):

    url_target = f'https://www.target.com/s?searchTerm={product}&sortBy=PriceLow&moveTo=product-list-grid'

    url_walmart = 'https://www.walmart.com/search?q=pencil'

    response = requests.get(url_walmart)

    soap = BeautifulSoup(response.text, 'lxml')
    return soap

def transform(soap):
   
    products.append(soap.find_all('a', class_ = 'absolute w-100 h-100 z-1 hide-sibling-opacity', limit=1)[0].find('span', class_ = 'w_Be').string)
    prices.append( soap.find('div', class_='mr1 mr2-xl lh-copy b black f5 f4-l').string)
    ratings.append(soap.find('div', class_= 'flex items-center mt2').find('span', class_='w_Be').string)
    stores.append('Walmart')

    df = pd.DataFrame({'Product Name':products,'Price':prices,'Rating':ratings, 'Store':stores})

    return print(df)


c = set_up('pencil+sharpener')
transform(c)
