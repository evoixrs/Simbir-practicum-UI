import re
from decimal import Decimal

from selenium.webdriver.support.select import Select

from locators.page_locators import CategoryPageLocators
from pages.base_page import BasePage


"""Page object страницы категории товаров"""
class CategoryPage(BasePage):

    """Возвращает заголовок текущей категории"""
    def get_title(self):
        return self.get_text(CategoryPageLocators.PAGE_TITLE)

    """Возвращает количество карточек товаров в категории"""
    def get_products_count(self):
        return len(self.find_elements(CategoryPageLocators.PRODUCT_CARDS))

    """Выбирает сортировку в выпадающем списке Sort By"""
    def sort_by(self, option_value):
        Select(self.find_element(CategoryPageLocators.SORT_DROPDOWN)).select_by_value(option_value)
        self.wait_for_products_loaded()

    """Возвращает список названий товаров в текущем порядке"""
    def get_product_names(self):
        return [name for name in self.get_elements_text(CategoryPageLocators.PRODUCT_NAMES) if name]

    """Возвращает список цен товаров в текущем порядке"""
    def get_product_prices(self):
        return [self._parse_price(price) for price in self.get_elements_text(CategoryPageLocators.PRODUCT_PRICES)]

    """Ожидает загрузку карточек товаров после перехода или сортировки"""
    def wait_for_products_loaded(self):
        self.wait_for_visible(CategoryPageLocators.PRODUCT_CARDS)

    """Преобразует цену из текста вида '$12.34' в Decimal"""
    @staticmethod
    def _parse_price(price_text):
        prices = re.findall(r"\$([\d,.]+)", price_text)
        return Decimal(prices[-1].replace(",", ""))
