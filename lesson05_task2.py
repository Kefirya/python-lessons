# lesson05_task2.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_dynamic_button():
  
    driver = webdriver.Chrome() 
    
    try:
             driver.get("http://uitestingplayground.com/dynamicid")
        blue_button_xpath = "//button[contains(@class, 'btn-primary')]"
        
      
     
        blue_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, blue_button_xpath))
        )
        
        
        blue_button.click()
        print("✓ Скрипт выполнен")
        
    except Exception as e:
        print(f"✗ Произошла ошибка: {e}")
        driver.save_screenshot(f"error_screenshot_{__import__('time').time()}.png")
        
    finally:
        # Закрываем браузер
        driver.quit()

if __name__ == "__main__":
    test_dynamic_button()
