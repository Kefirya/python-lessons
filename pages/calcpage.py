from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class CalculatorPage(BasePage):
    """Page Object для страницы калькулятора."""
    
    DELAY_INPUT = (By.CSS_SELECTOR, "#delay")
    SCREEN_DISPLAY = (By.CSS_SELECTOR, ".screen")

    def get_delay_input(self):
        """
        Получить поле ввода задержки.
        
        Returns:
            WebElement: Элемент поля ввода задержки
        """
        return self.find_element(*self.DELAY_INPUT)
    
    def get_screen_display(self):
        """
        Получить элемент экрана калькулятора.
        
        Returns:
            WebElement: Элемент экрана с результатом
        """
        return self.find_element(*self.SCREEN_DISPLAY)
    
    def get_calculator_button(self, button_text):
        """
        Получить кнопку калькулятора по тексту.
        
        Args:
            button_text (str): Текст на кнопке
            
        Returns:
            WebElement: Элемент кнопки калькулятора
        """
        return self.find_clickable_element(By.XPATH, f"//span[text()='{button_text}']")
    
    def open(self):
        """
        Открыть страницу калькулятора.
        
        Returns:
            CalculatorPage: Текущий экземпляр страницы
        """
        self.driver.get("https://bonigarcia.dev/selenium-webdriver-java/slow-calculator.html")
        return self
    
    def set_delay(self, seconds):
        """
        Установить задержку вычисления.
        
        Args:
            seconds (str|int): Количество секунд задержки
            
        Returns:
            CalculatorPage: Текущий экземпляр страницы
        """
        delay_input = self.get_delay_input()
        delay_input.clear()
        delay_input.send_keys(str(seconds))
        return self
    
    def click_button(self, button_text):
        """
        Нажать на кнопку калькулятора.
        
        Args:
            button_text (str): Текст на кнопке
            
        Returns:
            CalculatorPage: Текущий экземпляр страницы
        """
        button = self.get_calculator_button(button_text)
        button.click()
        return self
    
    def perform_calculation(self, a, operator, b):
        """
        Выполнить математическую операцию: a operator b =
        
        Args:
            a (int|float|str): Первое число
            operator (str): Математический оператор (+, -, *, /)
            b (int|float|str): Второе число
            
        Returns:
            CalculatorPage: Текущий экземпляр страницы
        """
        self.click_button(str(a))
        self.click_button(operator)
        self.click_button(str(b))
        self.click_button("=")
        return self
    
    def get_result(self):
        """
        Получить текущий результат с экрана калькулятора.
        
        Returns:
            str: Текст результата
        """
        return self.get_screen_display().text
    
    def wait_for_result(self, expected_result, timeout=50):
        """
        Ожидать появления ожидаемого результата на экране.
        
        Args:
            expected_result (str|int): Ожидаемый результат
            timeout (int): Максимальное время ожидания в секундах
            
        Returns:
            CalculatorPage: Текущий экземпляр страницы
            
        Raises:
            TimeoutException: Если результат не появился за указанное время
        """
        wait = WebDriverWait(self.driver, timeout)
        wait.until(
            EC.text_to_be_present_in_element(self.SCREEN_DISPLAY, str(expected_result))
        )
        return self
