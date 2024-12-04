from selenium.webdriver.common.by import By
def test_locate_image(driver, button_box, input_box):
    """ check the coords of the driver versus the coords our locate_image returns """
    driver_location = driver.find_element(By.ID, 'test-button-1').size
    assert driver_location['height'] == button_box.height
    assert driver_location['width'] == button_box.width

    driver_location = driver.find_element(By.ID, 'test-input').size
    assert driver_location['height'] == input_box.height
    assert driver_location['width'] == input_box.width