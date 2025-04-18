from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

USERNAME = "ab5129326@gmail.com"
PASSWORD = "AAbb321@"

driver = webdriver.Chrome()
driver.get("https://www.linkedin.com/login")
wait = WebDriverWait(driver, 15)

def login():
    username_input = wait.until(EC.presence_of_element_located((By.ID, "username")))
    password_input = driver.find_element(By.ID, "password")
    username_input.send_keys(USERNAME)
    password_input.send_keys(PASSWORD)
    password_input.send_keys(Keys.RETURN)

def search():
    search_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".search-global-typeahead__input")))
    search_input.send_keys("oxford university")
    search_input.send_keys(Keys.RETURN)

def filters():
    people = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='People']")))
    people.click()
    category1 =wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='1st']")))
    category1.click()
    category2 =wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='2nd']")))
    category2.click()
    category3 =wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='3rd+']")))
    category3.click()
    checkbox_label = wait.until(EC.element_to_be_clickable((By.ID, "searchFilter_geoUrn")))
    checkbox_label.click()
    location_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"input[placeholder= 'Add a location']")))
    location_input.send_keys("United Kingdom")
    checkbox_label = wait.until(EC.element_to_be_clickable((By.XPATH, "//label[@for='geoUrn-101165590']")))
    checkbox_label.click()
    apply_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button//span[text()='Show results']/..")))
    apply_button.click()

def allfilters():
    allfilter = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='All filters']")))
    allfilter.click()
    filter_panel = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@role='dialog']")))

    # === Step 4: Find and click all checkboxes inside the filter panel ===
    checkboxes = filter_panel.find_elements(By.XPATH, ".//input[@type='checkbox']")

    for checkbox in checkboxes:
        if not checkbox.is_selected():
          try:
            checkbox.click()
          except:
            # If checkbox is hidden, click the label instead
            label = checkbox.find_element(By.XPATH, "./ancestor::label")
            driver.execute_script("arguments[0].click();", label)

    show_results_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Show results')]")))
    show_results_btn.click()

       
login()
search()
filters()
allfilters()
time.sleep(60)
driver.quit()
