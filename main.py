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

def scroll_and_click(elem):
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", elem)
    elem.click()

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
    scroll_and_click(people)
    one = wait.until(EC.element_to_be_clickable((By.XPATH,"//button[text()='1st']")))
    one.click()
    sec = wait.until(EC.element_to_be_clickable((By.XPATH,"//button[text()='2nd']")))
    sec.click()
    third = wait.until(EC.element_to_be_clickable((By.XPATH,"//button[text()='3rd+']")))
    third.click()

def open_all_filters():
    all_filters_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='All filters']")))
    scroll_and_click(all_filters_btn)

def click_all_checkboxes():
    time.sleep(2)
    checkboxes = driver.find_elements(By.XPATH, "//input[@type='checkbox']")
    print(f"Total checkboxes found: {len(checkboxes)}")

    for checkbox in checkboxes:
        try:
            checkbox_id = checkbox.get_attribute("id")
            if checkbox_id:
                label = driver.find_element(By.XPATH, f"//label[@for='{checkbox_id}']")
                driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", label)
                label.click()
                time.sleep(0.1)  
        except Exception as e:
            print(f"Error clicking checkbox: {e}")


login()
search()
filters()
open_all_filters()
click_all_checkboxes()
show = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Show results')]")))
scroll_and_click(show)
time.sleep(60)
driver.quit()
