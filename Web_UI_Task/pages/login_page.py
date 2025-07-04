from selenium.webdriver.common.by import By

from selenium.webdriver.remote.webdriver import WebDriver


class LoginPage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        
        self.username_input = (By.ID, "user-name")
        self.password_input = (By.ID, "password")
        self.login_button = (By.ID, "login-button")

        self.users_container = (By.ID, "login_credentials")
        self.password_container = (By.CLASS_NAME, "login_password")

    
    def open(self, url):
        self.driver.get(url)

    def get_username_and_pass(self) -> tuple[str, str]:
        user_container = self.driver.find_element(*self.users_container)
        pass_container = self.driver.find_element(*self.password_container)

        users = user_container.text.splitlines()[1:]
        
        passwords = pass_container.text.splitlines()[1:]

        return (users[0], passwords[0])

    def login(self, username: str, password: str):
        self.driver.find_element(*self.username_input).send_keys(username)
        self.driver.find_element(*self.password_input).send_keys(password)
        self.driver.find_element(*self.login_button).click()