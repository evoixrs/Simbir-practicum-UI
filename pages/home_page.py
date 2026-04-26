from typing import TypedDict

from locators.home_page_locators import HomePageLocators
from pages.base_page import BasePage


class ProductLink(TypedDict):
    name: str
    href: str


class HomePage(BasePage):
    def search(self, query: str) -> None:
        self.input(HomePageLocators.SEARCH_INPUT, query)
        self.press_enter(HomePageLocators.SEARCH_INPUT)

    def open_men_fragrance_sets_from_dropdown(self) -> None:
        self.hover(HomePageLocators.MEN_MENU)
        self.click(HomePageLocators.FRAGRANCE_SETS)

    def get_unique_product_links(self) -> list[ProductLink]:
        unique_products: list[ProductLink] = []
        seen_hrefs: set[str] = set()

        for product_link in self.find_elements(HomePageLocators.PRODUCT_NAME_LINKS):
            href = self.get_element_attribute_value(product_link, "href")
            name = self.get_element_text(product_link)

            if not href or href in seen_hrefs or not name:
                continue

            seen_hrefs.add(href)
            unique_products.append({"name": name, "href": href})

        return unique_products

    def open_product_by_href(self, href: str) -> None:
        self.open(href)

    def open_home_from_navigation(self) -> None:
        self.click(HomePageLocators.HOME_LINK)

    def open_cart_from_navigation(self) -> None:
        self.click(HomePageLocators.CART_LINK)
