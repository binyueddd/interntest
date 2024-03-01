import sys
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException


class CurrencyExchanger:
    def __init__(self):
        self.name_dict = {}
        # self.driver_path = driver_path

    def fetch_currency_names(self, url='https://www.11meigui.com/tools/currency'):
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            rows = soup.find_all('tr')

            for row in rows[3:]:
                cells = row.find_all('td')
                if len(cells) >= 5:
                    chinese_name = cells[1].text.strip()
                    standard_symbol = cells[4].text.strip()
                    self.name_dict[standard_symbol] = chinese_name
        else:
            print('Failed to retrieve currency names from the webpage')

    def get_exchange_rate(self, date, currency_code):
        currency_name = self.name_dict.get(currency_code)
        if currency_name is None:
            print(f"No currency found for code: {currency_code}")
            return

        driver = webdriver.Chrome(executable_path=self.driver_path)
        url = "https://www.boc.cn/sourcedb/whpj/"
        driver.get(url)

        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "pjname"))
            )

            currency_select = driver.find_element(By.ID, "pjname")
            for option in currency_select.find_elements(By.TAG_NAME, 'option'):
                print(option.text)
                if option.text == currency_name:
                    option.click()
                    break

            date_input = driver.find_element(By.ID, "erectDate")
            date_input.clear()
            date_input.send_keys(date)

            date_input = driver.find_element(By.ID, "nothing")
            date_input.clear()
            date_input.send_keys(date)

            search_buttons = driver.find_elements(By.CLASS_NAME, "search_btn")
            if len(search_buttons) > 1:
                search_buttons[1].click()
            else:
                print("Required search button not found.")

            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "BOC_main")))
            all_data = driver.find_element(By.CLASS_NAME, "BOC_main").text

            with open("result.txt", "w") as file:
                file.write(all_data)
            print("Data written to result.txt")

            exchange_rate = driver.find_element(By.XPATH,
                                                "//div[contains(@class, 'BOC_main')]//table/tbody/tr[2]/td[4]").text

            print(exchange_rate)

        except TimeoutException:
            print("Timeout occurred while loading the page or searching for the exchange rate.")
        finally:
            driver.quit()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 script.py YYYYMMDD CURRENCY_CODE")
        sys.exit(1)

    date = sys.argv[1]
    currency_code = sys.argv[2]

    exchanger = CurrencyExchanger()
    exchanger.fetch_currency_names()
    exchanger.get_exchange_rate(date, currency_code)
