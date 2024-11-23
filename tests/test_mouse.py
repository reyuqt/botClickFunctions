import time

from selenium import webdriver
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os

from click_helper.box import Box
from click_helper.mouse import click_image, click_at_coordinates, locate_image
from click_helper.selenium_click import save_element


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


@pytest.fixture
def button_box() -> Box:
    return locate_image('test_button.png', region=None, confidence=0.8, min_confidence=0.5, retries=3)


@pytest.fixture
def input_box() -> Box:
    return locate_image('test_input.png', region=None, confidence=0.8, min_confidence=0.5, retries=3)


def test_locate_image(driver, button_box, input_box):
    driver_location = driver.find_element(By.ID, 'test-button-1').size
    assert driver_location['height'] == button_box.height
    assert driver_location['width'] == button_box.width

    driver_location = driver.find_element(By.ID, 'test-input').size
    assert driver_location['height'] == input_box.height
    assert driver_location['width'] == input_box.width


def test_click_at_coordinates(driver, button_box, input_box):
    x, y = button_box.center()
    click_at_coordinates(x=x, y=y, duration_range=(1, 5))
    last_clicked = driver.execute_script("return window.lastClickedElement;")
    assert last_clicked == 'test-button-1'

    x, y = input_box.center()
    click_at_coordinates(x=x, y=y, duration_range=(1, 5))
    last_clicked = driver.execute_script("return window.lastClickedElement;")
    assert last_clicked == 'test-input


def test_click_image(driver):
    clicked = click_image('test_button.png',
                          region=None,
                          confidence=0.8,
                          min_confidence=0.5,
                          retries=3,
                          x_reduction=0.2,
                          y_reduction=0.2,
                          duration_range=(1, 5))
    last_clicked = driver.execute_script("return window.lastClickedElement;")
    assert clicked
    assert last_clicked == 'test-button-1'

    clicked = click_image('test_input.png',
                          region=None,
                          confidence=0.8,
                          min_confidence=0.5,
                          retries=3,
                          x_reduction=0.2,
                          y_reduction=0.2,
                          duration_range=(1, 5))
    last_clicked = driver.execute_script("return window.lastClickedElement;")
    assert clicked
    assert last_clicked == 'test-input'
