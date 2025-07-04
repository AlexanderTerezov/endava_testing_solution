from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement



class InventoryPage:
    def __init__(self, driver: WebDriver):
        self.driver = driver

        self.inventory_item = (By.CLASS_NAME, "inventory_item")
        self.cart_button = (By.CLASS_NAME, "shopping_cart_link")
        self.product_sort_container = (By.CLASS_NAME, "product_sort_container")

    def get_items(self) -> list[WebElement]:
        return self.driver.find_elements(*self.inventory_item)

    def add_to_cart_by_index(self, index: int) -> str:
        items = self.get_items()
        button = items[index].find_element(By.TAG_NAME, "button")

        if button.text.lower() == "add to cart":
            button.click()
        else:
            print(f"Item at index {index} is already in cart.")
        
        return items[index].find_element(By.CLASS_NAME, "inventory_item_name ").text


    def remove_from_cart_by_index(self, index: int):
        items = self.get_items()
        button = items[index].find_element(By.TAG_NAME, "button")

        if button.text.lower() == "remove":
            button.click()
        else:
            print(f"Item at index {index} can't be removed, beacuse it is not in cart.")

    def sort_by_price_hilo(self):
        select_element = self.driver.find_element(*self.product_sort_container)
        Select(select_element).select_by_value("hilo")
    
    def get_item_prices(self) -> list[float]:
            return [float(item.find_element(By.CLASS_NAME, "inventory_item_price").text.replace("$", "")) for item in self.get_items()]


    def go_to_cart(self):
        self.driver.find_element(*self.cart_button).click()