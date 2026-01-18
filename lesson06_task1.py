from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()

try:
    driver.get("http://uitestingplayground.com/ajax")
    
    blue_button = driver.find_element(By.ID, "ajaxButton")
    blue_button.click()
    
    green_alert = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, "bg-success"))
    )
    
    alert_text = green_alert.text
    
    print(alert_text)
    
    import time
    time.sleep(2)
    
except Exception as e:
    print(f"Ошибка: {e}")
    
finally:
    driver.quit()
