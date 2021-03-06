import time
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv

load_dotenv()

CHROMEDRIVER_PATH = '/bin/chromedriver'

options = Options()
options.add_argument("user-data-dir=./profile") # to bypass OTP verification

LOGIN_PASSWORD = os.getenv("LOGIN_PASSWORD")

ITEM_URL = 'https://www.amazon.com/dp/B07VGRJDFY/' # Product URL
CART_URL = 'https://www.amazon.com/gp/cart/view.html/ref=nav_cart'

ACCEPT_SHOP = 'Amazon'
LIMIT_VALUE = 320      # Max price

TIME_OUT = 60 # How often you want to check for changes

def l(str):
    print("%s : %s"%(datetime.now().strftime("%Y/%m/%d %H:%M:%S"),str))

if __name__ == '__main__':
    PURCHASED = False
    EMPTY_CART = True
    # Boot up the browser
    try:
        b = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, options=options)
        b.get(ITEM_URL)
    except:
        l('Failed to open browser.')
        exit()
    
    while True and not PURCHASED:
        # Clear cart, so only 1 desired item is there
        while not EMPTY_CART:
            try:
                b.get(CART_URL)
                b.find_element_by_xpath("/html/body/div[1]/div[4]/div[1]/div[5]/div/div[2]/div[4]/form/div[2]/div[3]/div[4]/div/div[1]/div/div/div[2]/div/div/div[2]/div[1]/span[2]/span/input").click()
            except:
                EMPTY_CART = True
                b.get(ITEM_URL)
        while True:
            try:
                # Confirm seller - Uncomment if you care about store
                #shop = b.find_element_by_id('merchant-info').text
                #shop = shop.split('Ships from and sold by ')[1] # may not work for other shops

                #if ACCEPT_SHOP not in shop:
                #    l("NOT IN AMAZON")
                #    time.sleep(60)
                #    b.refresh()
                #    continue

                # Add to cart
                b.find_element_by_id('add-to-cart-button-ubb').click()
                EMPTY_CART = False
                break
            except:
                l('EXCEPTION OCCURED.')
                time.sleep(TIME_OUT)
                b.get(ITEM_URL)

        # Go to cart and checkout
        b.get(CART_URL)
        try: 
            b.find_element_by_name('proceedToRetailCheckout').click()
        except:
            l('CHECKOUT BUTTON NOT FOUND')
            continue

        # Purchase re-log in verification
        try:
            b.find_element_by_id('ap_password').send_keys(LOGIN_PASSWORD)
            b.find_element_by_id('signInSubmit').click()
        except:
            l('POSSIBLE LOGIN PROBLEMS.')
            pass

        # Confirm price is not too high
        try:
            p = b.find_element_by_css_selector('td.grand-total-price').text
            if int(p.replace('$', '').replace(',', '').split('.')[0]) > LIMIT_VALUE:
                l('PRICE IS TOO LARGE. CURRENT PRICE IS: ' + p)
                time.sleep(TIME_OUT)
                continue
        except:
            l('EXCEPTION OCCURED. POSSIBLY ADDRESS PROBLEMS.')
            time.sleep(TIME_OUT)
            b.get(ITEM_URL)
            continue

        # Accept the order
        else:
            b.find_element_by_name('placeYourOrder1').click()
            PURCHASED = True
        break
    l('ITEM PURCHASED')
