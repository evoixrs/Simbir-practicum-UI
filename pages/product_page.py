import re
from decimal import Decimal

from locators.product_page_locators import ProductPageLocators
from pages.base_page import BasePage


class ProductPage(BasePage):
    def get_product_name(self) -> str:
        return self.get_text(ProductPageLocators.PRODUCT_NAME)

    def get_product_price(self) -> Decimal:
        return self._parse_price(self.get_text(ProductPageLocators.PRODUCT_PRICE))

    def has_product_options(self) -> bool:
        return bool(self.driver.find_elements(*ProductPageLocators.PRODUCT_OPTIONS))

    def set_quantity(self, quantity: int) -> None:
        self.input(ProductPageLocators.QTY_INPUT, str(quantity))

    def get_quantity_limit(self) -> int | None:
        # Лимит количества на странице не вынесен в отдельный атрибут, поэтому читаем его из текста страницы.
        page_text = self.get_page_text()
        limit = re.search(r"limit set to (\d+)", page_text)

        if limit:
            quantity_limit = int(limit.group(1))
            return quantity_limit

        return None

    def add_to_cart(self) -> None:
        self.click(ProductPageLocators.ADD_TO_CART_BTN)

    @staticmethod
    def _parse_price(price_text: str) -> Decimal:
        price = re.search(r"\$([\d,.]+)", price_text)
        return Decimal(price.group(1).replace(",", ""))
