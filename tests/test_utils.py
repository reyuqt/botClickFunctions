import time

from selenium import webdriver
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os

from click_helper.box import Box
from click_helper.utils import click_image, click_at_coordinates, locate_image


@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
    driver.get(f"file://{os.getcwd()}/test.html")
    yield driver
    driver.quit()


@pytest.fixture
def image_box() -> Box:
    return locate_image('test_button.png', region=None, confidence=0.8, min_confidence=0.5, retries=3)

def test_locate_image(driver, image_box):
    driver_location = driver.find_element(By.ID, 'test-button-1')


def test_click_at_coordinates(image_box):
    x, y = image_box.center()
    click_at_coordinates(x=x, y=y, duration_range=(1, 5))
    time.sleep(1)
    last_clicked = driver.execute_script("return window.lastClickedElement;")
    time.sleep(1)
    assert last_clicked == 'test-button-1'



def test_click_image(driver):
    clicked = click_image('test_button.png',
                          region=None,
                          confidence=0.8,
                          min_confidence=0.5,
                          retries=3,
                          x_reduction=0.2,
                          y_reduction=0.2,
                          duration_range=(1, 5))
    assert clicked
