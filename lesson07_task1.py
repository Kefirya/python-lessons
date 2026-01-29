import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

class CalculatorPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 50)
    
    def open(self):
        self.driver.get("https://bonigarcia.dev/selenium-webdriver-java/slow-calculator.html")
        return self
    
    def set_delay(self, seconds):
        delay_input = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#delay")))
        delay_input.clear()
        delay_input.send_keys(str(seconds))
        return self
    
    def click_button(self, button_text):
        button = self.driver.find_element(By.XPATH, f"//span[text()='{button_text}']")
        button.click()
        return self
    
    def get_result(self):
        result_display = self.driver.find_element(By.CSS_SELECTOR, ".screen")
        return result_display.text
    
    def wait_for_result(self, expected_result):
        self.wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, ".screen"), str(expected_result)))
        return self

class TestCalculatorWithPageObject:
    
    @pytest.fixture(autouse=True)
    def setup(self):
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.driver.maximize_window()
        yield
        self.driver.quit()
    
    def test_slow_calculator(self):
        calculator_page = CalculatorPage(self.driver)
        
        calculator_page.open() \
            .set_delay(45) \
            .click_button("7") \
            .click_button("+") \
            .click_button("7") \
            .click_button("=") \
            .wait_for_result("14")
        
        result = calculator_page.get_result()
        assert result == "15", f"Ожидаемый результат: 15, фактический результат: {result}"
