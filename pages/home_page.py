from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

from locators.page_locators import HomePageLocators
from pages.base_page import BasePage


"""Page object главной страницы"""
class HomePage(BasePage):

    """Выполняет поиск по введенному запросу"""
    def search(self, query):
        self.input(HomePageLocators.SEARCH_INPUT, query)
        self.find_element(HomePageLocators.SEARCH_INPUT).send_keys(Keys.ENTER)

    """Наводит курсор на категорию Men и открывает Fragrance Sets из dropdown"""
    def open_men_fragrance_sets_from_dropdown(self):
        men_menu = self.find_element(HomePageLocators.MEN_MENU)
        ActionChains(self.driver).move_to_element(men_menu).perform()
        self.click(HomePageLocators.FRAGRANCE_SETS)
