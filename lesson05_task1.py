
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


driver = webdriver.Chrome() 

try:
 
    driver.get("http://uitestingplayground.com/classattr")
    

    blue_button_xpath = "//button[contains(concat(' ', normalize-space(@class), ' '), ' btn-primary ')]"
    
 
    blue_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, blue_button_xpath))
    )
    blue_button.click()
    
   
    WebDriverWait(driver, 5).until(EC.alert_is_present())
    alert = driver.switch_to.alert
    alert.accept() 
    
except Exception as e:
    print(f"Ошибка: {e}")
    
finally:
    driver.quit()
