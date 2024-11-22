import time

from selenium import webdriver
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os
from click_helper.selenium_click import get_element, click_image, click_this_element


@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
    driver.get(f"file://{os.getcwd()}/test.html")
    yield driver
    driver.quit()

def test_get_element(driver):
    button = get_element(driver, (By.ID, 'test-button-1'))
    assert button is not None


def test_click_this_element(driver):
    time.sleep(3)
    clicked = click_this_element(driver, (By.ID, 'test-button-1'))
    assert clicked