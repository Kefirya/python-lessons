from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()

try:
    driver.get("https://bonigarcia.dev/selenium-webdriver-java/loading-images.html")
   
    WebDriverWait(driver, 15).until(
        lambda d: len(d.find_elements(By.CSS_SELECTOR, "#image-container img")) >= 4
    )
    

    images = driver.find_elements(By.CSS_SELECTOR, "#image-container img")
    
  
    if len(images) > 2:
        third_image_src = images[2].get_attribute("src")
        print(third_image_src)
       
        print(f"\nИнформация о 3-й картинке:")
        print(f"Index: 2 ")
        print(f"Атрибут src: {third_image_src}")
        print(f"Атрибут alt: {images[2].get_attribute('alt')}")
        print(f"Размеры: {images[2].size}")
        
    else:
        print(f"Недостаточно изображений. Найдено: {len(images)}")
    
finally:
    driver.quit()
