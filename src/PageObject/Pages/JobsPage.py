# src/PageObject/Pages/JobsPage.py
from selenium.webdriver.common.by import By
from src.PageObject.Base.BasePage import BasePage
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time


class JobsPage(BasePage):
    JOB_LIST = (By.CSS_SELECTOR, "div.job-search-card")
    DISMISS_MODAL = (By.CSS_SELECTOR, "button.modal__dismiss")
    SEE_MORE_BUTTON = (By.CSS_SELECTOR, "button.infinite-scroller__show-more-button")
    KEYWORDS_INPUT = (By.ID, "job-search-bar-keywords")
    LOCATION_INPUT = (By. ID, "job-search-bar-location")
    EXPERIENCE_LEVEL_DROPDOWN = (By.XPATH, "//button[normalize-space()='Experience level' or normalize-space()='Nivel de experiencia']")
    INTERNSHIP_EXPERIENCE = (By. ID, "f_E-0")
    ENTRY_LEVEL_EXPERIENCE = (By. ID, "f_E-1")
    ASSOCIATE_EXPERIENCE = (By. ID, "f_E-2")
    MID_SENIOR_EXPERIENCE = (By. ID, "f_E-3")
    DIRECTOR_EXPERIENCE = (By. ID, "f_E-4")
    SUBMIT_BUTTON_EXPERIENCE = (By.XPATH, "//button[@data-tracking-control-name='public_jobs_f_E' and not(@hidden)]")


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

    def replace_job_location(self, keyword, job_location, experience_level="entry", date_posted="any"):
        """
        Construir la URL de búsqueda incluyendo:
        - keyword
        - job_location
        - nivel de experiencia (f_E)
        - fecha de publicación (f_TPR)
        """

        # Valores correctos según LinkedIn real
        experience_map = {
            "internship": "1",
            "entry": "2",
            "associate": "3",
            "mid-senior": "4",
            "director": "5",
        }

        date_map = {
            "any": "",
            "past_24_hours": "r86400",
            "past_week": "r604800",
            "past_month": "r2592000",
        }

        keyword_param = keyword.replace(" ", "%20")
        location_param = job_location.replace(" ", "%20")
        experience_param = experience_map.get(experience_level.lower(), "1")
        date_param = date_map.get(date_posted.lower(), "")


        url = (
            f"https://www.linkedin.com/jobs/search?"
            f"keywords={keyword_param}&"
            f"location={location_param}&"
            f"f_E={experience_param}&"
            f"geoId=&trk=public_jobs_jobs-search-bar_search-submit"
        )

        if date_param:
            url += f"&f_TPR={date_param}"

        url += "&position=1&pageNum=0"

        print(f"🔗 Navegando a URL filtrada: {url}")
        self.driver.get(url)
        time.sleep(5)