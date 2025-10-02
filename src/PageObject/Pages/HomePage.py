# src/PageObject/Pages/HomePage.py
from selenium.webdriver.common.by import By
from src.PageObject.Base.BasePage import BasePage

class HomePage(BasePage):
    URL = "https://www.linkedin.com/"

    REJECT_COOKIES = (By.CSS_SELECTOR, "button[data-control-name='ga-cookie.consent.deny.v4']")
    JOBS_LINK = (By.CSS_SELECTOR, "a[data-tracking-control-name='guest_homepage-basic_guest_nav_menu_jobs']")
    SEARCH_BAR = (By.CSS_SELECTOR, "input[placeholder='United States']")


    def open(self):
        self.driver.get(self.URL)

    def reject_cookies(self):
        if self.exists(self.REJECT_COOKIES, timeout=5):
            self.click(self.REJECT_COOKIES)

    def go_to_jobs(self):
        self.click(self.JOBS_LINK)

    def clean_search_bar(self):
        if self.exists(self.SEARCH_BAR, timeout=5):
            self.click(self.SEARCH_BAR)
            self.send_keys(self.SEARCH_BAR, "")