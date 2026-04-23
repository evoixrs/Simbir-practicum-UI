import re
from decimal import Decimal

from selenium.webdriver.common.by import By

from locators.cart_page_locators import CartPageLocators
from pages.base_page import BasePage


class CartPage(BasePage):
    def get_rows(self):
        return self.find_elements(CartPageLocators.CART_ROWS)

    def get_rows_count(self):
        return len(self.get_rows())

    def get_row_name(self, row):
        return row.find_element(By.CSS_SELECTOR, "td:nth-child(2) a").text.strip()

    def get_row_quantity(self, row):
        return int(row.find_element(By.CSS_SELECTOR, "input[name^='quantity']").get_attribute("value"))

    def get_row_total(self, row):
        return self._parse_price(row.find_elements(By.CSS_SELECTOR, "td.align_right")[-1].text)

    def get_row_totals(self):
        return [self.get_row_total(row) for row in self.get_rows()]

    def get_sub_total(self):
        return self._parse_price(self.get_text(CartPageLocators.SUB_TOTAL))

    def get_cart_total(self):
        return self._parse_price(self.get_text(CartPageLocators.CART_TOTAL))

    def get_cheapest_row_index(self):
        totals = self.get_row_totals()
        return totals.index(min(totals))

    def set_row_quantity(self, index, quantity):
        quantity_input = self.get_rows()[index].find_element(By.CSS_SELECTOR, "input[name^='quantity']")
        quantity_input.clear()
        quantity_input.send_keys(str(quantity))

    def update_cart(self):
        self.click(CartPageLocators.UPDATE_BTN)
        self.wait_for_visible(CartPageLocators.CART_ROWS)

    @staticmethod
    def _parse_price(price_text):
        price = re.search(r"\$([\d,.]+)", price_text)
        return Decimal(price.group(1).replace(",", ""))
