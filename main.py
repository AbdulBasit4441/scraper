from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

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
    scroll_pause = 1
    screen_height = driver.execute_script("return window.innerHeight")
    scroll_height = driver.execute_script("return document.body.scrollHeight")

    current_position = 0
    while current_position < scroll_height:
        driver.execute_script(f"window.scrollTo(0, {current_position});")
        time.sleep(scroll_pause)
        current_position += screen_height
        scroll_height = driver.execute_script("return document.body.scrollHeight")

def getLinks(driver, wait):
    try:
        wait.until(EC.presence_of_element_located((
            By.CSS_SELECTOR,
            "ul.OTwhyBrRIjzkDqCQWvaMgSgHXVjmkFiPnI a[data-test-app-aware-link]"
        )))
    except:
        print("No profile links found on page.")
        return []

    time.sleep(3)

    anchors = driver.find_elements(
        By.CSS_SELECTOR,
        "ul.OTwhyBrRIjzkDqCQWvaMgSgHXVjmkFiPnI a[data-test-app-aware-link]"
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

# Start Process
login()
search()
filters()
open_all_filters()
click_all_checkboxes()

show = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Show results')]")))
scroll_and_click(show)
time.sleep(5)

all_profiles = []

while True:
    scroll_to_load()
    profiles = getLinks(driver, wait)
    all_profiles.extend(profiles)

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

all_profiles = list(set(all_profiles))

#  NEW FEATURE: Check education section for "Currently Studying"
currently_studying_profiles = []

for link in all_profiles:
    driver.get(link)
    time.sleep(3)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

    try:
        edu_entries = driver.find_elements(By.XPATH, "//section[contains(@id, 'education')]//li")
        for entry in edu_entries:
            if "present" in entry.text.lower() or "currently" in entry.text.lower():
                currently_studying_profiles.append(link)
                print(f" Currently studying: {link}")
                break
    except Exception as e:
        print(f" Error checking education for {link}: {e}")

#  Save all profiles and filtered ones
df_all = pd.DataFrame({'Profile Links': all_profiles})
df_all.to_excel('linkedin_all_profiles.xlsx', index=False)

df_current = pd.DataFrame({'Currently Studying Profiles': currently_studying_profiles})
df_current.to_excel('linkedin_currently_studying_profiles.xlsx', index=False)

print(" Profile data saved successfully.")
driver.quit()
