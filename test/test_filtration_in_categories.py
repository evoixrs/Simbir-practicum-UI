import allure

from locators.page_locators import CategoryPageLocators
from pages.category_page import CategoryPage
from pages.home_page import HomePage


@allure.feature("Категории")
@allure.story("Сортировка товаров")
@allure.title("Сортировка товаров в подкатегории Men > Fragrance Sets")
def test_filtration_in_categories(driver, base_url):
    """Создаем page object категории поверх готового драйвера"""
    home_page = HomePage(driver, base_url)
    category_page = CategoryPage(driver, base_url)

    with allure.step("Открыть главную страницу сайта"):
        """Открываем главную страницу и проверяем, что перешли на нужный домен"""
        home_page.open(base_url)
        assert "automationteststore.com" in driver.current_url

    with allure.step("Перейти в подкатегорию Men > Fragrance Sets"):
        """Наводим курсор на Men и открываем Fragrance Sets из выпадающего меню"""
        home_page.open_men_fragrance_sets_from_dropdown()
        assert "fragrance sets" in category_page.get_title().casefold()

    with allure.step("Проверить количество товаров в подкатегории"):
        """Сохраняем исходное количество товаров для дальнейших проверок"""
        initial_count = category_page.get_products_count()
        assert initial_count >= 4

    with allure.step("Проверить сортировку Name A - Z"):
        """Проверяем сортировку товаров по названию от A до Z"""
        category_page.sort_by(CategoryPageLocators.SORT_NAME_ASC)
        names = category_page.get_product_names()
        assert category_page.get_products_count() == initial_count
        assert names == sorted(names, key=str.casefold)

    with allure.step("Проверить сортировку Name Z - A"):
        """Проверяем сортировку товаров по названию от Z до A"""
        category_page.sort_by(CategoryPageLocators.SORT_NAME_DESC)
        names = category_page.get_product_names()
        assert category_page.get_products_count() == initial_count
        assert names == sorted(names, key=str.casefold, reverse=True)

    with allure.step("Проверить сортировку Price Low > High"):
        """Проверяем сортировку товаров по цене от меньшей к большей"""
        category_page.sort_by(CategoryPageLocators.SORT_PRICE_ASC)
        prices = category_page.get_product_prices()
        assert category_page.get_products_count() == initial_count
        assert prices == sorted(prices)

    with allure.step("Проверить сортировку Price High > Low"):
        """Проверяем сортировку товаров по цене от большей к меньшей"""
        category_page.sort_by(CategoryPageLocators.SORT_PRICE_DESC)
        prices = category_page.get_product_prices()
        assert category_page.get_products_count() == initial_count
        assert prices == sorted(prices, reverse=True)
