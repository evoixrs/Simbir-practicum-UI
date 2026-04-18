from selenium.webdriver.common.by import By


class HomePageLocators:
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
