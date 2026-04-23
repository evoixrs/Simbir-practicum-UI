import re
from decimal import Decimal

from selenium.webdriver.support.select import Select

from locators.category_page_locators import CategoryPageLocators
from pages.base_page import BasePage


class CategoryPage(BasePage):
    def get_title(self):
        return self.get_text(CategoryPageLocators.PAGE_TITLE)

    def get_products_count(self):
        return len(self.find_elements(CategoryPageLocators.PRODUCT_CARDS))

    def sort_by(self, option_value):
        Select(self.find_element(CategoryPageLocators.SORT_DROPDOWN)).select_by_value(option_value)
        self.wait_for_products_loaded()

    def get_product_names(self):
        return [name for name in self.get_elements_text(CategoryPageLocators.PRODUCT_NAMES) if name]

    def get_product_prices(self):
        return [self._parse_price(price) for price in self.get_elements_text(CategoryPageLocators.PRODUCT_PRICES)]

    def wait_for_products_loaded(self):
        self.wait_for_visible(CategoryPageLocators.PRODUCT_CARDS)

    @staticmethod
    def _parse_price(price_text):
        prices = re.findall(r"\$([\d,.]+)", price_text)
        return Decimal(prices[-1].replace(",", ""))
