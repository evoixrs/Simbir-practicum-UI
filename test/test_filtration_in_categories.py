import allure
from selenium.webdriver.remote.webdriver import WebDriver

from pages.category_page import CategoryPage
from pages.home_page import HomePage
from data.sort_options import SortOptions


@allure.feature("Категории")
@allure.story("Сортировка товаров")
@allure.suite("UI tests")
@allure.sub_suite("Catalog")
@allure.tag("ui", "catalog", "sorting", "positive", "TC-01")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("Сортировка товаров в подкатегории Men > Fragrance Sets")
@allure.description(
    "Проверка сортировки товаров по тест-кейсу TC-01 из docs/test_cases.md. "
    "Тест открывает подкатегорию Men > Fragrance Sets и проверяет сортировку "
    "по названию и цене в обоих направлениях."
)
def test_filtration_in_categories(driver: WebDriver, base_url: str) -> None:
    home_page = HomePage(driver, base_url)
    category_page = CategoryPage(driver, base_url)

    with allure.step("Открыть главную страницу сайта"):
        home_page.open(base_url)
        assert "automationteststore.com" in home_page.get_current_url(), (
            f"Ожидался домен automationteststore.com, получен URL: {home_page.get_current_url()}"
        )

    with allure.step("Перейти в подкатегорию Men > Fragrance Sets"):
        home_page.open_men_fragrance_sets_from_dropdown()
        assert "fragrance sets" in category_page.get_title().casefold(), (
            f"Ожидалось открытие категории Fragrance Sets, получен заголовок: {category_page.get_title()}"
        )

    with allure.step("Проверить количество товаров в подкатегории"):
        initial_count = category_page.get_products_count()
        assert initial_count >= 4, f"Ожидалось минимум 4 товара в категории, найдено: {initial_count}"

    with allure.step("Проверить сортировку Name A - Z"):
        category_page.sort_by(SortOptions.NAME_ASC)
        names = category_page.get_product_names()
        current_count = category_page.get_products_count()
        assert current_count == initial_count, (
            f"После сортировки Name A - Z количество товаров изменилось: было {initial_count}, стало {current_count}"
        )
        assert names == sorted(names, key=str.casefold), (
            f"Сортировка Name A - Z не применена. Получен порядок: {names}"
        )

    with allure.step("Проверить сортировку Name Z - A"):
        category_page.sort_by(SortOptions.NAME_DESC)
        names = category_page.get_product_names()
        current_count = category_page.get_products_count()
        assert current_count == initial_count, (
            f"После сортировки Name Z - A количество товаров изменилось: было {initial_count}, стало {current_count}"
        )
        assert names == sorted(names, key=str.casefold, reverse=True), (
            f"Сортировка Name Z - A не применена. Получен порядок: {names}"
        )

    with allure.step("Проверить сортировку Price Low > High"):
        category_page.sort_by(SortOptions.PRICE_ASC)
        prices = category_page.get_product_prices()
        current_count = category_page.get_products_count()
        assert current_count == initial_count, (
            f"После сортировки Price Low > High количество товаров изменилось: было {initial_count}, стало {current_count}"
        )
        assert prices == sorted(prices), (
            f"Сортировка Price Low > High не применена. Получен порядок цен: {prices}"
        )

    with allure.step("Проверить сортировку Price High > Low"):
        category_page.sort_by(SortOptions.PRICE_DESC)
        prices = category_page.get_product_prices()
        current_count = category_page.get_products_count()
        assert current_count == initial_count, (
            f"После сортировки Price High > Low количество товаров изменилось: было {initial_count}, стало {current_count}"
        )
        assert prices == sorted(prices, reverse=True), (
            f"Сортировка Price High > Low не применена. Получен порядок цен: {prices}"
        )
