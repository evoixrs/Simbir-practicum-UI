import allure

from pages.category_page import CategoryPage
from pages.home_page import HomePage
from sorting.sort_options import SortOptions


@allure.feature("Категории")
@allure.story("Сортировка товаров")
@allure.title("Сортировка товаров в подкатегории Men > Fragrance Sets")
def test_filtration_in_categories(driver, base_url):
    home_page = HomePage(driver, base_url)
    category_page = CategoryPage(driver, base_url)

    with allure.step("Открыть главную страницу сайта"):
        home_page.open(base_url)
        assert "automationteststore.com" in driver.current_url

    with allure.step("Перейти в подкатегорию Men > Fragrance Sets"):
        home_page.open_men_fragrance_sets_from_dropdown()
        assert "fragrance sets" in category_page.get_title().casefold()

    with allure.step("Проверить количество товаров в подкатегории"):
        initial_count = category_page.get_products_count()
        assert initial_count >= 4

    with allure.step("Проверить сортировку Name A - Z"):
        category_page.sort_by(SortOptions.NAME_ASC)
        names = category_page.get_product_names()
        assert category_page.get_products_count() == initial_count
        assert names == sorted(names, key=str.casefold)

    with allure.step("Проверить сортировку Name Z - A"):
        category_page.sort_by(SortOptions.NAME_DESC)
        names = category_page.get_product_names()
        assert category_page.get_products_count() == initial_count
        assert names == sorted(names, key=str.casefold, reverse=True)

    with allure.step("Проверить сортировку Price Low > High"):
        category_page.sort_by(SortOptions.PRICE_ASC)
        prices = category_page.get_product_prices()
        assert category_page.get_products_count() == initial_count
        assert prices == sorted(prices)

    with allure.step("Проверить сортировку Price High > Low"):
        category_page.sort_by(SortOptions.PRICE_DESC)
        prices = category_page.get_product_prices()
        assert category_page.get_products_count() == initial_count
        assert prices == sorted(prices, reverse=True)
