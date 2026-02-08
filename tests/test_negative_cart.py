import allure
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
    
    @allure.step("Проверка количества товаров в корзине")
    def _verify_empty_cart(self, cart_page):
        cart_items_count = cart_page.get_cart_items_count()
        assert cart_items_count == 0, \
            f"Корзина должна быть пустой, но содержит {cart_items_count} товаров"
        return cart_items_count
    
    @allure.step("Проверка состояния кнопки Checkout")
    def _verify_checkout_button_state(self, cart_page):
        try:
            from selenium.common.exceptions import TimeoutException
            checkout_button = cart_page.find_clickable_element(
                cart_page.CHECKOUT_BUTTON[0], 
                cart_page.CHECKOUT_BUTTON[1]
            )
            
            if checkout_button.is_enabled():
                return "active", "Кнопка Checkout должна быть неактивна при пустой корзине"
            else:
                return "inactive", "Кнопка Checkout неактивна - корректное поведение"
                
        except TimeoutException:
            return "not_found", "Кнопка Checkout не найдена (возможно скрыта или недоступна при пустой корзине)"
    
    @allure.title("Оформление заказа с пустой корзиной")
    @allure.description("Тест проверяет корректность обработки попытки оформления заказа с пустой корзиной")
    @allure.feature("Обработка пустой корзины")
    @allure.severity(allure.severity_level.NORMAL)
    def test_checkout_with_empty_cart(self, driver):
        
        # Авторизация
        with allure.step("Авторизация стандартного пользователя"):
            login_page = LoginPage(driver)
            inventory_page = login_page.login_as_standard_user()
        
        # Переход в корзину
        with allure.step("Переход в корзину"):
            cart_page = inventory_page.go_to_cart()
        
        # Проверка пустой корзины
        items_count = self._verify_empty_cart(cart_page)
        allure.attach(f"Количество товаров: {items_count}", 
                     name="Количество товаров", 
                     attachment_type=allure.attachment_type.TEXT)
        
        # Проверка кнопки Checkout
        button_state, message = self._verify_checkout_button_state(cart_page)
        allure.attach(f"Состояние кнопки: {button_state}\nСообщение: {message}", 
                     name="Состояние кнопки Checkout", 
                     attachment_type=allure.attachment_type.TEXT)
        
        # Если кнопка активна - это ошибка
        if button_state == "active":
            pytest.fail(message)
        
        # Завершение
        with allure.step("Завершение теста"):
            final_msg = f"Негативный тест пройден: {message}"
            allure.attach(final_msg, 
                         name="Результат теста", 
                         attachment_type=allure.attachment_type.TEXT)
            print(final_msg)
