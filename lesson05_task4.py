from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Firefox()

try:
    driver.get("http://the-internet.herokuapp.com/login")
    
    # 3. В поле username ввести значение tomsmith
    driver.find_element(By.ID, "username").send_keys("tomsmith")
    

    driver.find_element(By.ID, "password").send_keys("SuperSecretPassword!")
    
  
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    

    

    flash_message = driver.find_element(By.ID, "flash")
    print(flash_message.text.replace("×", "").strip())
    
finally:
    driver.quit()
