from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.remote.webdriver import WebDriver


from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from pages.menu_page import MenuComponent

from factories.user_info_factory import CheckoutInfoFactory

BASE_URL = "https://www.saucedemo.com/"

#Scenario 1
def test_scenario_1(driver: WebDriver, base_url: str):
    print("Running scenario 1...")
    #Initiallizing pages
    login_page = LoginPage(driver)
    inventory_page = InventoryPage(driver)
    cart_page = CartPage(driver)
    checkout_page = CheckoutPage(driver)
    menu_page = MenuComponent(driver)

    #Log in with standard user
    login_page.open(base_url)
    (username, password) = login_page.get_username_and_pass()
    login_page.login(username, password)

    #Assert check if logged
    assert "inventory" in driver.current_url.lower(), "Couldn't log in"

    #Add first and last 
    item1 = inventory_page.add_to_cart_by_index(0)
    item2 = inventory_page.add_to_cart_by_index(-1)

    #Verify items in cart
    inventory_page.go_to_cart()
    items_in_cart = cart_page.get_cart_item_names()

    assert len(items_in_cart) == 2, f"Expected 2 items, but got {len(items_in_cart)}"
    assert item1 in items_in_cart and item2 in items_in_cart,  f"Cart items {items_in_cart} don't match expected {[item1, item2]}"

    #Remove first and add second to last
    cart_page.continue_shopping()
    assert "inventory" in driver.current_url.lower(), "Couldn't click continue shopping"

    inventory_page.remove_from_cart_by_index(0)
    item3 = inventory_page.add_to_cart_by_index(-2)

    #Verify items in cart
    inventory_page.go_to_cart()
    items_in_cart = cart_page.get_cart_item_names()

    assert len(items_in_cart) == 2, f"Expected 2 items, but got {len(items_in_cart)}"
    assert item2 in items_in_cart and item3 in items_in_cart,  f"Cart items {items_in_cart} don't match expected {[item3, item2]}"

    #Go to checkout
    cart_page.click_checkout()
    assert "checkout" in driver.current_url.lower()

    #Finish the order
    info = CheckoutInfoFactory.get_valid_info()
    checkout_page.enter_checkout_info(**info)
    checkout_page.finish_order()

    #Check if order successful
    assert checkout_page.is_order_successful(), "Order was not successful"

    #Verify cart empty
    inventory_page.go_to_cart()
    cart_contents = cart_page.get_contents()
    assert len(cart_contents) == 0

    #Log out
    menu_page.logout()
    login_button_displayed = driver.find_element(By.ID, "login-button").is_displayed()
    assert login_button_displayed, "Logout unsuccessful - login button not found"

    print("Scenario 1 test completed successfully!")


#Scenario 2
def test_scenario_2(driver: WebDriver, base_url: str):
    print("Running Scenario 2...")

    #Initiallizing pages
    login_page = LoginPage(driver)
    inventory_page = InventoryPage(driver)
    menu_page = MenuComponent(driver)

    #Log in with standard user
    login_page.open(base_url)
    (username, password) = login_page.get_username_and_pass()
    login_page.login(username, password)

    #Assert check if logged
    assert "inventory" in driver.current_url.lower(), "Couldn't log in"

    #Sort high to low
    inventory_page.sort_by_price_hilo()
    prices = inventory_page.get_item_prices()
    assert prices == sorted(prices, reverse=True)

    #Log out
    menu_page.logout()
    login_button_displayed = driver.find_element(By.ID, "login-button").is_displayed()
    assert login_button_displayed, "Logout unsuccessful - login button not found"

    print("Scenario 2 test completed successfully!")


if __name__ == "__main__":

    #Setting up the driver
    options = FirefoxOptions()
    #options.add_argument("--headless")
    service = FirefoxService()
    driver = webdriver.Firefox(service=service, options=options)

    test_scenario_1(driver, BASE_URL)
    test_scenario_2(driver, BASE_URL)

    driver.quit()