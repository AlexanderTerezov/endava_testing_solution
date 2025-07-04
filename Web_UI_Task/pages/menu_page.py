from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver


class MenuComponent:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.menu_button = (By.ID, "react-burger-menu-btn")
        self.logout_button = (By.ID, "logout_sidebar_link")
        self.reset_button = (By.ID, "reset_sidebar_link")
        self.close_menu_button = (By.ID, "react-burger-cross-btn")

    def open_menu(self):
        self.driver.find_element(*self.menu_button).click()

    def logout(self):
        self.open_menu()
        logout = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.logout_button)
        )

        logout.click()

    def is_logged_out(self) -> bool:
        return self.driver.find_element(By.ID, "login-button").is_displayed()

    def reset_app_state(self):
        self.open_menu()
        self.driver.find_element(*self.reset_button).click()

    def close_menu(self):
        self.driver.find_element(*self.close_menu_button).click()