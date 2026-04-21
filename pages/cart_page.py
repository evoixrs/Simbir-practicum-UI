import re
from decimal import Decimal

from selenium.webdriver.common.by import By

from locators.page_locators import CartPageLocators
from pages.base_page import BasePage


"""Page object страницы корзины"""
class CartPage(BasePage):
    """Возвращает строки товаров в корзине"""
    def get_rows(self):
        return self.find_elements(CartPageLocators.CART_ROWS)

    """Возвращает количество строк товаров в корзине"""
    def get_rows_count(self):
        return len(self.get_rows())

    """Возвращает название товара из строки корзины"""
    def get_row_name(self, row):
        return row.find_element(By.CSS_SELECTOR, "td:nth-child(2) a").text.strip()

    """Возвращает текущее количество товара из строки корзины"""
    def get_row_quantity(self, row):
        return int(row.find_element(By.CSS_SELECTOR, "input[name^='quantity']").get_attribute("value"))

    """Возвращает итоговую сумму строки"""
    def get_row_total(self, row):
        return self._parse_price(row.find_elements(By.CSS_SELECTOR, "td.align_right")[-1].text)

    """Возвращает все итоговые суммы строк"""
    def get_row_totals(self):
        return [self.get_row_total(row) for row in self.get_rows()]

    """Возвращает Sub-Total корзины"""
    def get_sub_total(self):
        return self._parse_price(self.get_text(CartPageLocators.SUB_TOTAL))

    """Возвращает Total корзины"""
    def get_cart_total(self):
        return self._parse_price(self.get_text(CartPageLocators.CART_TOTAL))

    """Возвращает индекс строки с минимальной итоговой суммой"""
    def get_cheapest_row_index(self):
        totals = self.get_row_totals()
        return totals.index(min(totals))

    """Устанавливает новое количество товара в строке по индексу"""
    def set_row_quantity(self, index, quantity):
        quantity_input = self.get_rows()[index].find_element(By.CSS_SELECTOR, "input[name^='quantity']")
        quantity_input.clear()
        quantity_input.send_keys(str(quantity))

    """Обновляет корзину после изменения количества"""
    def update_cart(self):
        self.click(CartPageLocators.UPDATE_BTN)
        self.wait_for_visible(CartPageLocators.CART_ROWS)

    """Преобразует цену из текста в Decimal"""
    @staticmethod
    def _parse_price(price_text):
        price = re.search(r"\$([\d,.]+)", price_text)
        return Decimal(price.group(1).replace(",", ""))
