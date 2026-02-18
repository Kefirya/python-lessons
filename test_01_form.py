import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeDriverManager

class TestFormValidation:
    
    @pytest.fixture(autouse=True)
    def setup(self):
        self.driver = webdriver.Edge(service=EdgeService(EdgeDriverManager().install()))
        self.driver.maximize_window()
        self.driver.get("https://bonigarcia.dev/selenium-webdriver-java/data-types.html")
        self.wait = WebDriverWait(self.driver, 10)
        yield
        self.driver.quit()
    
    def test_form_validation(self):
        driver = self.driver
        wait = self.wait
        
        test_data = {
            "first-name": "Иван",
            "last-name": "Петров",
            "address": "Ленина, 55-3",
            "e-mail": "test@skypro.com",
            "phone": "+7985899998787",
            "zip-code": "",  # Оставляем пустым для проверки ошибки
            "city": "Москва",
            "country": "Россия",
            "job-position": "QA",
            "company": "SkyPro"
        }
      
        for field_id, value in test_data.items():
            element = wait.until(EC.element_to_be_clickable((By.ID, field_id)))
            element.clear()
            element.send_keys(value)
        
        submit_btn = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[@type='submit']")
        ))
        submit_btn.click()
        
        wait.until(EC.invisibility_of_element_located(
            (By.XPATH, "//button[@type='submit' and not(@disabled)]")
        ))
        

        zip_code_field = wait.until(EC.presence_of_element_located((By.ID, "zip-code")))
        zip_code_classes = zip_code_field.get_attribute("class")
        assert "danger" in zip_code_classes, "Поле Zip code должно быть подсвечено красным"
  
        green_fields_ids = [
            "first-name", "last-name", "address", "e-mail",
            "phone", "city", "country", "job-position", "company"
        ]
        
        for field_id in green_fields_ids:
            field = driver.find_element(By.ID, field_id)
            field_classes = field.get_attribute("class")
            assert "success" in field_classes, f"Поле {field_id} должно быть подсвечено зеленым"
