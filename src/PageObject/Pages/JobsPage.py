# src/PageObject/Pages/JobsPage.py
from selenium.webdriver.common.by import By
from src.PageObject.Base.BasePage import BasePage
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains
import time


class JobsPage(BasePage):
    JOB_LIST = (By.CSS_SELECTOR, "div.base-card")
    DISMISS_MODAL = (By.CSS_SELECTOR, "button.modal__dismiss")
    SEE_MORE_BUTTON = (By.CSS_SELECTOR, "button.infinite-scroller__show-more-button")
    KEYWORDS_INPUT = (By.ID, "job-search-bar-keywords")
    LOCATION_INPUT = (By. ID, "job-search-bar-location")

    def dismiss_modal(self):
        if self.exists(self.DISMISS_MODAL, timeout=5):
            self.click(self.DISMISS_MODAL)

    def get_job_cards(self):
        return self.get_elements(self.JOB_LIST)

    def click_job(self, job_card):
        self.driver.execute_script("arguments[0].scrollIntoView(true);", job_card)
        time.sleep(1)  # darle un respiro al scroll
        actions = ActionChains(self.driver)
        actions.move_to_element(job_card).click().perform()

    def load_more_jobs(self):
        if self.exists(self.SEE_MORE_BUTTON, timeout=5):
            self.click(self.SEE_MORE_BUTTON)

    def search_job(self, job_title):
        """Hace click en el input de búsqueda y escribe el job_title"""
        input_box = self.get_element(self.KEYWORDS_INPUT)
        input_box.clear()  # limpiar cualquier texto previo
        input_box.click()  # hacer click
        input_box.send_keys(job_title)

    def replace_job_location(self, keyword, job_location):
        # Construir la URL de búsqueda directamente
        keyword_param = keyword.replace(" ", "+")
        location_param = job_location.replace(" ", "+")
        url = f"https://www.linkedin.com/jobs/search?keywords={keyword_param}&location={location_param}&geoId=&trk=public_jobs_jobs-search-bar_search-submit"
        self.driver.get(url)
        time.sleep(5)  # esperar a que cargue la página

                # wait = WebDriverWait(self.driver, 10)
        # for i in range(3):
        #     try:
        #         input_box = wait.until(EC.presence_of_element_located(self.LOCATION_INPUT))
        #         input_box.clear()
        #         input_box.send_keys(job_location + Keys.ENTER)
        #         wait.until(lambda d: d.find_element(*self.LOCATION_INPUT).get_attribute("value") == job_location)
        #         break
        #     except StaleElementReferenceException:
        #         print("⚠️ El input se recargó, reintentando...")
        #         time.sleep(1)