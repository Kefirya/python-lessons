import pytest
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from pages.login_page import LoginPage


class TestPositiveCheckout:
    
    @pytest.fixture
    def driver(self):
        driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
        driver.maximize_window()
        yield driver
        driver.quit()
    
    def test_complete_purchase_with_correct_total(self, driver):
 
        login_page = LoginPage(driver)
        inventory_page = login_page.login_as_standard_user()
        inventory_page.add_item_to_cart("Sauce Labs Backpack") \
            .add_item_to_cart("Sauce Labs Bolt T-Shirt") \
            .add_item_to_cart("Sauce Labs Onesie")

        cart_page = inventory_page.go_to_cart()
        

        assert cart_page.get_cart_items_count() == 3, \

        checkout_page = cart_page.checkout()

        checkout_page.fill_shipping_info("Анастасия", "Ряшина", "90001") \
            .continue_to_overview()

        total_amount = checkout_page.get_total_amount()
        assert total_amount == "58.29", \
            f"Ожидаемый результат $58.29, фактический результат ${total_amount}"
        
