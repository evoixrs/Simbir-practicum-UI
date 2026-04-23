from selenium.webdriver.common.by import By


class CategoryPageLocators:
    PAGE_TITLE = (By.CSS_SELECTOR, "h1 .maintext")
    SORT_DROPDOWN = (By.ID, "sort")
    PRODUCT_CARDS = (By.CSS_SELECTOR, ".thumbnails.grid .col-md-3")
    PRODUCT_NAMES = (By.CSS_SELECTOR, "a.prdocutname")
    PRODUCT_PRICES = (By.CSS_SELECTOR, "div.pricetag.jumbotron")
