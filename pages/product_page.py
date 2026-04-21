import re
from decimal import Decimal

from selenium.webdriver.common.by import By

from locators.page_locators import ProductPageLocators
from pages.base_page import BasePage


"""Page object страницы товара"""
class ProductPage(BasePage):
    """Возвращает название товара"""
    def get_product_name(self):
        return self.get_text(ProductPageLocators.PRODUCT_NAME)

    """Возвращает цену товара"""
    def get_product_price(self):
        return self._parse_price(self.get_text(ProductPageLocators.PRODUCT_PRICE))

    """Вводит количество товара"""
    def set_quantity(self, quantity):
        self.input(ProductPageLocators.QTY_INPUT, str(quantity))

    """Возвращает лимит количества товара, если он указан на странице"""
    def get_quantity_limit(self):
        page_text = self.driver.find_element(By.TAG_NAME, "body").text
        limit = re.search(r"limit set to (\d+)", page_text)

        if limit:
            quantity_limit = int(limit.group(1))
            return quantity_limit

        return None

    """Добавляет товар в корзину"""
    def add_to_cart(self):
        self.click(ProductPageLocators.ADD_TO_CART_BTN)

    """Преобразует цену из текста в Decimal"""
    @staticmethod
    def _parse_price(price_text):
        price = re.search(r"\$([\d,.]+)", price_text)
        return Decimal(price.group(1).replace(",", ""))
