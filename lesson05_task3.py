from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_input_field():
    driver = webdriver.Firefox()  # Убедитесь, что geckodriver установлен
    
    try:
    
     
        driver.get("http://the-internet.herokuapp.com/inputs")

        input_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "input"))
        )
   
   
        input_field.send_keys("Sky")
        
    
       
        input_field.clear()
        
   
        
 
        input_field.send_keys("Pro")
        
     sleep(2)
        
    
        current_value = input_field.get_attribute("value")
        print(f"✓ Текущее значение поля: '{current_value}'")
    
        
    except Exception as e:
        print(f"✗ Произошла ошибка: {e}")
       
        driver.save_screenshot(f"firefox_error_{__import__('time').time()}.png")
        
    finally:
      
        driver.quit()

if __name__ == "__main__":
    test_input_field()
