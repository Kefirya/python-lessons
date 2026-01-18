import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

class TestSlowCalculator:
    
    @pytest.fixture(autouse=True)
    def setup(self):
   
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.driver.maximize_window()
        self.driver.get("https://bonigarcia.dev/selenium-webdriver-java/slow-calculator.html")
        self.wait = WebDriverWait(self.driver, 50)  
        yield
     
        self.driver.quit()
    
    def test_slow_calculator(self):
        
        driver = self.driver
        wait = self.wait

        delay_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#delay")))
        delay_input.clear()
        delay_input.send_keys("45")

        btn_7 = driver.find_element(By.XPATH, "//span[text()='7']")
        btn_7.click()

        btn_plus = driver.find_element(By.XPATH, "//span[text()='+']")
        btn_plus.click()

        btn_8 = driver.find_element(By.XPATH, "//span[text()='8']")
        btn_8.click()

        btn_equals = driver.find_element(By.XPATH, "//span[text()='=']")
        btn_equals.click()
        
        result_display = driver.find_element(By.CSS_SELECTOR, ".screen")
        
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, ".screen"), "15"))
        
        final_result = result_display.text
        assert final_result == "15", f"Ожидался результат 15, но получили {final_result}"
