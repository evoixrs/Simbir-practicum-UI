from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


"""Класс с общими действиями для всех page object"""
class BasePage:
    def __init__(self, driver, base_url=None, timeout=10):
        """Сохраняем driver, базовый URL и общий timeout ожиданий"""
        self.driver = driver
        self.base_url = base_url
        self.timeout = timeout

    """Открывает страницу по переданному URL"""
    def open(self, url):
        self.driver.get(url)

    """Ожидает появления одного элемента в DOM и возвращает его"""
    def find_element(self, locator):
        return WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located(locator)
        )

    """Ожидает появления списка элементов в DOM и возвращает его"""
    def find_elements(self, locator):
        return WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_all_elements_located(locator)
        )

    """Ожидает, что элемент стал видимым на странице"""
    def wait_for_visible(self, locator):
        return WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(locator)
        )

    """Ожидает кликабельность элемента и кликает по нему"""
    def click(self, locator):
        element = WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable(locator)
        )
        element.click()

    """Возвращает очищенный текст одного элемента"""
    def get_text(self, locator):
        return self.find_element(locator).text.strip()

    """Возвращает список очищенных текстов найденных элементов"""
    def get_elements_text(self, locator):
        return [element.text.strip() for element in self.find_elements(locator)]
