import logging
import os
import shutil
import tempfile
from collections.abc import Generator

import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.webdriver import WebDriver

from config.urls import BASE_URL


logger = logging.getLogger("qa")


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption("--base-url", action="store", default=BASE_URL,
        help="Base URL of test stand")
    parser.addoption("--headless", action="store_true", default=False,
        help="Run Chrome in headless mode")


@pytest.fixture
def base_url(request: pytest.FixtureRequest) -> str:
    url = request.config.getoption("--base-url")
    logger.info("Base URL: %s", url)
    return url


@pytest.fixture
def driver(request: pytest.FixtureRequest) -> Generator[WebDriver, None, None]:
    options = Options()
    options.page_load_strategy = "eager"

    options.add_argument("--disable-notifications")
    options.add_argument("--disable-background-networking")
    options.add_argument("--disable-sync")
    options.add_argument("--metrics-recording-only")
    options.add_argument("--disable-default-apps")
    options.add_argument("--no-first-run")
    options.add_argument("--disable-component-update")
    options.add_argument("--disable-features=MediaRouter")

    profile_dir = None

    is_headless = request.config.getoption("--headless")
    logger.info("Start browser. Headless = %s", is_headless)

    if is_headless:
        profile_dir = tempfile.mkdtemp(prefix="chrome-headless-")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--headless=new")

        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--remote-debugging-port=0")
        options.add_argument(f"--user-data-dir={profile_dir}")

    service = Service(
        service_args=["--verbose"],
        log_output=f"chromedriver-{os.getpid()}.log",
    )

    driver = webdriver.Chrome(service=service, options=options)

    driver.set_page_load_timeout(20)

    if not is_headless:
        driver.maximize_window()

    driver.implicitly_wait(0)
    logger.info("Chrome started successfully")

    yield driver

    logger.info("Test finished. Closing browser")
    driver.quit()

    if profile_dir:
        shutil.rmtree(profile_dir, ignore_errors=True)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(
    item: pytest.Item,
    call: pytest.CallInfo[None],
) -> Generator[None, None, None]:
    outcome = yield
    report = outcome.get_result()

    if report.when != "call" or report.passed:
        return

    driver = item.funcargs.get("driver")
    if driver is None:
        return

    try:
        allure.attach(
            driver.get_screenshot_as_png(),
            name="failure-screenshot",
            attachment_type=allure.attachment_type.PNG,
        )
    except Exception as exc:
        logger.warning("Failed to attach screenshot: %s", exc)

    try:
        allure.attach(
            driver.page_source,
            name="page-source",
            attachment_type=allure.attachment_type.HTML,
        )
    except Exception as exc:
        logger.warning("Failed to attach page source: %s", exc)
