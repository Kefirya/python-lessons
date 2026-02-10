from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CheckoutPage(BasePage):
    """Page Object для страницы оформления заказа."""
    
    FIRST_NAME_INPUT = (By.ID, "first-name")
    LAST_NAME_INPUT = (By.ID, "last-name")
    POSTAL_CODE_INPUT = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    TOTAL_LABEL = (By.XPATH, "//div[@class='summary_total_label']")
    
    def fill_shipping_info(self, first_name, last_name, postal_code):
        """
        Заполнить информацию о доставке.
        
        Args:
            first_name (str): Имя покупателя
            last_name (str): Фамилия покупателя
            postal_code (str): Почтовый индекс
            
        Returns:
            CheckoutPage: Текущий экземпляр страницы оформления заказа
        """
        self.find_element(*self.FIRST_NAME_INPUT).send_keys(first_name)
        self.find_element(*self.LAST_NAME_INPUT).send_keys(last_name)
        self.find_element(*self.POSTAL_CODE_INPUT).send_keys(postal_code)
        return self
    
    def continue_to_overview(self):
        """
        Перейти к обзору заказа после заполнения информации о доставке.
        
        Returns:
            CheckoutPage: Текущий экземпляр страницы оформления заказа
        """
        self.find_clickable_element(*self.CONTINUE_BUTTON).click()
        return self
    
    def get_total_amount(self):
        """
        Получить общую сумму заказа.
        
        Returns:
            str: Общая сумма заказа в виде строки (без символа валюты)
        """
        total_label = self.find_element(*self.TOTAL_LABEL)
        total_text = total_label.text
        return total_text.split("$")[1] if "$" in total_text else total_text
