from selenium.webdriver.common.by import By
from webdriver_click_functions.selenium.click import get_element, click_this_element, save_element, \
    click_inside_this_element, ElementNotFoundError

selectors_to_test = [(By.ID, 'test-button-1'), (By.ID, 'test-input')]


def test_get_element(driver):
    for selector in selectors_to_test:
        button = get_element(driver, selector)
        assert button is not None


def test_element_does_not_exist(driver):
    try:
        get_element(driver, (By.ID, 'made-up-id'), timeout=2)
        assert False
    except ElementNotFoundError:
        assert True


def test_save_element(driver):
    for selector in selectors_to_test:
        element = driver.find_element(*selector)
        file_path = save_element(element, name='test-button-1')
        assert 'test-button-1' in file_path


def test_click_this_element(driver):
    for selector in selectors_to_test:
        clicked = click_this_element(driver, selector=selector,
                                     confidence=0.8,
                                     retries=3,
                                     x_reduction=0.2,
                                     y_reduction=0.2,
                                     duration_range=(1, 3),
                                     )
        last_clicked = driver.execute_script("return window.lastClickedElement;")

        assert clicked
        assert last_clicked == selector[1]


def test_click_inside_this_element(driver):
    selector_inner = (By.ID, 'test-button-nested-1')
    selector_outer = (By.ID, 'nest-1')
    clicked = click_inside_this_element(driver=driver, selector_outer=selector_outer, selector_inner=selector_inner)
    last_clicked = driver.execute_script("return window.lastClickedElement;")

    assert clicked
    assert last_clicked == selector_inner
