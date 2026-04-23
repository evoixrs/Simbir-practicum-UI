from selenium.webdriver.remote.webelement import WebElement

from locators.search_page_locators import SearchPageLocators
from pages.base_page import BasePage


class SearchPage(BasePage):
    def get_product_cards(self) -> list[WebElement]:
        return self.find_elements(SearchPageLocators.PRODUCT_CARDS)

    def get_products_count(self) -> int:
        return len(self.get_product_cards())

    def sort_by(self, option_value: str) -> None:
        self.select_by_value(SearchPageLocators.SORT_DROPDOWN, option_value)
        self.wait_for_visible(SearchPageLocators.PRODUCT_CARDS)

    def get_product_names(self) -> list[str]:
        return [name for name in self.get_elements_text(SearchPageLocators.PRODUCT_NAMES) if name]

    def open_product_by_index(self, index: int) -> None:
        card = self.get_product_cards()[index]
        self.click_inner_element(card, SearchPageLocators.PRODUCT_LINKS_IN_CARD)
