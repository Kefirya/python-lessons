import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    def open(self):
        self.driver.get("https://www.saucedemo.com/")
        return self
    
    def login_as_standard_user(self):

        username_field = self.wait.until(EC.presence_of_element_located((By.ID, "user-name")))
        password_field = self.driver.find_element(By.ID, "password")
        login_button = self.driver.find_element(By.ID, "login-button")
        
        username_field.send_keys("standard_user")
        password_field.send_keys("secret_sauce")
        login_button.click()
        
        return InventoryPage(self.driver)


class InventoryPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    def add_to_cart(self, item_name):
        add_button = self.driver.find_element(
            By.XPATH, f"//div[text()='{item_name}']/ancestor::div[@class='inventory_item']//button"
        )
        add_button.click()
        return self
    
    def go_to_cart(self):
        cart_icon = self.driver.find_element(By.CLASS_NAME, "shopping_cart_link")
        cart_icon.click()
        return CartPage(self.driver)

class CartPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    def checkout(self):
        checkout_button = self.wait.until(EC.element_to_be_clickable((By.ID, "checkout")))
        checkout_button.click()
        return CheckoutPage(self.driver)

class CheckoutPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    def fill_form(self, first_name, last_name, postal_code):
        first_name_field = self.wait.until(EC.presence_of_element_located((By.ID, "first-name")))
        last_name_field = self.driver.find_element(By.ID, "last-name")
        postal_code_field = self.driver.find_element(By.ID, "postal-code")
        
        first_name_field.send_keys(first_name)
        last_name_field.send_keys(last_name)
        postal_code_field.send_keys(postal_code)
        return self
    
    def continue_to_overview(self):
        continue_button = self.driver.find_element(By.ID, "continue")
        continue_button.click()
        return CheckoutOverviewPage(self.driver)

class CheckoutOverviewPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    def get_total_amount(self):
        total_label = self.wait.until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='summary_total_label']"))
        )
        total_text = total_label.text
        return total_text.split("$")[1] 


class TestSauceDemoStoreWithPageObject:
    
    @pytest.fixture(autouse=True)
    def setup(self):
        self.driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
        self.driver.maximize_window()
        yield
        self.driver.quit()
    
    def test_complete_purchase(self):
        login_page = LoginPage(self.driver)
        inventory_page = login_page.open().login_as_standard_user()
        
        inventory_page.add_to_cart("Sauce Labs Backpack") \
            .add_to_cart("Sauce Labs Bolt T-Shirt") \
            .add_to_cart("Sauce Labs Onesie")
        
        cart_page = inventory_page.go_to_cart()
        checkout_page = cart_page.checkout()
        
        checkout_page.fill_form("Анастасия", "Ряшина", "90001")
        checkout_overview_page = checkout_page.continue_to_overview()
        
        total_amount = checkout_overview_page.get_total_amount()
        assert total_amount == "58.29", f"Ожидаемая сумма $58.29, фактическая сумма ${total_amount}"
