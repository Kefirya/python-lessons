import pytest
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from pages.login_page import LoginPage


class TestNegativeEmptyCart: 
    @pytest.fixture
    def driver(self):
        driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
        driver.maximize_window()
        yield driver
        driver.quit()
    
    def test_checkout_with_empty_cart(self, driver):
 
        login_page = LoginPage(driver)
        inventory_page = login_page.login_as_standard_user()
     
        cart_page = inventory_page.go_to_cart()
 
        cart_items_count = cart_page.get_cart_items_count()
    
        assert cart_items_count == 0, \
            f"Корзина должна быть пустой, но содержит {cart_items_count} товаров"
        
   
        try:
       
            from selenium.common.exceptions import TimeoutException
            checkout_button = cart_page.find_clickable_element(
                cart_page.CHECKOUT_BUTTON[0], 
                cart_page.CHECKOUT_BUTTON[1]
            )
   
            if checkout_button.is_enabled():
                pytest.fail("Ошибка")
            else:
                print("Кнопка Checkout неактивна")
                
        except TimeoutException:
            print("Кнопка Checkout не найдена)")
        
        print("Негативный тест пройден: пустая корзина обрабатывается корректно")
