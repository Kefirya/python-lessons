from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CalculatorPage(BasePage):

    DELAY_INPUT = (By.CSS_SELECTOR, "#delay")
    SCREEN_DISPLAY = (By.CSS_SELECTOR, ".screen")

    def get_delay_input(self):
        return self.find_element(*self.DELAY_INPUT)
    
    def get_screen_display(self):
        return self.find_element(*self.SCREEN_DISPLAY)
    
    def get_calculator_button(self, button_text):
        return self.find_clickable_element(By.XPATH, f"//span[text()='{button_text}']")
    
    def open(self):
        self.driver.get("https://bonigarcia.dev/selenium-webdriver-java/slow-calculator.html")
        return self
    
    def set_delay(self, seconds):
        delay_input = self.get_delay_input()
        delay_input.clear()
        delay_input.send_keys(str(seconds))
        return self
    
    def click_button(self, button_text):
        button = self.get_calculator_button(button_text)
        button.click()
        return self
    
    def perform_calculation(self, a, operator, b):
        """
        Выполнить расчет: a operator b =
        
        Args:
            a: Первое число
            operator: Оператор (+, -, *, /)
            b: Второе число
        """
        self.click_button(str(a))
        self.click_button(operator)
        self.click_button(str(b))
        self.click_button("=")
        return self
    
    def get_result(self):
        return self.get_screen_display().text
    
    def wait_for_result(self, expected_result, timeout=50):
        wait = WebDriverWait(self.driver, timeout)
        wait.until(
            EC.text_to_be_present_in_element(self.SCREEN_DISPLAY, str(expected_result))
        )
        return self
