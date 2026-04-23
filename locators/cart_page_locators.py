from selenium.webdriver.common.by import By


class CartPageLocators:
    BASKET_LINK = (By.CSS_SELECTOR, "a[href*='checkout/cart']")
    CART_ROWS = (By.XPATH, "//div[contains(@class, 'product-list')]//tr[.//input[starts-with(@name, 'quantity')]]")
    UPDATE_BTN = (By.XPATH, "//button[contains(., 'Update')]")
    SUB_TOTAL = (By.XPATH, "//table[@id='totals_table']//tr[td/span[contains(., 'Sub-Total')]]/td[2]/span")
    CART_TOTAL_LABEL = (By.CSS_SELECTOR, "span.extra.bold.totalamout")
    CART_TOTAL = (By.CSS_SELECTOR, "span.bold.totalamout:not(.extra)")
