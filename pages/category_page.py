import re
from decimal import Decimal

from locators.category_page_locators import CategoryPageLocators
from pages.base_page import BasePage


class CategoryPage(BasePage):
    def get_title(self) -> str:
        return self.get_text(CategoryPageLocators.PAGE_TITLE)

    def get_products_count(self) -> int:
        return len(self.find_elements(CategoryPageLocators.PRODUCT_CARDS))

    def sort_by(self, option_value: str) -> None:
        self.select_by_value(CategoryPageLocators.SORT_DROPDOWN, option_value)
        self.wait_for_products_loaded()

    def get_product_names(self) -> list[str]:
        return [name for name in self.get_elements_text(CategoryPageLocators.PRODUCT_NAMES) if name]

    def get_product_prices(self) -> list[Decimal]:
        return [self._parse_price(price) for price in self.get_elements_text(CategoryPageLocators.PRODUCT_PRICES)]

    def wait_for_products_loaded(self) -> None:
        self.wait_for_visible(CategoryPageLocators.PRODUCT_CARDS)

    @staticmethod
    def _parse_price(price_text: str) -> Decimal:
        prices = re.findall(r"\$([\d,.]+)", price_text)
        return Decimal(prices[-1].replace(",", ""))
