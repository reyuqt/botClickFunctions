import time

import pyautogui
from selenium import webdriver
import pytest
from selenium.webdriver.common.by import By
import os

from webdriver_click_functions.box import Box
from webdriver_click_functions.mouse import locate_image
from webdriver_click_functions.selenium.click import save_element


@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
    driver.get(f"file://{os.getcwd()}/test.html")
    driver.maximize_window()
    save_element(driver.find_element(By.ID, 'test-button-1'), name='test_button')
    save_element(driver.find_element(By.ID, 'test-input'), name='test_input')
    yield driver
    driver.quit()
    os.remove('test_button.png')
    os.remove('test_input.png')

@pytest.fixture(scope="module", autouse=True)
def reset_state():
    """
    Fixture to reset the system state before each test function.
    Useful when using PyAutoGUI to ensure a clean slate.
    """
    yield
    pyautogui.moveTo(0, 0, duration=0.5)
    time.sleep(0.5)

@pytest.fixture
def button_box() -> Box:
    return locate_image('test_button.png', region=None, confidence=0.8, min_confidence=0.5, retries=3)


@pytest.fixture
def input_box() -> Box:
    return locate_image('test_input.png', region=None, confidence=0.8, min_confidence=0.5, retries=3)
