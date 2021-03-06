import os
import re
import sys
from time import sleep

from selenium import webdriver

import login


class LotsBot():
    def __init__(self, driver: webdriver.Chrome) -> None:
        self.driver = driver

        self.added_skus = []

    def run(self, item_count: int) -> None:
        """parse individual items tab (https://beta.888lots.com/catalog)
        and add every item to the cart
        """

        print('running bot...')

        self.driver.refresh()
        
        table = self.driver.find_elements_by_xpath('//div[@class="row products_page"]/div/ul/li')

        for i in range(item_count):
            item = table[i]
            
            sku = re.search('[BX]\d.{8}', item.text)

            if not sku:
                print('sku not able to be found, continuing')
                continue
            
            sku = sku.group()

            if sku in self.added_skus:
                continue

            print('processing: SKU ' + sku)

            if 'not order it' in item.text:
                print(' ~ beep beep boop boop the item is already in someone\'s cart')

                continue

            if 'In your cart' in item.text:
                print(' ~ beep beep boop boop the item is already in your cart')

                self.added_skus.append(sku)

                continue

            buy_now = item.find_element_by_xpath('.//div[@class="cartbrnh"]/a')
            
            buy_now.click()

            sleep(1)

            add_to_cart = item.find_element_by_xpath('//button[contains(text(), "Add to cart")]')

            if not add_to_cart.is_displayed() or not add_to_cart.is_enabled():
                print(' ~ beep beep boop boop the item is already in someone\s cart')

                cancel = item.find_element_by_xpath('//button[contains(text(), "Cancel")]')

                cancel.click()

                continue

            add_to_cart.click()
            
            sleep(1)

            print(' ~ the item has been added to your cart')

            self.added_skus.append(sku)

            self.added_skus = self.added_skus[:item_count]

        print('finished running the bot')
        
    def run_loop(self, item_count: int) -> None:
        while True:
            #if not os.path.isfile('run'):
            #    print('run file does not exist, sleeping bot for 10 seconds...\n')
            #    
            #    sleep(10)

            try:
                self.run(item_count)
            except Exception as e:
                print(e)
                print(' ~ beep beep boop boop there was an error')
                print(' ~ unsure of how to handle this error, so restarting...')


def main() -> None:
    options = webdriver.ChromeOptions()

    if '--debug' not in sys.argv:
        options.add_argument('headless')

    driver = webdriver.Chrome(options=options)
    
    driver.implicitly_wait(10)

    driver.get('https://888lots.com/')

    login_prompt = driver.find_element_by_xpath('//*[contains(text(), "Login")]')

    login_prompt.click()

    sleep(1)

    email = driver.find_element_by_xpath('//form/div/input[@name="email"]')
    password = driver.find_element_by_xpath('//input[@name="password"]')

    def send_keys_slow(elem: webdriver.remote.webelement.WebElement, text: str) -> None:
        for c in text:
            elem.send_keys(c)

            sleep(.05)

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

    count = 20

    if len(sys.argv) > 1:
        count = int(sys.argv[len(sys.argv) - 1])

    bot.run_loop(count)


if __name__ == '__main__':
    main()
