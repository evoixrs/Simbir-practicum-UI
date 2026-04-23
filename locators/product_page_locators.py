from selenium.webdriver.common.by import By


class ProductPageLocators:
    PRODUCT_NAME = (By.CSS_SELECTOR, "h1.productname")
    PRODUCT_PRICE = (By.CSS_SELECTOR, ".productpageprice .productfilneprice")
    QTY_INPUT = (By.ID, "product_quantity")
    ADD_TO_CART_BTN = (By.CSS_SELECTOR, "a.cart")
