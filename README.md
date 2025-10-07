# 🤖 Selenium LinkedIn Bot: Pytest + Page Object Model (Version V2.)

This repository contains an automation framework built with **Selenium** and **Pytest**, designed to search job offers on **LinkedIn** (e.g., “Python Developer” in “Europe”).  
It navigates through the results, extracts relevant information (title, company, location, date, link, and description), and saves it into a CSV file.

> ⚠️ **Legal & Usage Notice**  
> Perform responsible scraping. Always respect **LinkedIn’s Terms of Service** and avoid aggressive or large-scale automated queries.  
> Use this tool **only for personal purposes** or with **explicit permission**.

---

## 🚀 Tech Stack  

**Core:** Python 3.8+  

**Libraries & Tools:**  
- Selenium → browser automation  
- Pytest → test execution & fixtures  
- WebDriver Manager → dynamic ChromeDriver setup (optional)  
- CSV → data export  

**Concepts Applied:**  
- Page Object Model (POM)  
- Dynamic element handling (WebDriverWait, retries)  
- Data extraction and file writing  
- Cross-platform execution (macOS, Linux, Windows) 

### 📂 Project Structure  

A Selenium Page Object Model (POM) project for job search automation on LinkedIn.
```
SeleniumLinkedInBot/
├── src/
│   ├── PageObject/
│   │   ├── Pages/
│   │   │   ├── HomePage.py           # LinkedIn home/search page
│   │   │   ├── JobsPage.py           # Job listings and filters
│   │   │   └── JobDetailsPage.py     # Job details extraction
│   │   └── Base/
│   │       └── BasePage.py           # Common page actions (click, send_keys, waits)
│   └── TestBase/
│       └── WebDriverSetup.py         # WebDriver setup and teardown
├── tests/
│   └── test_linkedin_jobs.py         # Main test script (job scraping + CSV export)
├── conftest.py                       # Pytest configuration and fixtures
├── requirements.txt
└── README.md
```

---

### 🔑 Key Features  

1. **Page Object Model (POM)**  
   - Encapsulates LinkedIn’s UI elements and actions for maintainability.  
   - Each page (Home, Jobs, JobDetails) has isolated responsibilities.  

2. **Automated Job Extraction**  
   - Searches LinkedIn for specific roles and regions.  
   - Extracts key job data (title, company, link, location, date, and description).  
   - Saves all results to a structured CSV file (`linkedin_jobs.csv`).  

3. **Configurable WebDriver Setup**  
   - `WebDriverSetup.py` manages driver initialization and teardown.  
   - ChromeDriver path can be set manually or dynamically via **webdriver-manager**.  

4. **Pytest-Driven Flow**  
   - Execute the entire workflow via `pytest`.  
   - Fixtures (`conftest.py`) handle setup and teardown for clean test orchestration.  

5. **Robustness & Stability**  
   - Handles common Selenium issues (stale elements, interaction errors).  
   - Encourages responsible automation with waits and delays.

---

### ⚙️ Getting Started

1. Clone the Repository
```bash
git clone https://github.com/your-username/SeleniumLinkedInBot.git
cd SeleniumLinkedInBot
```

2. Set Up Virtual Environment & Dependencies
```bash
python -m venv .venv
source .venv/bin/activate    # macOS / Linux
.venv\Scripts\activate       # Windows
pip install -r requirements.txt
```
If you don’t have a requirements.txt, install at least:
```bash
pip install selenium pytest
```

3. Configure ChromeDriver
Set the path manually in:
```
src/TestBase/WebDriverSetup.py
```
Or use webdriver-manager for automatic driver management:
```bash
pip install webdriver-manager
```
You can also export the driver path as an environment variable:
```bash
export CHROMEDRIVER_PATH=/usr/local/bin/chromedriver
```

### ▶️ Run the Script / Tests
Run the main test, which executes the scraping flow and generates the CSV:
```bash
pytest -v -s tests/test_linkedin_jobs.py
```
The output file will be created as:
```
linkedin_jobs.csv
```

### 🧩 Best Practices
  - ⏱️ Use WebDriverWait instead of time.sleep() for dynamic waits.
  - 💡 Respect delays and avoid overloading LinkedIn servers.
  - 🧱 For CI or headless environments, enable headless Chrome.
  - 🔍 Re-locate elements after DOM changes to prevent stale element errors.

### ⚠️ Common Issues & Fixes

🤝 Contributing

1️⃣ Fork the repository  
2️⃣ Create a feature branch:
```bash
git checkout -b feature/my-change
```
3️⃣ Commit your updates and push:
```bash
git push origin feature/my-change
```
4️⃣ Open a Pull Request with a clear description.

### 📜 License

This project is licensed under the MIT License.
