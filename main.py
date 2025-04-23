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
    time.sleep(3)

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

    skip_ids = [
        "advanced-filter-geoUrn-101022442",
        "advanced-filter-currentCompany-4477",
        "advanced-filter-currentCompany-6148",
        "advanced-filter-currentCompany-1441",
        "advanced-filter-currentCompany-1073",
        "advanced-filter-currentCompany-4476",
        "advanced-filter-pastCompany-4477",
        "advanced-filter-pastCompany-6148",
        "advanced-filter-pastCompany-1441",
        "advanced-filter-pastCompany-1073",
        "advanced-filter-pastCompany-1038",
        "advanced-filter-schoolFilter-4476",
        "advanced-filter-industry-1810",
        "advanced-filter-industry-43",
        "advanced-filter-profileLanguage-de",
        "advanced-filter-profileLanguage-es",
        "advanced-filter-profileLanguage-fr",
        "advanced-filter-profileLanguage-pt",
        "advanced-filter-openToVolunteer-true",
        "advanced-filter-serviceCategory-220",
        "advanced-filter-serviceCategory-50413",
        "advanced-filter-serviceCategory-63",
        "advanced-filter-serviceCategory-55800",
        "advanced-filter-serviceCategory-2461"
    ]

    for checkbox in checkboxes:
        try:
            checkbox_id = checkbox.get_attribute("id")
            if checkbox_id in skip_ids:
                continue
            if checkbox_id:
                label = driver.find_element(By.XPATH, f"//label[@for='{checkbox_id}']")
                driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", label)
                label.click()
                time.sleep(0.1)
        except Exception as e:
            print(f"Error clicking checkbox: {e}")

def scroll_to_load():
    scroll_pause = 2
    screen_height = driver.execute_script("return window.innerHeight")
    scroll_height = driver.execute_script("return document.body.scrollHeight")

    current_position = 0
    while current_position < scroll_height:
        driver.execute_script(f"window.scrollTo(0, {current_position});")
        time.sleep(scroll_pause)
        current_position += screen_height
        scroll_height = driver.execute_script("return document.body.scrollHeight")

def getLinks(driver, wait):
    # wait for at least one real-profile anchor to appear
    try:
        wait.until(EC.presence_of_element_located((
            By.CSS_SELECTOR,
            "li.ZEMKWShUEvptWlRHdUwqKAevVHDrTs a[data-test-app-aware-link]"
        )))
    except:
        print("No profile links found on page.")
        return []

    time.sleep(3)   # give JS a moment to finish rendering

    anchors = driver.find_elements(
        By.CSS_SELECTOR,
        "li.ZEMKWShUEvptWlRHdUwqKAevVHDrTs a[data-test-app-aware-link]"
    )

    profile_links = []
    for a in anchors:
        raw = a.get_attribute("href") or ""
        clean = raw.split('?')[0]
        if "/in/" in clean and clean not in profile_links:
            profile_links.append(clean)

    print(f"Found {len(profile_links)} profile URLs:")
    for link in profile_links:
        print(link)

    return profile_links

login()
search()
filters()
open_all_filters()
click_all_checkboxes()

show = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Show results')]")))
scroll_and_click(show)
time.sleep(5)
while True:
    scroll_to_load()
    profiles =  getLinks(driver, wait)

    try:
        next_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Next']")))
        if next_button.is_enabled():
            print("Going to next page...")
            scroll_and_click(next_button)
            time.sleep(5)
        else:
            print("Next button is disabled. Stopping.")
            break
    except Exception as e:
        print("No more pages or error finding next button:", e)
        break

print("Finished scraping.")
driver.quit()
