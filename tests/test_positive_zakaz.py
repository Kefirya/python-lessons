import allure
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
    
    @allure.title("Полная покупка с корректным итогом")
    @allure.description("Тест проверяет полный процесс покупки с добавлением товаров в корзину и проверкой итоговой суммы")
    @allure.feature("Оформление заказа")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_complete_purchase_with_correct_total(self, driver):
        
        # Шаг 1: Авторизация
        with allure.step("Авторизация пользователя"):
            login_page = LoginPage(driver)
            inventory_page = login_page.login_as_standard_user()
        
        # Шаг 2: Добавление товаров в корзину
        with allure.step("Добавление товаров в корзину"):
            inventory_page.add_item_to_cart("Sauce Labs Backpack") \
                .add_item_to_cart("Sauce Labs Bolt T-Shirt") \
                .add_item_to_cart("Sauce Labs Onesie")
        
        # Шаг 3: Переход в корзину
        with allure.step("Переход в корзину"):
            cart_page = inventory_page.go_to_cart()
        
        # Проверка 1: Количество товаров в корзине
        with allure.step("Проверка количества товаров в корзине"):
            actual_count = cart_page.get_cart_items_count()
            assert actual_count == 3, \
                f"Ожидалось 3 товара в корзине, фактически: {actual_count}"
        
        # Шаг 4: Начало оформления заказа
        with allure.step("Начало оформления заказа"):
            checkout_page = cart_page.checkout()
        
        # Шаг 5: Заполнение информации о доставке
        with allure.step("Заполнение информации о доставке"):
            checkout_page.fill_shipping_info("Анастасия", "Ряшина", "90001") \
                .continue_to_overview()
        
        # Проверка 2: Итоговая сумма
        with allure.step("Проверка итоговой суммы"):
            total_amount = checkout_page.get_total_amount()
            assert total_amount == "58.29", \
                f"Ожидаемый результат $58.29, фактический результат ${total_amount}"
