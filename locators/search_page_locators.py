from selenium.webdriver.common.by import By


class SearchPageLocators:
    PRODUCT_CARDS = (By.CSS_SELECTOR, ".thumbnails.grid .col-md-3")
    PRODUCT_LINKS_IN_CARD = (By.CSS_SELECTOR, "a[href*='product_id']")
    SORT_DROPDOWN = (By.CSS_SELECTOR, "select[name='sort']")
    PRODUCT_NAMES = (By.CSS_SELECTOR, ".thumbnails.grid .col-md-3 .prdocutname")
