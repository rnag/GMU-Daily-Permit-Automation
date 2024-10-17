import re
import time
from pathlib import Path
from typing import Annotated, Literal

import toml

import typer
from typer.core import TyperGroup

from dataclasses import dataclass, fields
from datetime import date
from random import randint, uniform

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from rich.console import Console
from rich.prompt import Confirm, Prompt
from rich.table import Table

from .utils import next_day, Day, get_full_name


class AliasGroup(TyperGroup):

    _CMD_SPLIT_P = re.compile(r" ?[,|] ?")

    def get_command(self, ctx, cmd_name):
        cmd_name = self._group_cmd_name(cmd_name)
        return super().get_command(ctx, cmd_name)

    def _group_cmd_name(self, default_name):
        for cmd in self.commands.values():
            name = cmd.name
            if name and default_name in self._CMD_SPLIT_P.split(name):
                return name
        return default_name


app = typer.Typer(cls=AliasGroup)

console = Console()


APP_NAME = __name__.split('.', 1)[0].replace('_', '-')

APP_DIR = Path(typer.get_app_dir(APP_NAME))
APP_DIR.mkdir(parents=True, exist_ok=True)

CONFIG_FILE_PATH: Path = APP_DIR / "config.toml"


class MaskedPassword(str):
    """Mask value but show the last 4 digits"""
    def __repr__(self):
        return f'***{self[-2:]} ({len(self)})'

    def mask(self):
        return repr(self).strip(" '")


class MaskedExceptLast4Chars(str):
    """Mask value but show the last 4 digits"""
    def __repr__(self):
        # Credits: https://stackoverflow.com/a/79092406/10237506
        return f"'{self[-4:]:*>{len(self)}}'"

    def mask(self):
        return repr(self).strip(" '")


_FULL_NAME = get_full_name()
_DEFAULT_NET_ID = (_FULL_NAME[0] + _FULL_NAME.rsplit(' ', 1)[-1]).lower()


def _get_value(value, mask_value=True):
    if mask_value:
        return repr(value).strip(" '")

    return value if isinstance(value, str) else str(value)



@dataclass
class Config:
    user: Annotated[str, 'Mason NetID'] = _DEFAULT_NET_ID
    password: Annotated[MaskedPassword, 'Password'] = MaskedPassword('TODO')
    parking_date: Annotated[str, 'Parking Date'] = 'Monday'
    card_type: Annotated[Literal['Visa', 'Mastercard'], 'Type'] = 'Visa'
    cardholder: Annotated[str, 'Name on Card'] = _FULL_NAME
    card_num: Annotated[MaskedExceptLast4Chars, 'Number'] = MaskedExceptLast4Chars('1234 5678 9012 3456')
    card_cvv: Annotated[str, 'Security Code'] = '123'
    card_expiry_month: Annotated[int, 'Expiration Month'] = 1
    card_expiry_year: Annotated[int, 'Expiration Year'] = 2050
    phone: Annotated[MaskedExceptLast4Chars, 'Phone'] = MaskedExceptLast4Chars('1234567890')
    dry_run: Annotated[bool, 'Dry Run'] = False

    def to_dict(self):
        return {
            "credentials": {
                "user": self.user,
                "password": str(self.password),
            },
            "parking": {
                "date": self.parking_date,
            },
            "credit_card": {
                "type": self.card_type,
                "name": self.cardholder,
                "number": str(self.card_num),
                "cvv": self.card_cvv,
                "expiry_month": self.card_expiry_month,
                "expiry_year": self.card_expiry_year,
            },
            "contact": {
                "phone": str(self.phone),
            },
            # "dry_run": self.dry_run,
        }

    @classmethod
    def load(cls):
        # Load the TOML configuration file
        if CONFIG_FILE_PATH.is_file():
            with CONFIG_FILE_PATH.open() as f:
                data = toml.load(f)
                # return Config.from_dict(data)

            parking_date = data['parking']['date']

            return cls(
                user=(credentials := data['credentials'])['user'],
                password=MaskedPassword(credentials['password']),
                parking_date=parking_date,
                card_type=(card := data['credit_card'])['type'],
                cardholder=card['name'],
                card_num=MaskedExceptLast4Chars(card['number'].replace(' ', '')),
                card_cvv=card['cvv'],
                card_expiry_month=card['expiry_month'],
                card_expiry_year=card['expiry_year'],
                phone=MaskedExceptLast4Chars(data['contact']['phone']),
            )

        return Config()


    def title(self):
        parking_date = self.parking_date
        try:
            day = Day.fromstr(parking_date)
        except KeyError:
            pass
        else:
            parking_date = next_day(date.today(), day).strftime('%B %d')

        return parking_date

    def print_table(self, mask_values=True):

        table = Table(title="Config", padding=(0, 0))
        table.add_column("General")
        table.add_column("Card")

        st = Table(
            padding=(0, 1),
            show_edge=False,
            show_lines=True,
            show_header=False,
        )

        st.add_column(style="cyan")
        st.add_column(style="green")

        # st.add_column("C")
        # st.add_column("D")

        tt = Table(
            padding=(0, 1),
            show_edge=False,
            show_lines=False,
            show_header=False,
        )

        tt.add_column(style="cyan")
        tt.add_column(style="green")

        # table = Table(title="Config")

        # table.add_column("Name", justify="right", style="cyan", no_wrap=True)
        # table.add_column("Value", justify="right", style="green")
        #
        # table2 = Table(title="Card")
        # table2.add_column("Name", justify="right", style="cyan", no_wrap=True)
        # table2.add_column("Value", justify="right", style="green")

        for f in fields(Config):
            if f.repr:
                value = getattr(self, f.name)
                if f.name.startswith('card'):
                    tt.add_row(f.type.__metadata__[0], _get_value(value, mask_values))
                else:
                    if f.name == 'parking_date':
                        value = self.title()
                    st.add_row(f.type.__metadata__[0], _get_value(value, mask_values))

        table.add_row(st, tt)

        # table.add_row(table2)
        console.print(table)


