import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from pages.calculator_page import CalculatorPage


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
    
    def test_calculator_without_delay_setting(self, calculator):
    
        
        calculator.perform_calculation(7, "+", 7)
      
        try:
            calculator.wait_for_result("15", timeout=5)
            result = calculator.get_result()
            assert result == "14", f"Получен результат {result}"
      
  
    def test_calculator_invalid_input(self, calculator):
      
        calculator.open()
        
        calculator.set_delay("abc")
        
        calculator.perform_calculation(7, "+", 7)
        
        calculator.wait_for_result("14", timeout=10)
        result = calculator.get_result()
        assert result == "14", f"Правильный результат 14, полученный результат {result}"
