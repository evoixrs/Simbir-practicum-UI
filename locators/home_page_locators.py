from selenium.webdriver.common.by import By


class HomePageLocators:
    SEARCH_INPUT = (By.ID, "filter_keyword")
    SEARCH_BTN = (By.CSS_SELECTOR, "button.btn.btn-default.btn-lg")
    MEN_MENU = (By.CSS_SELECTOR, "a[href$='path=58']")
    FRAGRANCE_SETS = (By.CSS_SELECTOR, "a[href*='path=58_59']")
    PRODUCT_NAME_LINKS = (By.CSS_SELECTOR, "a.prdocutname")
    HOME_LINK = (By.LINK_TEXT, "HOME")
    CART_LINK = (By.LINK_TEXT, "CART")

    @staticmethod
    def product_link_by_href(href: str) -> tuple[str, str]:
        return By.CSS_SELECTOR, f'a.prdocutname[href="{href}"]'
