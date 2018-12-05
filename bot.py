from time import sleep

from selenium import webdriver

import login


def send_keys_slow(elem, text):
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


if __name__ == '__main__':
    main()
