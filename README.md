# SeleniumLinkedInBot


Small project to search for job offers on LinkedIn (e.g., "Python Developer" in "Europe"), navigate through the results, extract relevant information (title, link, company, location, date, and description), and save it to a CSV file.


> **Legal and usage notice**: Do responsible scraping. Respect LinkedIn’s terms of service and avoid aggressive or large-scale automated queries. Use this tool only for personal purposes or with proper permissions.


## Project structure
SeleniumLinkedInBot/ ├── src/ │ ├── PageObject/ │ │ ├── Pages/ │ │ │ ├── HomePage.py │ │ │ ├── JobsPage.py │ │ │ └── JobDetailsPage.py │ │ └── Base/ │ │ └── BasePage.py │ └── TestBase/ │ └── WebDriverSetup.py ├── tests/ │ └── test_linkedin_jobs.py ├── conftest.py ├── requirements.txt └── README.md

## Requirements


- Python 3.8+
- Google Chrome and ChromeDriver (compatible with your Chrome version)
- Dependencies: run:

bash
```
python -m venv .venv
source .venv/bin/activate # macOS / Linux
..venv\Scripts\activate # Windows
pip install -r requirements.txt

If you don’t have requirements.txt, install at least:
````
pip install selenium pytest
````

## Driver configuration

Currently, the chromedriver path is set in src/TestBase/WebDriverSetup.py (for example /usr/local/bin/chromedriver).

Recommendation: modify WebDriverSetup.py to read the path from an environment variable CHROMEDRIVER_PATH or use a helper like webdriver-manager.

Example (mac/linux environment):
```
# if you use webdriver-manager:
pip install webdriver-manager
````

Or make sure chromedriver is in a known path and update WebDriverSetup.py.

## Run tests / script

To run the main test (which executes the flow and generates the CSV):
```
pytest -v -s tests/test_linkedin_jobs.py
```
The output CSV is called linkedin_jobs.csv by default.

## Best practices

  -Don’t use aggressive polling (reduce time.sleep and prefer WebDriverWait).
  -Respect delays between actions and request limits to avoid being blocked.
    -If running in CI or headless environments, consider using headless Chrome or xvfb.

## Common issues

  -StaleElementReferenceException: occurs when the DOM re-renders; re-locate elements and use retries.
  -ElementClickInterceptedException/ElementNotInteractableException: use scrollIntoView or ActionChains.
  -Changing locators: review selectors and prioritize id, data-* or specific selectors.

## Contribuir
1) Fork the repo.

2) Create a feature/my-change branch.

3) Open a PR with a clear description. 

## License