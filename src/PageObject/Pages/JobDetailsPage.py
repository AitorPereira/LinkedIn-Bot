# src/PageObject/Pages/JobDetailsPage.py
from selenium.webdriver.common.by import By
from src.PageObject.Base.BasePage import BasePage
import time

class JobDetailsPage(BasePage):
    TITLE = (By.CSS_SELECTOR, "h2.top-card-layout__title")
    TITLE_LINK = (By.CSS_SELECTOR, "a.base-card__full-link")
    COMPANY = (By.CSS_SELECTOR, "a.topcard__org-name-link")
    LOCATION = (By.CSS_SELECTOR, "span.topcard__flavor--bullet")
    DATE = (By.CSS_SELECTOR, "span.posted-time-ago__text")
    SHOW_MORE = (By.XPATH, "//button[@aria-label='Show more']")
    DESCRIPTION = (By.CSS_SELECTOR, "div.show-more-less-html__markup")

    def get_job_info(self, job_card):
        try:
            title = job_card.find_element(By.CSS_SELECTOR, "span.sr-only").text
        except:
            title = "N/A"

        try:
            link = job_card.find_element(By.CSS_SELECTOR, "a.base-card__full-link").get_attribute("href")
        except:
            link = "N/A"

        try:
            company = job_card.find_element(By.CSS_SELECTOR, "a.topcard__org-name-link").text
        except:
            company = "N/A"

        try:
            location = job_card.find_element(By.CSS_SELECTOR, "span.job-search-card__location").text
        except:
            location = "N/A"

        try:
            date = job_card.find_element(By.CSS_SELECTOR, "time").text
        except:
            date = "N/A"

        return {
            "title": title,
            "link": link,
            "company": company,
            "location": location,
            "date": date
        }

        # if not self.exists(self.TITLE, timeout=5):
        #     return None
        # if not self.exists(self.COMPANY, timeout=5):
        #     return None

        # title = self.get_text(self.TITLE)
        # link = self.get_element(self.TITLE_LINK).get_attribute("href") #if self.exists(self.TITLE_LINK, 3) else "N/A"
        # company = self.get_text(self.COMPANY)
        # location = self.get_text(self.LOCATION) if self.exists(self.LOCATION, 3) else "N/A"
        # date = self.get_text(self.DATE) if self.exists(self.DATE, 3) else "N/A"

        # return {"title": title, "link": link, "company": company, "location": location, "date": date}

    def expand_description(self):
        if self.exists(self.SHOW_MORE, timeout=3):
            self.click(self.SHOW_MORE)
            time.sleep(1)

    def get_description(self):
        return self.get_text(self.DESCRIPTION) if self.exists(self.DESCRIPTION, 5) else ""