# def load_config() -> Config:
#     if CONFIG_FILE_PATH.is_file():
#         with CONFIG_FILE_PATH.open() as f:
#             data = toml.load(f)
#             return Config.from_dict(data)
#     return Config()


def save_config(config: Config):
    with CONFIG_FILE_PATH.open('w') as f:
        toml.dump(config.to_dict(), f)


options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
options.add_argument('--start-fullscreen')


def configure_sensitive_field(current_value, prompt_message, mask_type, password=False):
    # Show the masked value while allowing the user to input a new one
    masked_value = current_value.mask()
    new_value = Prompt.ask(prompt_message, default=masked_value if current_value != 'TODO' else None, password=password)

    # If user enters the masked default, return the original value
    if new_value == masked_value:
        return current_value

    # Otherwise, return a new instance of the mask type
    return mask_type(new_value)


@app.command("c | configure")
def configure():
    """
    Prompts the user for configuration values and updates the TOML file.
    """
    config = Config.load()

    # Prompt the user for each value, using existing values as defaults.
    config.user = Prompt.ask("Enter your Mason NetID", default=config.user)
    config.password = configure_sensitive_field(config.password, "Enter your password (input hidden)",
                                                MaskedPassword, password=True)
    config.parking_date = Prompt.ask("Enter the parking date (ex. `Tuesday` or `January 5`)",
                                     default=config.parking_date)
    config.card_type = Prompt.ask("Enter your card type", default=config.card_type, choices=['Visa', 'Mastercard'])
    config.cardholder = Prompt.ask("Enter the name on the card", default=config.cardholder)
    config.card_num = configure_sensitive_field(config.card_num, "Enter your card number", MaskedExceptLast4Chars)
    config.card_cvv = Prompt.ask("Enter your CVV or security code (input hidden)",
                                 default=config.card_cvv, password=True)
    config.card_expiry_month = Prompt.ask("Enter your card's expiration month", default=str(config.card_expiry_month))
    config.card_expiry_year = Prompt.ask("Enter your card's expiration year", default=str(config.card_expiry_year))
    config.phone = configure_sensitive_field(config.phone, "Enter your phone number", MaskedExceptLast4Chars)

    # config.dry_run = Confirm.ask("Enable dry run mode?", default=config.dry_run)

    # Save the updated config back to the TOML file.
    save_config(config)
    console.print("Configuration saved successfully.", style="bold green")


