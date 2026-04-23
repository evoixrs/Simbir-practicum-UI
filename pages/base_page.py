from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    def __init__(self, driver, base_url=None, timeout=10):
        self.driver = driver
        self.base_url = base_url
        self.timeout = timeout

    def open(self, url):
        self.driver.get(url)

    def go_back(self, times=1):
        for _ in range(times):
            self.driver.back()

    def find_element(self, locator):
        return WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located(locator)
        )

    def find_elements(self, locator):
        return WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_all_elements_located(locator)
        )

    def wait_for_visible(self, locator):
        return WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(locator)
        )

    def click(self, locator):
        element = WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable(locator)
        )
        element.click()

    def input(self, locator, text):
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator):
        return self.find_element(locator).text.strip()

    def get_elements_text(self, locator):
        return [element.text.strip() for element in self.find_elements(locator)]
