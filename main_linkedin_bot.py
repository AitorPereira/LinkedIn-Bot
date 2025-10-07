# main_linkedin_bot.py
import time
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException, InvalidSessionIdException
from src.PageObject.Pages.HomePage import HomePage
from src.PageObject.Pages.JobsPage import JobsPage
from src.PageObject.Pages.JobDetailsPage import JobDetailsPage


# ===============================
# CONFIGURACIÓN
# ===============================
KEYWORDS_INCLUDE = ["junior", "entry", "trainee", "intern", "no experience", "sin experiencia"]
KEYWORDS_EXCLUDE = ["senior", "lead", "manager", "3 years", "4 years", "5 years"]
MAX_JOBS = 20
OUTPUT_FILE = "linkedin_jobs.csv"


# ===============================
# CONFIGURACIÓN SELENIUM
# ===============================
def init_driver(headless=True):
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    service = Service(executable_path="/usr/local/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.maximize_window()
    return driver


# ===============================
# CSV
# ===============================
def init_csv():
    """Inicializa el archivo CSV limpio con cabeceras"""
    with open(OUTPUT_FILE, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Title", "Link", "Company", "Location", "Date", "Description"])


def read_existing_jobs():
    """Lee el CSV actual y devuelve un conjunto de claves únicas (Company, Location, Date)"""
    existing = set()
    try:
        with open(OUTPUT_FILE, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                key = (row["Company"].strip().lower(), row["Location"].strip().lower(), row["Date"].strip().lower())
                existing.add(key)
    except FileNotFoundError:
        pass
    return existing


def save_job_to_csv(job_info, description):
    """Guarda una oferta en el CSV"""
    with open(OUTPUT_FILE, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            job_info["title"],
            job_info["link"],
            job_info["company"],
            job_info["location"],
            job_info["date"],
            description[:200]  # guardar los primeros 200 caracteres
        ])


# ===============================
# BOT PRINCIPAL
# ===============================
def main():
    jobs_saved = 0
    driver = init_driver(headless=True)

    home = HomePage(driver)
    jobs_page = JobsPage(driver)
    details_page = JobDetailsPage(driver)

    # Crear CSV limpio e inicializar conjunto de duplicados
    init_csv()
    seen_jobs = set()

    try:
        print("Iniciando Bot..")
        home.open()
        home.reject_cookies()
        home.go_to_jobs()
        jobs_page.dismiss_modal()

        # Aplicar filtros de búsqueda
        jobs_page.search_job("Python Developer")
        jobs_page.replace_job_location(
            "Python Developer", "Europe",
            experience_level="entry", date_posted="past_week"
        )

        while jobs_saved < MAX_JOBS:
            try:
                job_cards = jobs_page.get_job_cards()
                if not job_cards:
                    print("No hay más ofertas visibles, cargando más...")
                    jobs_page.load_more_jobs()
                    time.sleep(5)
                    continue

                for card in job_cards:
                    if jobs_saved >= MAX_JOBS:
                        break

                    try:
                        job_info = details_page.get_job_info(card)
                        if not job_info:
                            continue

                        # Crear clave de unicidad basada en company + location + date
                        job_key = (
                            job_info["company"].strip().lower(),
                            job_info["location"].strip().lower(),
                            job_info["date"].strip().lower()
                        )

                        # Evitar duplicados por company/location/date
                        if job_key in seen_jobs:
                            continue
                        seen_jobs.add(job_key)

                        # Cargar descripción
                        jobs_page.click_job(card)
                        time.sleep(2)
                        details_page.expand_description()
                        description = details_page.get_description()
                        description_lower = description.lower()

                        # Filtros de texto
                        include_ok = any(kw.lower() in description_lower for kw in KEYWORDS_INCLUDE)
                        exclude_ok = not any(kw.lower() in description_lower for kw in KEYWORDS_EXCLUDE)

                        if include_ok and exclude_ok:
                            jobs_saved += 1
                            print(f"✅ [{jobs_saved}/{MAX_JOBS}] {job_info['title']}")
                            save_job_to_csv(job_info, description)
                        else:
                            print(f"❌ Excluido: {job_info['title']}")

                    except (WebDriverException, InvalidSessionIdException):
                        print("⚠️ Error al cargar oferta, continuando...")
                        continue

                jobs_page.load_more_jobs()
                time.sleep(4)

            except (WebDriverException, InvalidSessionIdException) as e:
                print(f"⚠️ Error crítico detectado: {e}")
                print("Reiniciando driver y continuando...")
                driver.quit()
                driver = init_driver(headless=True)
                home = HomePage(driver)
                jobs_page = JobsPage(driver)
                details_page = JobDetailsPage(driver)
                home.open()
                home.reject_cookies()
                home.go_to_jobs()
                jobs_page.dismiss_modal()
                jobs_page.replace_job_location(
                    "Python Developer", "Europe",
                    experience_level="entry", date_posted="past_week"
                )
                continue

    finally:
        driver.quit()
        print(f"Bot finalizado. Total ofertas guardadas: {jobs_saved}")


# ===============================
# EJECUCIÓN
# ===============================
if __name__ == "__main__":
    main()