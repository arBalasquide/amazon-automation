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

ACCEPT_SHOP = 'Amazon'
LIMIT_VALUE = 320      # Max price


def l(str):
    print("%s : %s"%(datetime.now().strftime("%Y/%m/%d %H:%M:%S"),str))

if __name__ == '__main__':
    PURCHASED = False

    # Boot up the browser
    try:
        b = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, options=options)
        b.get(ITEM_URL)
    except:
        l('Failed to open browser.')
        exit()

    while True and not PURCHASED:
        while True:
            try:
                # Confirm seller
                #shop = b.find_element_by_id('merchant-info').text
                #shop = shop.split('Ships from and sold by ')[1] # may not work for other shops

                #if ACCEPT_SHOP not in shop:
                #    l("NOT IN AMAZON")
                #    time.sleep(60)
                #    b.refresh()
                #    continue

                # Add to cart
                b.find_element_by_id('add-to-cart-button-ubb').click()
                break
            except:
                l('EXCEPTION OCCURED.')
                time.sleep(60)
                b.get(ITEM_URL)

        # Go to cart and checkout
        b.get('https://www.amazon.com/gp/cart/view.html/ref=nav_cart')
        b.find_element_by_name('proceedToRetailCheckout').click()

        # Purchase re-log in verification
        try:
            b.find_element_by_id('ap_password').send_keys(LOGIN_PASSWORD)
            b.find_element_by_id('signInSubmit').click()
        except:
            l('LOGIN PASS.')
            pass

        # Confirm price is not too high
        try:
            p = b.find_element_by_css_selector('td.grand-total-price').text
            if int(p.replace('$', '').split('.')[0]) > LIMIT_VALUE:
                l('PRICE IS TOO LARGE. CURRENT PRICE IS', p)
                continue
        except:
            l('EXCEPTION OCCURED. POSSIBLY ADDRESS PROBLEMS.')
            continue

        # Accept the order
        else:
            b.find_element_by_name('placeYourOrder1').click()
            PURCHASED = True
        break
    l('ITEM PURCHASED')
