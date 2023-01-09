import argparse

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait


def send_message(driver: webdriver.Chrome, message: str):
    message_box = driver.find_element('css selector', 'textarea')
    message_box.send_keys(message)
    driver.find_element('css selector', 'textarea + button').click()


def login(driver: webdriver.Chrome, username: str, password: str):
    driver.find_element('id', 'username').send_keys(username)
    driver.find_element('id', 'password').send_keys(password)
    driver.find_element('class name', 'btn-submit').click()


def login_check(driver: webdriver.Chrome):
    return 'cas.finki.ukim.mk' in driver.current_url


def get_driver():
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    return driver


def parse_args():
    arg_parser = argparse.ArgumentParser(description='BBB Bot')

    arg_parser.add_argument('-l', type=str, required=True, help='Link')
    arg_parser.add_argument('-u', type=str, required=True, help='Username')
    arg_parser.add_argument('-p', type=str, required=True, help='Password')
    arg_parser.add_argument('-m', type=str, required=False, help='Message to send', default='123456')

    return arg_parser.parse_args()


def main():
    args = parse_args()
    driver = get_driver()

    driver.get(args.l)

    if login_check(driver):
        login(driver, args.u, args.p)
        driver.get(args.l)

    driver.find_element('id', 'join_button_input').click()

    WebDriverWait(driver, 5).until(ec.number_of_windows_to_be(2))
    driver.switch_to.window(driver.window_handles[1])

    WebDriverWait(driver, 5).until(ec.presence_of_element_located(('css selector', 'h1 + button')))
    driver.execute_script('document.querySelector("h1 + button").click()')
    print('Ready')

    send_message(driver, args.m)

    while True:
        try:
            _ = input()
        except KeyboardInterrupt:
            print('Exiting')
            break


if __name__ == '__main__':
    main()
