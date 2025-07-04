from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.remote.webdriver import WebDriver


class CheckoutPage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        
        self.first_name_input = (By.ID, "first-name")
        self.last_name_input = (By.ID, "last-name")
        self.postal_code_input = (By.ID, "postal-code")
        self.continue_button = (By.ID, "continue")
        self.finish_button = (By.ID, "finish")
        self.success_message = (By.CLASS_NAME, "complete-header")

    def enter_checkout_info(self, first_name: str, last_name: str, postal_code: str):
        self.driver.find_element(*self.first_name_input).send_keys(first_name)
        self.driver.find_element(*self.last_name_input).send_keys(last_name)
        self.driver.find_element(*self.postal_code_input).send_keys(postal_code)
        self.driver.find_element(*self.continue_button).click()

    def finish_order(self):
        self.driver.find_element(*self.finish_button).click()

    def is_order_successful(self) -> bool:
        success_text = self.driver.find_element(*self.success_message).text
        return "Thank you for your order!" in success_text