def print_path(path):
    parts = path.parts
    colored_parts = []

    for part in parts:
        if part == '/':
            colored_parts.append('')
        else:
            if " " in part:
                colored_parts.append(f"[blue]{part}[/]")
            else:
                colored_parts.append(f"[magenta]{part}[/]")

    console.print("/".join(colored_parts))


@app.command('sc | show-config')
def show_config(mask_values: bool = False):
    """Show the config file."""
    console.print(f'File Path: ', end='')
    print_path(CONFIG_FILE_PATH)
    print()

    if CONFIG_FILE_PATH.is_file():
        config = Config.load()
        config.print_table(mask_values=mask_values)

        if Confirm.ask("Launch config?"):
            console.print("Opening config file...", style='bold yellow')
            typer.launch(str(CONFIG_FILE_PATH), locate=True)

    else:
        console.print("Config file doesn't exist yet! Use [bold green]c | configure[/] to set it up.", style='bold red')


@app.command('dp | daily-permit')
def daily_permit(dry_run: bool = False):
    """Purchase a Daily (Parking) Permit for the GMU Campus."""
    config = Config.load()
    config.dry_run = dry_run

    config.print_table()
    console.print()

    if not Confirm.ask('Looks good?'):
        print()
        console.print('Use [bold green]c | configure[/] to get started.')
        exit(0)

    # Using Chrome to access web
    # driver = webdriver.Chrome()

    # Creating a driver instance with the previous capabilities
    driver = webdriver.Chrome(options)

    wait = WebDriverWait(driver, 60)  # Wait for a maximum of 60 seconds

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

    if driver.find_elements(By.XPATH, '//span[text()="A previous basket in payment pending status was found.'
                                      '  You have been assigned to this basket."]'):
        basket = driver.find_element(By.ID, 'basketText')
        basket.click()
        driver.save_screenshot('cart.png')

        driver.get('https://gmu.t2hosted.com/crt/view.aspx')

    else:
        check = driver.find_element(By.NAME, 'terms')
        check.click()

        btn = driver.find_element(By.CSS_SELECTOR, '[value="Next >>"]')
        btn.click()

        label = driver.find_element(By.XPATH, '//label[text()="Evening General Permit '
                                              '(only valid from 4:00pm-11:59pm)"]')
        radio_id = label.get_attribute('for')
        radio = driver.find_element(By.ID, radio_id)
        radio.click()

        label = driver.find_element(By.XPATH, '//label[text()="I have read and understand the '
                                              'rules & regulations associated with the chosen permit."]')
        check_id = label.get_attribute('for')
        check = driver.find_element(By.ID, check_id)
        check.click()

        btn = driver.find_element(By.CSS_SELECTOR, '[value="Next >>"]')
        btn.click()

        # Select Start Date
        driver.save_screenshot('sdate.png')

        date_link = driver.find_element(By.CSS_SELECTOR, f'[title="{config.title()}"]')
        date_link.click()

        btn = driver.find_element(By.CSS_SELECTOR, '[value="Next >>"]')
        btn.click()

        # Select your Vehicles for Permit
        check = driver.find_element(By.NAME, 'terms')
        check.click()

        check = driver.find_element(By.XPATH, ".//table[@summary='This table shows "
                                              "a list of vehicles.']/tbody/tr[2]/td[1]/input")
        check.click()

        btn = driver.find_element(By.CSS_SELECTOR, '[value="Next >>"]')
        btn.click()

        # Summary

        driver.save_screenshot('summary.png')

        if dry_run:
            raise typer.Exit()

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
    credit_card_type.send_keys(config.card_type)  # Visa or Mastercard

    card_number = driver.find_element(By.ID, 'creditCardPaymentAccountNumber')
    card_number.send_keys(config.card_num)

    cvv = driver.find_element(By.ID, 'creditCardPaymentCVV2')
    cvv.send_keys(config.card_cvv)

    s = randint(1, 3)
    # s = randint(2, 5)
    time.sleep(s)

    card_month = driver.find_element(By.ID, 'creditCardPaymentExpirationMonthSelect')

    card_month.send_keys(str(config.card_expiry_month).zfill(2))

    s = uniform(0.5, 2)
    time.sleep(s)

    card_year = driver.find_element(By.ID, 'creditCardPaymentExpirationYearSelect')
    card_year.send_keys(str(config.card_expiry_year))

    s = uniform(0.5, 2)
    time.sleep(s)

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


def main():
    app()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()