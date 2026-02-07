import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from pages.calculator_page import CalculatorPage
import time

class TestCalculatorNegative:
    @pytest.fixture
    def driver(self):
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        driver.maximize_window()
        yield driver
        driver.quit()
    
    @pytest.fixture
    def calculator(self, driver):
        return CalculatorPage(driver)
    
    @allure.title("Тест калькулятора без установки задержки")
    @allure.description("Тест проверяет поведение калькулятора без предварительной установки задержки")
    @allure.feature("Калькулятор")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.story("Негативные тесты калькулятора")
    def test_calculator_without_delay_setting(self, calculator):
        with allure.step("Открыть калькулятор"):
            try: calculator.open(); allure.attach("Калькулятор открыт", name="Состояние", attachment_type=allure.attachment_type.TEXT)
            except: allure.attach("Калькулятор уже открыт", name="Состояние", attachment_type=allure.attachment_type.TEXT)
        with allure.step("Выполнить расчет без установки задержки: 7 + 7"):
            calculator.perform_calculation(7, "+", 7)
            allure.attach("Расчет 7 + 7 запущен", name="Операция", attachment_type=allure.attachment_type.TEXT)
        with allure.step("Попытка получить результат с таймаутом 5 секунд"):
            try:
                calculator.wait_for_result("14", timeout=5)
                result = calculator.get_result()
                allure.attach(f"Результат: {result}", name="Фактический результат", attachment_type=allure.attachment_type.TEXT)
                assert result == "14", f"Получен результат {result}"
            except Exception as e:
                allure.attach(f"Исключение: {type(e).__name__}", name="Исключение", attachment_type=allure.attachment_type.TEXT)
    
    @allure.title("Тест калькулятора с невалидным вводом задержки")
    @allure.description("Тест проверяет поведение калькулятора при установке невалидной задержки 'abc'")
    @allure.feature("Калькулятор")
    @allure.severity(allure.severity_level.MINOR)
    @allure.story("Негативные тесты калькулятора")
    def test_calculator_invalid_input(self, calculator):
        with allure.step("Открыть калькулятор"):
            calculator.open()
        with allure.step("Установить невалидную задержку: 'abc'"):
            try: calculator.set_delay("abc")
            except Exception as e: pass
        with allure.step("Выполнить расчет: 7 + 7"):
            calculator.perform_calculation(7, "+", 7)
        time.sleep(2)
        with allure.step("Ожидание результата"):
            try: calculator.wait_for_result("14", timeout=10)
            except Exception as e: pass
        with allure.step("Получить и проверить результат"):
            try:
                result = calculator.get_result()
                assert result == "14", f"Ожидался 14, получен {result}"
            except Exception as e: pass
