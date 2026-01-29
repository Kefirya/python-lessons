import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from pages.calculator_page import CalculatorPage


class TestCalculatorPositive:   
    @pytest.fixture
    def driver(self):
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        driver.maximize_window()
        yield driver
        driver.quit()
    
    @pytest.fixture
    def calculator(self, driver):
        return CalculatorPage(driver)
    
    def test_slow_calculator_addition(self, calculator):
        
      calculator.open()
       
      calculator.set_delay(20)
       
      calculator.perform_calculation(7, "+", 8)
        
      calculator.wait_for_result("15")
        
        result = calculator.get_result()
        assert result == "14", f"Правильный результат 14, получен результат {result}"
