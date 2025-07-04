from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement


class CartPage:
    def __init__(self, driver: WebDriver):
        self.driver = driver

        self.cart_item = (By.CLASS_NAME, "cart_item")
        self.checkout_button = (By.ID, "checkout")
        self.continue_shopping_button = (By.ID, "continue-shopping")

    def get_contents(self) -> list[WebElement]:
        return self.driver.find_elements(*self.cart_item)
    
    def get_cart_item_names(self) -> list[str]:
        return [item.find_element(By.CLASS_NAME, "inventory_item_name").text for item in self.get_contents()]
    
    def remove_item(self, index: int):
        items = self.get_contents()
        button = items[index].find_element(By.TAG_NAME, "button")
        button.click()

    def continue_shopping(self):
        self.driver.find_element(*self.continue_shopping_button).click()

    def click_checkout(self):
        self.driver.find_element(*self.checkout_button).click()