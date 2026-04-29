import logging
import random

import allure
from selenium.webdriver.remote.webdriver import WebDriver

from pages.cart_page import CartPage
from pages.home_page import HomePage
from pages.product_page import ProductPage
from pages.search_page import SearchPage
from data.sort_options import SortOptions


logger = logging.getLogger("qa")


@allure.feature("Корзина")
@allure.story("Поиск, добавление товаров и пересчет суммы")
@allure.suite("UI tests")
@allure.sub_suite("Cart")
@allure.tag("ui", "cart", "search", "positive", "TC-02")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Поиск shirt, добавление 2-го и 3-го товара и проверка итоговой суммы")
@allure.description(
    "Проверка корзины по тест-кейсу TC-02 из docs/test_cases.md. "
    "Тест выполняет поиск shirt, добавляет 2-й и 3-й товары, меняет количество "
    "самого дешевого товара и проверяет итоговую сумму корзины."
)
def test_search_results_and_cart(driver: WebDriver, base_url: str) -> None:
    home_page = HomePage(driver, base_url)
    search_page = SearchPage(driver, base_url)
    product_page = ProductPage(driver, base_url)
    cart_page = CartPage(driver, base_url)
    added_products = []

    with allure.step("Открыть главную страницу сайта"):
        home_page.open(base_url)
        assert "automationteststore.com" in home_page.get_current_url(), (
            f"Ожидался домен automationteststore.com, получен URL: {home_page.get_current_url()}"
        )

    with allure.step("Выполнить поиск по запросу shirt"):
        home_page.search("shirt")
        products_count = search_page.get_products_count()
        assert products_count >= 3, f"Ожидалось минимум 3 товара по запросу shirt, найдено: {products_count}"

    with allure.step("Отсортировать выдачу по Name A - Z"):
        search_page.sort_by(SortOptions.NAME_ASC)
        names = search_page.get_product_names()
        assert names == sorted(names, key=str.casefold), (
            f"Сортировка Name A - Z не применена в результатах поиска. Получен порядок: {names}"
        )

    for product_index in [1, 2]:
        with allure.step(f"Открыть товар на позиции {product_index + 1} из выдачи"):
            search_page.open_product_by_index(product_index)
            assert "product_id" in search_page.get_current_url(), (
                f"Ожидалось открытие страницы товара, получен URL: {search_page.get_current_url()}"
            )

        with allure.step("Сохранить название, цену и добавить товар в корзину"):
            max_quantity = product_page.get_quantity_limit() or 15
            quantity = random.randint(1, min(15, max_quantity))
            product_data = {
                "name": product_page.get_product_name(),
                "price": product_page.get_product_price(),
                "quantity": quantity,
            }
            product_page.set_quantity(quantity)
            product_page.add_to_cart()
            added_products.append(product_data)

        if product_index == 1:
            with allure.step("Вернуться на страницу отсортированной поисковой выдачи"):
                # Восстанавливаем выдачу через новый поиск, потому что возврат по истории браузера нестабилен в CI.
                home_page.open(base_url)
                home_page.search("shirt")
                search_page.sort_by(SortOptions.NAME_ASC)
                products_count = search_page.get_products_count()
                assert products_count >= 3, (
                    f"После повторного поиска ожидалось минимум 3 товара, найдено: {products_count}"
                )

    with allure.step("Проверить состав корзины"):
        rows_count = cart_page.get_rows_count()
        assert rows_count == 2, f"Ожидалось 2 товара в корзине, найдено: {rows_count}"
        cart_rows = cart_page.get_rows()
        cart_names = [cart_page.get_row_name(row).casefold() for row in cart_rows]
        cart_quantities = [cart_page.get_row_quantity(row) for row in cart_rows]
        for product_data in added_products:
            assert product_data["name"].casefold() in cart_names, (
                f"Товар '{product_data['name']}' не найден в корзине. Текущие товары: {cart_names}"
            )
            assert product_data["quantity"] in cart_quantities, (
                f"Количество {product_data['quantity']} не найдено в корзине. Текущие количества: {cart_quantities}"
            )

    with allure.step("Запомнить итоговую сумму Total внизу страницы"):
        cart_total_before_update = cart_page.get_cart_total()
        logger.info("Total до обновления корзины: %s", cart_total_before_update)
        assert cart_total_before_update > 0, (
            f"Итоговая сумма корзины должна быть больше 0, получено: {cart_total_before_update}"
        )

    with allure.step("Найти самый дешевый товар по столбцу Total"):
        cheapest_index = cart_page.get_cheapest_row_index()
        cheapest_row_total = cart_page.get_row_total(cart_page.get_rows()[cheapest_index])
        cheapest_quantity = cart_page.get_row_quantity(cart_page.get_rows()[cheapest_index])
        logger.info("Total строки самого дешевого товара до обновления: %s", cheapest_row_total)
        logger.info("Количество самого дешевого товара до обновления: %s", cheapest_quantity)

    with allure.step("Удвоить количество самого дешевого товара"):
        cart_page.set_row_quantity(cheapest_index, cheapest_quantity * 2)
        cart_page.update_cart()
        updated_quantity = cart_page.get_row_quantity(cart_page.get_rows()[cheapest_index])
        expected_quantity = cheapest_quantity * 2
        assert updated_quantity == expected_quantity, (
            f"Количество самого дешевого товара не обновилось. Ожидалось: {expected_quantity}, получено: {updated_quantity}"
        )

    with allure.step("Проверить итоговую сумму корзины"):
        expected_sub_total = sum(cart_page.get_row_totals())
        actual_sub_total = cart_page.get_sub_total()
        logger.info("Ожидаемый Sub-Total после обновления: %s", expected_sub_total)
        logger.info("Фактический Sub-Total после обновления: %s", actual_sub_total)
        assert abs(actual_sub_total - expected_sub_total) <= 0.01, (
            f"Sub-Total рассчитан неверно. Ожидалось: {expected_sub_total}, получено: {actual_sub_total}"
        )
        expected_cart_total = cart_total_before_update + cheapest_row_total
        actual_cart_total = cart_page.get_cart_total()
        logger.info("Ожидаемый Total после обновления: %s", expected_cart_total)
        logger.info("Фактический Total после обновления: %s", actual_cart_total)
        assert abs(actual_cart_total - expected_cart_total) <= 0.01, (
            f"Total рассчитан неверно. Ожидалось: {expected_cart_total}, получено: {actual_cart_total}"
        )
