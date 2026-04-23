from selenium.webdriver.support.select import Select

from locators.search_page_locators import SearchPageLocators
from pages.base_page import BasePage


class SearchPage(BasePage):
    def get_product_cards(self):
        return self.find_elements(SearchPageLocators.PRODUCT_CARDS)

    def get_products_count(self):
        return len(self.get_product_cards())

    def sort_by(self, option_value):
        Select(self.find_element(SearchPageLocators.SORT_DROPDOWN)).select_by_value(option_value)
        self.wait_for_visible(SearchPageLocators.PRODUCT_CARDS)

    def get_product_names(self):
        return [name for name in self.get_elements_text(SearchPageLocators.PRODUCT_NAMES) if name]

    def open_product_by_index(self, index):
        card = self.get_product_cards()[index]
        card.find_element(*SearchPageLocators.PRODUCT_LINKS_IN_CARD).click()
