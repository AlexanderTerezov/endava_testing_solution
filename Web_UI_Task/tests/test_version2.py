import sys

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.chrome.options import Options as ChromeOptions

from selenium.webdriver.remote.webdriver import WebDriver


from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from pages.menu_page import MenuComponent

from factories.user_info_factory import CheckoutInfoFactory

#Scenario 1
def test_scenario_1(driver: WebDriver, env: dict[str, str]):

    base_url = env["base_url"]

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
    assert menu_page.is_logged_out(), "Logout unsuccessful - login button not found"

    print("Scenario 1 test completed successfully!")


#Scenario 2
def test_scenario_2(driver: WebDriver, env:  dict[str, str]):

    base_url = env["base_url"]


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


TESTS_DICT = {
    "test_scenario_1": test_scenario_1,
    "test_scenario_2": test_scenario_2,
}

def generate_html_report(results: dict[str, tuple[bool, str]]):
    html_content = """
    <html><head><title>Test Report</title></head><body>
    <h1>Test Execution Report</h1>
    <table border="1" cellpadding="5" cellspacing="0">
        <tr><th>Test Name</th><th>Status</th><th>Details</th></tr>
    """
    for test_name, (passed, details) in results.items():
        color = "green" if passed else "red"
        status = "PASS" if passed else "FAIL"
        html_content += f"<tr><td>{test_name}</td><td style='color:{color}'>{status}</td><td>{details}</td></tr>"\
    
    html_content += "</table></body></html>"

    with open("test_report.html", "w") as f:
        f.write(html_content)
    print("HTML report generated: test_report.html")

def get_driver(args, width = 1920, height = 1080):

    if len(args) > 1:
        if args[1].lower() in ["chrome", "firefox"]:
            browser = args[1]
            args = args[2:]
        else:
            print("Invalid browser. Choosing default: firefox")
            browser = "firefox"
            args = args[1:]
    else:
        print("No browser specified. Choosing default: firefox")
        browser = "firefox"
        args = args[1:]

    if browser == "chrome":
        
        options = ChromeOptions()
        options.add_argument("--incognito")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--no-default-browser-check")
        options.add_argument("--disable-blink-features=AutomationControlled")

        prefs = {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "profile.default_content_setting_values.notifications": 2,
            "profile.default_content_setting_values.popups": 2,
        }
        options.add_experimental_option("prefs", prefs)
        driver = webdriver.Chrome(options=options)
    elif browser == "firefox":
        driver =  webdriver.Firefox()
    else:
        raise ValueError(f"Unsupported browser: {browser}")
    
    driver.set_window_size(width, height)

    return driver, args

def get_environment(args):
    environments = {
        "dev": {"base_url": "https://www.saucedemo.com/"},
        "testing": {"base_url": "https://www.saucedemo.com/"},
        "staging": {"base_url": "https://www.saucedemo.com/"}
    }

    if len(args) > 0:

        if args[0] not in environments:
            print("Incorrect environment selected. Using default one: dev")
            return args[0:], "dev", environments["dev"]
        else:
            return args[1:], args[0], environments[args[0]]
    else:
        print(f"No environment selected. Using default one: dev")
        return args, "dev", environments["dev"]



results = {}

### python -m tests.test_version2 [browser] [environment] [scenarios]
if __name__ == "__main__":

    args = sys.argv
    
    driver, args = get_driver(args, 1920, 1080)


    args, env_name, environment = get_environment(args)
    base_url = environment["base_url"]

    tests = args if len(args) > 0 else "all"
    selected_tests = TESTS_DICT.keys() if tests == "all" else tests
    print(f"Selected Tests: {selected_tests}")


    try:
        for test in selected_tests:
            test_func = TESTS_DICT.get(test)
            if not test_func:
                print(f"Test '{test}' not found")
                results[test] = (False, "Test not found")
                continue

            print(f"Running {test} in environment \"{env_name}\"...")
            try:
                test_func(driver, environment)
                results[test] = (True, "Test passed successfully")
            except Exception as e:
                print(f"{test} failed: {str(e)}")
                results[test] = (False, str(e))
    finally:
        driver.quit()

    generate_html_report(results)
