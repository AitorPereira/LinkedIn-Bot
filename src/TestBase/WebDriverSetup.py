# src/TestBase/WebDriverSetup.py
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

@pytest.fixture(scope="class")
def setup(request):
    service = Service(executable_path="/usr/local/bin/chromedriver")
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    request.cls.driver = driver
    yield
    driver.quit()