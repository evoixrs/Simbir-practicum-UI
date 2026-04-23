from selenium.webdriver.common.by import By


class HomePageLocators:
    SEARCH_INPUT = (By.ID, "filter_keyword")
    SEARCH_BTN = (By.CSS_SELECTOR, "button.btn.btn-default.btn-lg")
    MEN_MENU = (By.CSS_SELECTOR, "a[href$='path=58']")
    FRAGRANCE_SETS = (By.CSS_SELECTOR, "a[href*='path=58_59']")
