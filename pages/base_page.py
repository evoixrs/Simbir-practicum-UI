from typing import TypeAlias

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait


Locator: TypeAlias = tuple[str, str]


class BasePage:
    def __init__(self, driver: WebDriver, base_url: str | None = None, timeout: int = 10) -> None:
        self.driver = driver
        self.base_url = base_url
        self.timeout = timeout

    def open(self, url: str) -> None:
        self.driver.get(url)

    def go_back(self, times: int = 1) -> None:
        for _ in range(times):
            self.driver.back()

    def find_element(self, locator: Locator) -> WebElement:
        return WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located(locator)
        )

    def find_elements(self, locator: Locator) -> list[WebElement]:
        return WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_all_elements_located(locator)
        )

    def wait_for_visible(self, locator: Locator) -> WebElement:
        return WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(locator)
        )

    def click(self, locator: Locator) -> None:
        element = WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable(locator)
        )
        element.click()

    def click_inner_element(self, element: WebElement, locator: Locator) -> None:
        element.find_element(*locator).click()

    def input(self, locator: Locator, text: str) -> None:
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)

    def input_inner_element(self, element: WebElement, locator: Locator, text: str) -> None:
        inner_element = element.find_element(*locator)
        inner_element.clear()
        inner_element.send_keys(text)

    def press_enter(self, locator: Locator) -> None:
        self.find_element(locator).send_keys(Keys.ENTER)

    def get_current_url(self) -> str:
        return self.driver.current_url

    def get_page_text(self) -> str:
        return self.find_element((By.TAG_NAME, "body")).text.strip()

    def get_text(self, locator: Locator) -> str:
        return self.find_element(locator).text.strip()

    def get_element_text(self, element: WebElement) -> str:
        return element.text.strip()

    def get_inner_element_text(self, element: WebElement, locator: Locator) -> str:
        return element.find_element(*locator).text.strip()

    def get_elements_text(self, locator: Locator) -> list[str]:
        return [element.text.strip() for element in self.find_elements(locator)]

    def get_element_attribute(self, locator: Locator, attribute: str) -> str | None:
        return self.find_element(locator).get_attribute(attribute)

    def get_element_attribute_value(self, element: WebElement, attribute: str) -> str | None:
        return element.get_attribute(attribute)

    def get_inner_element_attribute(self, element: WebElement, locator: Locator, attribute: str) -> str | None:
        return element.find_element(*locator).get_attribute(attribute)

    def get_inner_elements_text(self, element: WebElement, locator: Locator) -> list[str]:
        return [inner_element.text.strip() for inner_element in element.find_elements(*locator)]

    def select_by_value(self, locator: Locator, value: str) -> None:
        Select(self.find_element(locator)).select_by_value(value)

    def hover(self, locator: Locator) -> None:
        ActionChains(self.driver).move_to_element(self.find_element(locator)).perform()
