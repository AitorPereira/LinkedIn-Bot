# src/PageObject/Base/BasePage.py
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def click(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def get_element(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def get_elements(self, locator):
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    def get_text(self, locator):
        return self.get_element(locator).text
    
    def get_text_from_element(self, parent, locator):
        return parent.find_element(*locator).text

    def exists(self, locator, timeout=5):
        try:
            WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(locator))
            return True
        except:
            return False