from tkinter.ttk import Progressbar
from turtle import color
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import pandas as pd
from geopy.geocoders import Nominatim
import geocoder
import re
import time
from tkinter import *

products = []
prices = []
ratings =[]
stores =[]

def set_up(product):

    product.replace(" ", "+")

    #URL OF THE WEBSITES
    url_walmart = f'https://www.walmart.com/search?q={product}&sort=price_low'
    url_target = f'https://www.target.com/s?searchTerm={product}&sortBy=PriceLow&moveTo=product-list-grid'
    url_costco = f'https://www.costco.com/CatalogSearch?keyword={product}&dept=All&sortBy=item_location_pricing_salePrice+asc'
    url_walgreens = f'https://www.walgreens.com/search/results.jsp?Ntt={product}&Ns=Final_Price&Nso=1'

    #SETTING UP THE SELENIUM DRIVER 
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')

    # this will disable image loading
    options.add_experimental_option(
    "prefs", {"profile.managed_default_content_settings.images": 2}
)
    
    #my_location= geocoder.ip('me')
    #latitude= my_location.geojson['features'][0]['properties']['lat']
    #longitude = my_location.geojson['features'][0]['properties']['lng']

    latitude = 36.169941
    longitude = -115.139832

    #SELECT THE LOCATION OF YOUR CHROME DRIVER
    browser = webdriver.Chrome('/Users/zaramarks/Desktop/Zara/prog/drivers/chromedriver', chrome_options=options)

   # browser.execute_cdp_cmd("Emulation.setGeolocationOverride", {
    #        "latitude": latitude,
    #        "longitude": longitude,
    #        "accuracy": 100
    #})
    if (walgreensVar.get()) == 1 :
        walgreens(browser, url_walgreens)
    if (costcoVar.get()) == 1:
        costco(browser, url_costco)
    if (walmartVar.get()) == 1:
        walmart(browser, url_walmart)
   

    df = pd.DataFrame({'Product Name':products,'Price':prices,'Rating':ratings, 'Store':stores}).sort_values(by=['Price'])

    print(df)

def walmart(browser, url_walmart):

    # 87% OF THE TIME 17 seconds
    browser.get(url_walmart)

    # 2 seconds
    soap = BeautifulSoup(browser.page_source, 'lxml')
    transformWalmart(soap)



def costco(browser, url_costco):
    browser.get(url_costco)
    soap = BeautifulSoup(browser.page_source, 'lxml')
    transformCostco(soap)

def walgreens(browser, url_walgreens):
    browser.get(url_walgreens)
    soap = BeautifulSoup(browser.page_source, 'lxml')
    transformWalgreens(soap)



def transformWalmart(soap):
   
    #Walmart redering
    #print(soap.find_all('a', class_ = 'absolute w-100 h-100 z-1 hide-sibling-opacity', limit =1)[0].find_all('span', limit=1)[0].text)
    #products.append(soap.find_all('a', class_ = 'absolute w-100 h-100 z-1 hide-sibling-opacity', limit =1)[0].find('span', class_ = 'w_Be').string)
    products.append(soap.find_all('a', class_ = 'absolute w-100 h-100 z-1 hide-sibling-opacity', limit =1)[0].find_all('span', limit=1)[0].text)
    prices.append( soap.find('div', class_='mr1 mr2-xl lh-copy b black f5 f4-l').string.replace('$', ''))
    ratings.append(soap.find('div', class_= 'flex items-center mt2').find('span', string = re.compile('Stars')).string)
    stores.append('Walmart')

    #df = pd.DataFrame({'Product Name':products,'Price':prices,'Rating':ratings, 'Store':stores})

    #return print(df)

def transformCostco(soap):

    products.append(soap.find('span', class_ = 'description').find('a').string.replace('\t', '').replace('\n', ''))
    prices.append(re.sub(r'[\t\n]', "", soap.find('div', class_= 'price').string.replace('$', '')))
    ratings.append(soap.find('div', class_='stars').find('span', class_ = 'offscreen').text.replace('\t', '').replace('\n', ''))
    stores.append('Costco')

    #df = pd.DataFrame({'Product Name':products,'Price':prices,'Rating':ratings, 'Store':stores})

    #return print(df)

def transformWalgreens(soap):

    a = soap.find('a', class_='color__text-black')
    print(a.find('div', class_ = 'brand').string +' '+a.find('strong', class_= 'description').string + a.find('span', class_='amount').text)
    products.append(a.find('div', class_ = 'brand').string +' '+a.find('strong', class_= 'description').string + ' ' + a.find('span', class_='amount').text)
    prices.append(a.find('span', class_='sr-only').text.replace('$', ''))
    ratings.append(a.find('img', alt=True)['alt'])
    stores.append('Walgreens')


#c = set_up('shampoo')

root = Tk()

root.title("Welcome to cheapest products!")

lbl = Label(root, text = "Choose a product")
lbl.grid(column =1, row =1)

txt = Entry(root, width=10)
txt.grid(column =2, row =1)


walgreensVar = IntVar()
costcoVar = IntVar()
walmartVar = IntVar()

buttonWalgreens = Checkbutton(root, text = "Walgreens", 
                      variable = walgreensVar,
                      onvalue = 1,
                      offvalue = 0,
                      height = 2,
                      width = 10)

buttonCostco = Checkbutton(root, text = "Costco", 
                      variable = costcoVar,
                      onvalue = 1,
                      offvalue = 0,
                      height = 2,
                      width = 10)

buttonWalmart = Checkbutton(root, text = "Walmart", 
                      variable = walmartVar,
                      onvalue = 1,
                      offvalue = 0,
                      height = 2,
                      width = 10)

buttonWalmart.grid(column =1, row =2)
buttonCostco.grid(column =2, row =2)
buttonWalgreens.grid(column =3, row =2)


pb = Progressbar(
    root,
    orient='horizontal',
    mode='indeterminate',
    length=280
)
# place the progressbar
#pb.grid(column=3, row=1, padx=10, pady=20)




def clicked():
    set_up(txt.get())
    

btn = Button(root, text = "Search" ,
             fg = "black", command=lambda: [set_up(txt.get())])
# Set Button Grid
btn.grid(column=3, row=1)



root.mainloop()

