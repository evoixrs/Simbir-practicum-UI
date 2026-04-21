from selenium.webdriver.common.by import By


class HomePageLocators:
    """Поле ввода поискового запроса"""
    SEARCH_INPUT = (By.ID, "filter_keyword")

    """Кнопка запуска поиска"""
    SEARCH_BTN = (By.CSS_SELECTOR, "button.btn.btn-default.btn-lg")

    """Ссылка на категорию Men в главном меню для hover"""
    MEN_MENU = (By.CSS_SELECTOR, "a[href$='path=58']")

    """Подкатегория Fragrance Sets в выпадающем дропдауне Men"""
    FRAGRANCE_SETS = (By.CSS_SELECTOR, "a[href*='path=58_59']")


"""Локаторы страницы категории товаров"""
class CategoryPageLocators:
    """Заголовок страницы категории"""
    PAGE_TITLE = (By.CSS_SELECTOR, "h1 .maintext")

    """Дропдаун сортировки товаров"""
    SORT_DROPDOWN = (By.ID, "sort")

    """Значения опций сортировки"""
    SORT_NAME_ASC = "pd.name-ASC"
    SORT_NAME_DESC = "pd.name-DESC"
    SORT_PRICE_ASC = "p.price-ASC"
    SORT_PRICE_DESC = "p.price-DESC"

    """Карточки товаров на странице категории"""
    PRODUCT_CARDS = (By.CSS_SELECTOR, ".thumbnails.grid .col-md-3")

    """Все названия товаров на странице категории"""
    PRODUCT_NAMES = (By.CSS_SELECTOR, "a.prdocutname")

    """Все цены товаров на странице категории"""
    PRODUCT_PRICES = (By.CSS_SELECTOR, "div.pricetag.jumbotron")


"""Локаторы страницы поисковой выдачи"""
class SearchPageLocators:
    """Все карточки товаров в сетке результатов поиска"""
    PRODUCT_CARDS = (By.CSS_SELECTOR, ".thumbnails.grid .col-md-3")

    """Ссылки на товары внутри карточек"""
    PRODUCT_LINKS_IN_CARD = (By.CSS_SELECTOR, "a[href*='product_id']")

    """Дропдаун сортировки"""
    SORT_DROPDOWN = (By.CSS_SELECTOR, "select[name='sort']")

    """Значение сортировки Name A - Z"""
    SORT_NAME_ASC = "pd.name-ASC"

    """Названия товаров во всех карточках"""
    PRODUCT_NAMES = (By.CSS_SELECTOR, ".thumbnails.grid .col-md-3 .prdocutname")


"""Локаторы страницы товара"""
class ProductPageLocators:
    """Заголовок страницы товара"""
    PRODUCT_NAME = (By.CSS_SELECTOR, "h1.productname")

    """Цена товара на странице товара"""
    PRODUCT_PRICE = (By.CSS_SELECTOR, ".productpageprice .productfilneprice")

    """Поле ввода количества товара"""
    QTY_INPUT = (By.ID, "product_quantity")

    """Кнопка Add to Cart"""
    ADD_TO_CART_BTN = (By.CSS_SELECTOR, "a.cart")


"""Локаторы страницы корзины"""
class CartPageLocators:
    """Ссылка Basket в хлебных крошках"""
    BASKET_LINK = (By.CSS_SELECTOR, "a[href*='checkout/cart']")

    """Все строки с товарами в таблице корзины"""
    CART_ROWS = (By.XPATH, "//div[contains(@class, 'product-list')]//tr[.//input[starts-with(@name, 'quantity')]]")

    """Кнопка Update"""
    UPDATE_BTN = (By.XPATH, "//button[contains(., 'Update')]")

    """Sub-Total в блоке итогов"""
    SUB_TOTAL = (By.XPATH, "//table[@id='totals_table']//tr[td/span[contains(., 'Sub-Total')]]/td[2]/span")

    """Название строки Total в блоке итогов"""
    CART_TOTAL_LABEL = (By.CSS_SELECTOR, "span.extra.bold.totalamout")

    """Значение строки Total в блоке итогов"""
    CART_TOTAL = (By.CSS_SELECTOR, "span.bold.totalamout:not(.extra)")
