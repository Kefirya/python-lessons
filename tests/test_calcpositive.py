import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from pages.calculator_page import CalculatorPage


class TestCalculatorPositive:
    """Класс для позитивных тестов калькулятора."""
    
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
    
    @allure.step("Открыть калькулятор")
    def _open_calculator(self, calculator):
        """Открывает страницу калькулятора."""
        calculator.open()
        return "Калькулятор успешно открыт"
    
    @allure.step("Выполнить расчет: {a} {operator} {b}")
    def _perform_calculation_step(self, calculator, a, operator, b):
        """Выполняет математическую операцию в калькуляторе."""
        calculator.perform_calculation(a, operator, b)
        return f"Расчет {a} {operator} {b} запущен"
    
    @allure.step("Ожидать результат: {expected}")
    def _wait_for_result(self, calculator, expected, timeout=30):
        """Ожидает появления ожидаемого результата с заданным таймаутом."""
        calculator.wait_for_result(expected, timeout)
        return f"Ожидается результат: {expected}"
    
    @allure.step("Проверить результат")
    def _verify_result(self, calculator, expected):
        """Проверяет корректность полученного результата."""
        result = calculator.get_result()
        allure.attach(f"Фактический результат: {result}", name="Результат", attachment_type=allure.attachment_type.TEXT)
        assert result == expected, f"Ожидался результат {expected}, получен результат {result}"
        return "Результат корректный"
    
    @allure.title("Тестирование сложения с медленным калькулятором")
    @allure.description("Тест проверяет сложение чисел с установленной задержкой в 20 секунд")
    @allure.feature("Калькулятор")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("Положительные тесты калькулятора")
    def test_slow_calculator_addition(self, calculator):
        """Тест сложения с использованием явных ожиданий вместо time.sleep()."""
        open_status = self._open_calculator(calculator)
        allure.attach(open_status, name="Открытие", attachment_type=allure.attachment_type.TEXT)
        
        calc_status = self._perform_calculation_step(calculator, 7, "+", 8)
        allure.attach(calc_status, name="Расчет", attachment_type=allure.attachment_type.TEXT)
        
        wait_status = self._wait_for_result(calculator, "15", timeout=25)
        allure.attach(wait_status, name="Ожидание", attachment_type=allure.attachment_type.TEXT)
        
        verify_status = self._verify_result(calculator, "15")
        allure.attach(verify_status, name="Проверка", attachment_type=allure.attachment_type.TEXT)
