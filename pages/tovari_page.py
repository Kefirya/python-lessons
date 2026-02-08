from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from pages.cart_page import CartPage


class InventoryPage(BasePage):
    """Page Object для страницы товаров/инвентаря."""
    
    CART_ICON = (By.CLASS_NAME, "shopping_cart_link")
    
    def _get_item_add_button(self, item_name):
        """
        Получить кнопку добавления товара в корзину по названию товара.
        
        Args:
            item_name (str): Название товара
            
        Returns:
            WebElement: Элемент кнопки добавления в корзину
        """
        return self.find_clickable_element(
            By.XPATH, 
            f"//div[text()='{item_name}']/ancestor::div[@class='inventory_item']//button"
        )
    
    def add_item_to_cart(self, item_name):
        """
        Добавить товар в корзину по названию.
        
        Args:
            item_name (str): Название товара для добавления
            
        Returns:
            InventoryPage: Текущий экземпляр страницы товаров
        """
        add_button = self._get_item_add_button(item_name)
        add_button.click()
        return self
    
    def go_to_cart(self):
        """
        Перейти в корзину покупок.
        
        Returns:
            CartPage: Экземпляр страницы корзины
        """
        cart_icon = self.find_clickable_element(*self.CART_ICON)
        cart_icon.click()
        return CartPage(self.driver)
