import os
import re
from time import sleep

from selenium import webdriver

import login


class LotsBot():
    def __init__(self, driver: webdriver.Chrome) -> None:
        self.driver = driver

        self.seen_items = []

    def run(self, item_count: int) -> None:
        """parse individual items tab (https://beta.888lots.com/catalog)
        and add every item to the cart
        """

        self.driver.refresh()
        
        # scroll to bottom of page to load more items
        #try:
        #    self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        
        #    sleep(10)
        #except:
        #    pass
        
        table = self.driver.find_elements_by_xpath('//div[@class="row products_page"]/div/ul/li')

        for i in range(item_count):
            item = table[i]

            sku = re.search('B\d.{8}', item.text).group()

            if sku in self.seen_items:
                continue

            print('processing: SKU ' + sku)

            #if item contains div with class containing 'alert':

            if 'not order it' in item.text:
                print(' ~ beep beep boop boop the item is already in someone\'s cart')

                continue

            #buy_now =
            
            #buy_now.click()
            
            #add_to_cart =

            #add_to_cart.click()

            self.seen_items.append(sku)
        
        # check for runtime, optimize so it does not run constantly but fast enough


    def run_loop(self, item_count: int=20) -> None:
        while True:
            if not os.path.isfile('run'):
                print('run file does not exist, sleeping bot for 10 seconds...')
                
                sleep(10)
            
            self.run(item_count)

            sleep(10)


def send_keys_slow(elem: webdriver.remote.webelement.WebElement, text: str) -> None:
    for c in text:
        elem.send_keys(c)

        sleep(.05)


def main() -> None:
    options = webdriver.ChromeOptions()

    #options.add_argument('headless')

    driver = webdriver.Chrome(options=options)
    
    driver.implicitly_wait(10)

    driver.get('https://888lots.com/')

    login_prompt = driver.find_element_by_xpath('//*[contains(text(), "Login")]')

    login_prompt.click()

    sleep(1)

    email = driver.find_element_by_xpath('//form/div/input[@name="email"]')
    password = driver.find_element_by_xpath('//input[@name="password"]')

    send_keys_slow(email, login.email)
    send_keys_slow(password, login.password)

    sleep(1)

    login_button = driver.find_element_by_xpath('//button[contains(text(), "Login")]')

    login_button.click()

    end_tour = driver.find_element_by_xpath('//button[contains(text(), "End tour")]')

    if end_tour:
        end_tour.click()

    driver.get('https://beta.888lots.com/catalog')
    
    bot = LotsBot(driver)

    bot.run_loop()


if __name__ == '__main__':
    main()
