import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager

class TestSauceDemoStore:
    
    @pytest.fixture(autouse=True)
    def setup(self):
        
        self.driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
        self.driver.maximize_window()
        self.driver.get("https://www.saucedemo.com/")
        self.wait = WebDriverWait(self.driver, 10)
        yield
        self.driver.quit()
    
    def test_purchase_total(self):
        driver = self.driver
        wait = self.wait
        
        username_field = wait.until(EC.presence_of_element_located((By.ID, "user-name")))
        password_field = driver.find_element(By.ID, "password")
        login_button = driver.find_element(By.ID, "login-button")
        
        username_field.send_keys("standard_user")
        password_field.send_keys("secret_sauce")
        login_button.click()
        
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "inventory_item")))
        
      
        items_to_add = [
            "Sauce Labs Backpack",
            "Sauce Labs Bolt T-Shirt", 
            "Sauce Labs Onesie"
        ]
        
        for item_name in items_to_add:
          
            add_button = driver.find_element(
                By.XPATH, f"//div[text()='{item_name}']/ancestor::div[@class='inventory_item']//button"
            )
            add_button.click()
      
        cart_icon = driver.find_element(By.CLASS_NAME, "shopping_cart_link")
        cart_icon.click()
        
        checkout_button = wait.until(EC.element_to_be_clickable((By.ID, "checkout")))
        checkout_button.click()
       
        wait.until(EC.presence_of_element_located((By.ID, "first-name")))
        
        
        first_name_field = driver.find_element(By.ID, "first-name")
        last_name_field = driver.find_element(By.ID, "last-name")
        postal_code_field = driver.find_element(By.ID, "postal-code")
        
        first_name_field.send_keys("Анастасия")
        last_name_field.send_keys("Ряшина")
        postal_code_field.send_keys("90001")
        
    
        continue_button = driver.find_element(By.ID, "continue")
        continue_button.click()
        
     
        total_label = wait.until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='summary_total_label']"))
        )
        
        total_text = total_label.text
        total_amount = total_text.split("$")[1]  # Получаем "58.29"
        
        assert total_amount == "58.29", f"Ожидалась сумма $58.29, но получили ${total_amount}"
