import random
from decimal import Decimal

import allure
from selenium.webdriver.remote.webdriver import WebDriver

from pages.cart_page import CartPage
from pages.home_page import HomePage
from pages.product_page import ProductPage


@allure.feature("Корзина")
@allure.story("Удаление товаров на четных позициях из исходного порядка")
@allure.suite("UI tests")
@allure.sub_suite("Cart")
@allure.tag("ui", "cart", "remove", "positive", "TC-03")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Состояние корзины после удаления товаров с позиций 2 и 4")
@allure.description(
    "Проверка корзины по тест-кейсу TC-03 из docs/test_cases.md. "
    "Тест добавляет 5 уникальных товаров, удаляет товары на позициях 2 и 4 "
    "из исходного порядка и проверяет оставшиеся товары и Sub-Total."
)
def test_cart_state_after_removing_even_items(driver: WebDriver, base_url: str) -> None:
    home_page = HomePage(driver, base_url)
    product_page = ProductPage(driver, base_url)
    cart_page = CartPage(driver, base_url)
    added_products: list[dict[str, str | int | Decimal]] = []

    with allure.step("Открыть главную страницу сайта и получить список уникальных товаров"):
        home_page.open(base_url)
        unique_products = home_page.get_unique_product_links()
        assert len(unique_products) >= 5, (
            f"Ожидалось минимум 5 уникальных товаров на главной, найдено: {len(unique_products)}"
        )

    candidate_products = unique_products[:]
    random.shuffle(candidate_products)

    for selected_product in candidate_products:
        if len(added_products) == 5:
            break

        product_number = len(added_products) + 1

        with allure.step(f"Открыть страницу товара-кандидата для позиции #{product_number}"):
            home_page.open_product_by_href(selected_product["href"])
            assert "product_id" in product_page.get_current_url(), (
                f"Ожидалось открытие страницы товара, получен URL: {product_page.get_current_url()}"
            )

        with allure.step(f"Проверить, что товар для позиции #{product_number} можно добавить без выбора опций"):
            if product_page.has_product_options():
                continue

        with allure.step(f"Попробовать добавить товар для позиции #{product_number} в корзину"):
            max_quantity = product_page.get_quantity_limit() or 15
            quantity = random.randint(1, min(15, max_quantity))
            product_data = {
                "name": product_page.get_product_name(),
                "price": product_page.get_product_price(),
                "quantity": quantity,
            }
            product_page.set_quantity(quantity)
            product_page.add_to_cart()

            # Считаем товар успешно добавленным только если в корзине появилась новая строка.
            expected_rows_count = len(added_products) + 1
            actual_rows_count = cart_page.get_rows_count()

            if actual_rows_count == expected_rows_count:
                added_products.append(product_data)

        if len(added_products) < 5:
            with allure.step("Вернуться на главную страницу через навигационное меню HOME"):
                home_page.open(base_url)
                assert "automationteststore.com" in home_page.get_current_url(), (
                    f"Ожидалось возвращение на главную страницу, получен URL: {home_page.get_current_url()}"
                )

    assert len(added_products) == 5, (
        f"Не удалось добавить 5 уникальных товаров в корзину. Успешно добавлено: {len(added_products)}"
    )

    with allure.step("Открыть корзину и проверить исходный состав из 5 товаров"):
        home_page.open_cart_from_navigation()
        rows_count = cart_page.get_rows_count()
        assert rows_count == 5, f"Ожидалось 5 товаров в корзине, найдено: {rows_count}"

        cart_rows = cart_page.get_rows()
        initial_names = [cart_page.get_row_name(row) for row in cart_rows]
        initial_products = {
            cart_page.get_row_name(row): cart_page.get_row_quantity(row)
            for row in cart_rows
        }

        for product_data in added_products:
            assert product_data["name"] in initial_products, (
                f"Товар '{product_data['name']}' не найден в корзине. Текущие товары: {initial_names}"
            )
            assert product_data["quantity"] == initial_products[product_data["name"]], (
                f"Для товара '{product_data['name']}' ожидалось количество {product_data['quantity']}, "
                f"получено: {initial_products[product_data['name']]}"
            )

    removed_names = [initial_names[1], initial_names[3]]
    expected_remaining_names = [initial_names[0], initial_names[2], initial_names[4]]

    # Удаляем товары по именам из исходного порядка строк: сначала бывшую позицию 4, потом бывшую позицию 2.
    with allure.step("Удалить товар, который был на позиции 4 в исходном порядке"):
        cart_page.remove_row_by_name(removed_names[1])
        rows_count_after_fourth_remove = cart_page.get_rows_count()
        assert rows_count_after_fourth_remove == 4, (
            f"После удаления бывшей позиции 4 ожидалось 4 товара в корзине, найдено: {rows_count_after_fourth_remove}"
        )

    with allure.step("Удалить товар, который был на позиции 2 в исходном порядке"):
        cart_page.remove_row_by_name(removed_names[0])
        rows_count_after_second_remove = cart_page.get_rows_count()
        assert rows_count_after_second_remove == 3, (
            f"После удаления бывшей позиции 2 ожидалось 3 товара в корзине, найдено: {rows_count_after_second_remove}"
        )

    with allure.step("Проверить, что в корзине остались бывшие позиции 1, 3 и 5"):
        remaining_rows = cart_page.get_rows()
        remaining_names = [cart_page.get_row_name(row) for row in remaining_rows]

        assert remaining_names == expected_remaining_names, (
            f"Ожидался порядок товаров {expected_remaining_names}, получен: {remaining_names}"
        )

        for removed_name in removed_names:
            assert removed_name not in remaining_names, (
                f"Удаленный товар '{removed_name}' остался в корзине. Текущие товары: {remaining_names}"
            )

    with allure.step("Проверить корректность значения Sub-Total после удаления товаров"):
        expected_sub_total = sum(cart_page.get_row_totals())
        actual_sub_total = cart_page.get_sub_total()

        assert abs(actual_sub_total - expected_sub_total) <= Decimal("0.01"), (
            f"Sub-Total рассчитан неверно. Ожидалось: {expected_sub_total}, получено: {actual_sub_total}"
        )
