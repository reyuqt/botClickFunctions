from webdriver_click_functions.mouse import click_image, click_at_coordinates


def test_click_at_coordinates(driver, button_box, input_box):
    x, y = button_box.center()
    click_at_coordinates(target=(x, y), duration_range=(1, 3))
    last_clicked = driver.execute_script("return window.lastClickedElement;")
    assert last_clicked == 'test-button-1'

    x, y = input_box.center()
    click_at_coordinates(target=(x, y), duration_range=(1, 3))
    last_clicked = driver.execute_script("return window.lastClickedElement;")
    assert last_clicked == 'test-input'


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
