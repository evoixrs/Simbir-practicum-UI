from selenium.webdriver.common.by import By


class CartPageLocators:
    BASKET_LINK = (By.CSS_SELECTOR, "a[href*='checkout/cart']")
    CART_ROWS = (By.XPATH, "//div[contains(@class, 'product-list')]//tr[.//input[starts-with(@name, 'quantity')]]")
    ROW_PRODUCT_NAME = (By.CSS_SELECTOR, "td:nth-child(2) a")
    ROW_QUANTITY_INPUT = (By.CSS_SELECTOR, "input[name^='quantity']")
    ROW_TOTAL_COLUMNS = (By.CSS_SELECTOR, "td.align_right")
    UPDATE_BTN = (By.XPATH, "//button[contains(., 'Update')]")
    SUB_TOTAL = (By.XPATH, "//table[@id='totals_table']//span[contains(normalize-space(.), 'Sub-Total:')]/parent::td/following-sibling::td/span")
    CART_TOTAL_LABEL = (By.CSS_SELECTOR, "span.extra.bold.totalamout")
    CART_TOTAL = (By.CSS_SELECTOR, "span.bold.totalamout:not(.extra)")
