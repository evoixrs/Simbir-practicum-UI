import re
from decimal import Decimal

from selenium.webdriver.remote.webelement import WebElement

from locators.cart_page_locators import CartPageLocators
from pages.base_page import BasePage


class CartPage(BasePage):
    def get_rows(self) -> list[WebElement]:
        return self.find_elements(CartPageLocators.CART_ROWS)

    def get_rows_count(self) -> int:
        return len(self.get_rows())

    def get_row_name(self, row: WebElement) -> str:
        return self.get_inner_element_text(row, CartPageLocators.ROW_PRODUCT_NAME)

    def get_row_quantity(self, row: WebElement) -> int:
        quantity = self.get_inner_element_attribute(row, CartPageLocators.ROW_QUANTITY_INPUT, "value")
        return int(quantity)

    def get_row_total(self, row: WebElement) -> Decimal:
        return self._parse_price(self.get_inner_elements_text(row, CartPageLocators.ROW_TOTAL_COLUMNS)[-1])

    def get_row_totals(self) -> list[Decimal]:
        return [self.get_row_total(row) for row in self.get_rows()]

    def get_sub_total(self) -> Decimal:
        return self._parse_price(self.get_text(CartPageLocators.SUB_TOTAL))

    def get_cart_total(self) -> Decimal:
        return self._parse_price(self.get_text(CartPageLocators.CART_TOTAL))

    def get_cheapest_row_index(self) -> int:
        totals = self.get_row_totals()
        return totals.index(min(totals))

    def set_row_quantity(self, index: int, quantity: int) -> None:
        self.input_inner_element(self.get_rows()[index], CartPageLocators.ROW_QUANTITY_INPUT, str(quantity))

    def remove_row_by_name(self, name: str) -> None:
        current_rows = self.get_rows()
        current_count = len(current_rows)

        for row in current_rows:
            if self.get_row_name(row).casefold() == name.casefold():
                self.click_inner_element(row, CartPageLocators.ROW_REMOVE_BTN)

                if current_count > 1:
                    self.wait_for_visible(CartPageLocators.CART_ROWS)

                return

        raise AssertionError(f"Товар '{name}' не найден в корзине для удаления")

    def update_cart(self) -> None:
        self.click(CartPageLocators.UPDATE_BTN)
        self.wait_for_visible(CartPageLocators.CART_ROWS)

    @staticmethod
    def _parse_price(price_text: str) -> Decimal:
        price = re.search(r"\$([\d,.]+)", price_text)
        return Decimal(price.group(1).replace(",", ""))
