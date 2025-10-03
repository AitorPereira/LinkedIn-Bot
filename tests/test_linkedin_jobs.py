# tests/test_linkedin_jobs.py
import pytest
import time
import csv
from src.PageObject.Pages.HomePage import HomePage
from src.PageObject.Pages.JobsPage import JobsPage
from src.PageObject.Pages.JobDetailsPage import JobDetailsPage
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

KEYWORDS = ["2 years", "at least 2 years", "Machine Learning", "IA", "Analyst", "Científico", "Ingeniero"]

OUTPUT_FILE = "linkedin_jobs.csv"

@pytest.mark.usefixtures("setup")
class TestLinkedInJobs:

    def save_job_to_csv(self, job_info, description):
        """Guardar oferta en CSV"""
        with open(OUTPUT_FILE, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([
                job_info["title"],
                job_info["link"],
                job_info["company"],
                job_info["location"],
                job_info["date"],
                description[:200]
            ])

    def test_search_jobs(self):
        home = HomePage(self.driver)
        jobs = JobsPage(self.driver)
        details = JobDetailsPage(self.driver)

        # Inicializar CSV con cabeceras
        with open(OUTPUT_FILE, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Title", "Link", "Company", "Location", "Date", "Description"])

        home.open()
        home.reject_cookies()
        home.go_to_jobs()
        jobs.dismiss_modal()

        # 🔹 Aquí hacemos la búsqueda
        jobs.search_job("Python Developer")
        jobs.replace_job_location("Python Developer","Europe", experience_level="entry", date_posted="past_week")

        while True:
            job_cards = jobs.get_job_cards()

            for card in job_cards:
                try:
                    # Click en ember-view
                    jobs.click_job(card)
                    time.sleep(3)

                    job_info = details.get_job_info(card)
                    if not job_info:
                        continue

                    # Expandir descripción
                    details.expand_description()
                    description = details.get_description()

                    # Buscar palabras clave
                    if any(keyword.lower() in description.lower() for keyword in KEYWORDS):
                        print("✅ Oferta encontrada:", job_info["title"])
                        self.save_job_to_csv(job_info, description)

                except Exception as e:
                    print("⚠️ Error procesando oferta:", e)
                    continue

            # Intentar cargar más resultados
            jobs.load_more_jobs()
            time.sleep(15)