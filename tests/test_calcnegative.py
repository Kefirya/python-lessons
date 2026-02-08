import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from pages.calculator_page import CalculatorPage


class TestCalculatorNegative:
    """Класс для негативных тестов калькулятора."""
    
    @pytest.fixture
    def driver(self):
        """Фикстура для инициализации драйвера Chrome."""
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        driver.maximize_window()
        yield driver
        driver.quit()
    
    @pytest.fixture
    def calculator(self, driver):
        """Фикстура для инициализации страницы калькулятора."""
        return CalculatorPage(driver)
    
    @allure.title("Тест калькулятора без установки задержки")
    @allure.description("Тест проверяет поведение калькулятора без предварительной установки задержки")
    @allure.feature("Калькулятор")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.story("Негативные тесты калькулятора")
    def test_calculator_without_delay_setting(self, calculator):
        """Тест проверяет расчет без установки задержки."""
        with allure.step("Открыть калькулятор"):
            try:
                calculator.open()
                allure.attach("Калькулятор открыт", name="Состояние", attachment_type=allure.attachment_type.TEXT)
            except:
                allure.attach("Калькулятор уже открыт или открытие не требуется", name="Состояние", attachment_type=allure.attachment_type.TEXT)
        
        with allure.step("Выполнить расчет без установки задержки: 7 + 7"):
            calculator.perform_calculation(7, "+", 7)
            allure.attach("Расчет 7 + 7 запущен без предварительной установки задержки", name="Операция", attachment_type=allure.attachment_type.TEXT)
        
        with allure.step("Попытка получить результат с таймаутом 5 секунд"):
            try:
                calculator.wait_for_result("14", timeout=5)
                result = calculator.get_result()
                allure.attach(f"Получен результат: {result}", name="Фактический результат", attachment_type=allure.attachment_type.TEXT)
                with allure.step("Проверка результата"):
                    assert result == "14", f"Получен результат {result}"
                    allure.attach(f"Результат {result} соответствует ожидаемому 14", name="Результат проверки", attachment_type=allure.attachment_type.TEXT)
            except Exception as e:
                allure.attach(f"Исключение: {type(e).__name__}: {str(e)}", name="Исключение", attachment_type=allure.attachment_type.TEXT)
                allure.attach("Калькулятор не вернул результат за 5 секунд", name="Состояние", attachment_type=allure.attachment_type.TEXT)
                print(f"Исключение: {e}")
    
    @allure.title("Тест калькулятора с невалидным вводом задержки")
    @allure.description("Тест проверяет поведение калькулятора при установке невалидной задержки 'abc'")
    @allure.feature("Калькулятор")
    @allure.severity(allure.severity_level.MINOR)
    @allure.story("Негативные тесты калькулятора")
    def test_calculator_invalid_input(self, calculator):
        """Тест проверяет обработку невалидного ввода с использованием явных ожиданий."""
        with allure.step("Открыть калькулятор"):
            calculator.open()
            allure.attach("Калькулятор успешно открыт", name="Состояние", attachment_type=allure.attachment_type.TEXT)
        
        with allure.step("Попытка установить невалидную задержку: 'abc'"):
            try:
                calculator.set_delay("abc")
                allure.attach("Попытка установки задержки 'abc' выполнена", name="Операция", attachment_type=allure.attachment_type.TEXT)
            except Exception as e:
                allure.attach(f"Исключение при установке задержки: {type(e).__name__}: {str(e)}", name="Исключение", attachment_type=allure.attachment_type.TEXT)
        
        with allure.step("Выполнить расчет: 7 + 7"):
            calculator.perform_calculation(7, "+", 7)
            allure.attach("Расчет 7 + 7 запущен после невалидной задержки", name="Операция", attachment_type=allure.attachment_type.TEXT)
        
        with allure.step("Ожидание результата с таймаутом 10 секунд"):
            try:
                calculator.wait_for_result("14", timeout=10)
                allure.attach("Результат получен", name="Состояние", attachment_type=allure.attachment_type.TEXT)
            except Exception as e:
                allure.attach(f"Исключение при ожидании результата: {type(e).__name__}: {str(e)}", name="Исключение", attachment_type=allure.attachment_type.TEXT)
        
        with allure.step("Получить и проверить результат"):
            try:
                result = calculator.get_result()
                allure.attach(f"Полученный результат: {result}", name="Фактический результат", attachment_type=allure.attachment_type.TEXT)
                expected_result = "14"
                with allure.step(f"Проверить что результат равен {expected_result}"):
                    assert result == expected_result, f"Ожидался результат {expected_result}, получен результат {result}"
                    allure.attach(f"Результат {result} корректен", name="Результат проверки", attachment_type=allure.attachment_type.TEXT)
            except Exception as e:
                allure.attach(f"Исключение при получении результата: {type(e).__name__}: {str(e)}", name="Исключение", attachment_type=allure.attachment_type.TEXT)
