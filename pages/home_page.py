from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

from locators.home_page_locators import HomePageLocators
from pages.base_page import BasePage


class HomePage(BasePage):
    def search(self, query):
        self.input(HomePageLocators.SEARCH_INPUT, query)
        self.find_element(HomePageLocators.SEARCH_INPUT).send_keys(Keys.ENTER)

    def open_men_fragrance_sets_from_dropdown(self):
        men_menu = self.find_element(HomePageLocators.MEN_MENU)
        ActionChains(self.driver).move_to_element(men_menu).perform()
        self.click(HomePageLocators.FRAGRANCE_SETS)
