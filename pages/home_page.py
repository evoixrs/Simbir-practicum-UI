from locators.home_page_locators import HomePageLocators
from pages.base_page import BasePage


class HomePage(BasePage):
    def search(self, query: str) -> None:
        self.input(HomePageLocators.SEARCH_INPUT, query)
        self.press_enter(HomePageLocators.SEARCH_INPUT)

    def open_men_fragrance_sets_from_dropdown(self) -> None:
        self.hover(HomePageLocators.MEN_MENU)
        self.click(HomePageLocators.FRAGRANCE_SETS)
