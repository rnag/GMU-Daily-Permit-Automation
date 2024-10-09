import time
from dataclasses import dataclass
from random import randint, uniform

import toml

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
options.add_argument('--start-fullscreen')

# Using Chrome to access web
#driver = webdriver.Chrome()

# Creating a driver instance with the previous capabilities
driver = webdriver.Chrome(options)


@dataclass
class Config:
    user: str
    password: str
    title: str
    card_type: str
    cardholder: str
    card_num: str
    card_cvv: str
    expiry_month: int
    expiry_year: int
    phone: str

    @classmethod
    def from_file(cls):
        # Load the TOML configuration file
        config_file = 'config.toml'
        _cfg = toml.load(config_file)

        return cls(
            user=(credentials := _cfg['credentials'])['user'],
            password=credentials['password'],
            title=_cfg['parking']['date'],
            card_type=(card := _cfg['credit_card'])['type'],
            cardholder=card['name'],
            card_num=card['number'],
            card_cvv=card['cvv'],
            expiry_month=card['expiry_month'],
            expiry_year=card['expiry_year'],
            phone=_cfg['contact']['phone'],
        )


config = Config.from_file()

wait = WebDriverWait(driver, 60)  # Wait for a maximum of 10 seconds


def main():

    driver.get('https://gmu.t2hosted.com/per/selectpermit.aspx')

    btn = driver.find_element(By.CSS_SELECTOR, '[value="Students & Faculty/Staff"]')
    btn.click()

    uname = driver.find_element(By.ID, 'username')
    pwd = driver.find_element(By.ID, 'password')

    uname.send_keys(config.user)
    pwd.send_keys(config.password)

    driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    # driver.implicitly_wait(5_000)

    # time.sleep(5)

    # "Trust This Device?"

    # <button id="dont-trust-browser-button" class="button--link link">No, other people use this device</button>
    wait.until(EC.visibility_of_element_located((By.ID, 'dont-trust-browser-button')))

    btn = driver.find_element(By.ID, 'dont-trust-browser-button')
    btn.click()

    # "Purchase a Permit"

    wait.until(EC.visibility_of_element_located((By.NAME, 'terms')))

    # basketText

    if driver.find_elements(By.XPATH, '//span[text()="A previous basket in payment pending status was found.  You have been assigned to this basket."]'):
        basket = driver.find_element(By.ID, 'basketText')
        basket.click()
        driver.save_screenshot('cart.png')

        driver.get('https://gmu.t2hosted.com/crt/view.aspx')

    else:
        check = driver.find_element(By.NAME, 'terms')
        check.click()

        btn = driver.find_element(By.CSS_SELECTOR, '[value="Next >>"]')
        btn.click()

        label = driver.find_element(By.XPATH, '//label[text()="Evening General Permit (only valid from 4:00pm-11:59pm)"]')
        radio_id = label.get_attribute('for')
        radio = driver.find_element(By.ID, radio_id)
        radio.click()

        label = driver.find_element(By.XPATH, '//label[text()="I have read and understand the rules & regulations associated with the chosen permit."]')
        check_id = label.get_attribute('for')
        check = driver.find_element(By.ID, check_id)
        check.click()

        btn = driver.find_element(By.CSS_SELECTOR, '[value="Next >>"]')
        btn.click()

        # Select Start Date
        driver.save_screenshot('sdate.png')

        date = driver.find_element(By.CSS_SELECTOR, f'[title="{config.title}"]')
        date.click()

        btn = driver.find_element(By.CSS_SELECTOR, '[value="Next >>"]')
        btn.click()

        # Select your Vehicles for Permit
        check = driver.find_element(By.NAME, 'terms')
        check.click()

        check = driver.find_element(By.XPATH, ".//table[@summary='This table shows a list of vehicles.']/tbody/tr[2]/td[1]/input")
        check.click()

        btn = driver.find_element(By.CSS_SELECTOR, '[value="Next >>"]')
        btn.click()

        # Summary

        driver.save_screenshot('summary.png')

        btn = driver.find_element(By.CSS_SELECTOR, '[value="Pay Now"]')
        btn.click()

    btn = driver.find_element(By.CSS_SELECTOR, '[value="Next >>"]')
    btn.click()

    # Payment Information

    wait.until(EC.visibility_of_element_located((By.XPATH, '//span[text()="Payment Information"]')))

    payment_method = driver.find_element(By.ID, 'pmtOptionsPaymentMethodTypeSelect')
    payment_method.send_keys('C')  # Credit Card
    payment_method.send_keys(Keys.RETURN)

    credit_card_type = driver.find_element(By.ID, 'creditCardPaymentCardTypeSelect')
    credit_card_type.send_keys(config.card_type) # Visa or Mastercard

    card_number = driver.find_element(By.ID, 'creditCardPaymentAccountNumber')
    card_number.send_keys(config.card_num.replace(' ', ''))

    cvv = driver.find_element(By.ID, 'creditCardPaymentCVV2')
    cvv.send_keys(config.card_cvv)

    s = randint(1, 3)
    # s = randint(2, 5)
    time.sleep(s)

    card_month = driver.find_element(By.ID, 'creditCardPaymentExpirationMonthSelect')

    card_month.send_keys(str(config.expiry_month).zfill(2))

    s = uniform(0.5, 2)
    time.sleep(s)

    card_year = driver.find_element(By.ID, 'creditCardPaymentExpirationYearSelect')
    card_year.send_keys(str(config.expiry_year))

    s = uniform(0.5, 2)
    time.sleep(s)

    # creditCardPaymentExpirationMonthSelect > 10
    # creditCardPaymentExpirationYearSelect > 2024
    name = driver.find_element(By.ID, 'creditCardPaymentNameOnCard')
    name.send_keys(config.cardholder)

    s = uniform(0.5, 2)
    time.sleep(s)

    mobile_phone = driver.find_element(By.ID, 'creditCardPaymentUserMobilePhone')
    mobile_phone.send_keys(config.phone)

    s = randint(1, 3)
    # s = randint(2, 5)
    time.sleep(s)

    btn = driver.find_element(By.ID, 'continueFromPayment')
    # driver.save_screenshot('before-confirm.png')
    btn.click()

    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[value="Logout"]')))
    # wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[value="<< Back"]')))

    driver.save_screenshot('confirm.png')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
