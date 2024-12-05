from selenium.webdriver.common.by import By
from webdriver_click_functions.selenium.click import get_element, click_this_element, save_element, \
    click_inside_this_element
from webdriver_click_functions.selenium.confirm import Clicked


def test_clicked_default(driver):
    clicked = click_this_element(driver, selector=(By.ID, 'test-button-1'),
                                 confidence=0.8, perform_test=Clicked.default
                                 )
    assert clicked


def test_clicked_selected(driver):
    clicked = click_this_element(driver, selector=(By.ID, 'test-button-1'),
                                 confidence=0.8, perform_test=Clicked.selected
                                 )
    assert clicked
