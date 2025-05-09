from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
import time
import re
from datetime import datetime

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
    search_input = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Search"]')))
    search_input.click()

    print("Waiting 25 seconds — you can type your search in LinkedIn and press Enter manually.")
    time.sleep(20)  

    print(" Resuming automation...")
    time.sleep(3)

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

    select_ids = [
        "advanced-filter-geoUrn-101165590",
        "advanced-filter-geoUrn-102299470",
        "advanced-filter-geoUrn-90009496",
        "advanced-filter-geoUrn-102257491",
        "advanced-filter-schoolFilter-4522",
        "advanced-filter-schoolFilter-4477",
        "advanced-filter-industry-1594",
        "advanced-filter-industry-6",
        "advanced-filter-industry-4",
        "advanced-filter-profileLanguage-en",
    ]

    for checkbox in checkboxes:
        try:
            checkbox_id = checkbox.get_attribute("id")
            if checkbox_id in select_ids:
                label = driver.find_element(By.XPATH, f"//label[@for='{checkbox_id}']")
                driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", label)
                label.click()
                time.sleep(0.1)
            if checkbox_id:
               continue
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
            By.XPATH,
            "//a[contains(@href, '/in/') and @href != '']"
        )))
    except:
        print("No profile links found on page.")
        return []

    time.sleep(3)

    anchors = driver.find_elements(
        By.XPATH,
        "//a[contains(@href, '/in/') and @href != '']"
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
def Pages():
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
currently_studying_profiles = []

Pages()

def Post():
   try:
       print("Opening filter dropdown...")

       # Step 1: Click the "People" filter dropdown button
       filter_button = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[@aria-label=' Filter by: People']")))
       filter_button.click()
       print("Filter dropdown clicked.")

       time.sleep(2)  # Let the dropdown open and render

       # Step 2: Try the precise XPath first (recommended way)
       try:
           posts_option_xpath = "//div[@role='menu']//span[text()='Posts']"
           posts_option = wait.until(EC.element_to_be_clickable((By.XPATH, posts_option_xpath)))
           driver.execute_script("arguments[0].scrollIntoView(true);", posts_option)
           driver.execute_script("arguments[0].click();", posts_option)
           print(" Successfully clicked the 'Posts' filter using precise XPath!")

       except Exception as precise_error:
           print(f" Precise XPath method failed: {precise_error}")
           print(" Falling back to generic search for any element containing 'Posts'...")

           posts_found = 0
           all_elements = driver.find_elements(By.XPATH, "//span[normalize-space(text())='Posts']")

           for elem in all_elements:
               try:
                   print(f"Found 'Posts' span: {elem.get_attribute('outerHTML')}")
                   driver.execute_script("arguments[0].scrollIntoView(true);", elem)
                   parent_button = elem.find_element(By.XPATH, "./ancestor::button")
                   driver.execute_script("arguments[0].click();", parent_button)
                   print(" Clicked the actual 'Posts' button!")
                   posts_found += 1
                   break
               except Exception as click_error:
                   print(f" Failed to click ancestor button: {click_error}")

           if posts_found == 0:
               print(" No clickable element found with exact text 'Posts'.")

   except Exception as e:
      print(f" Final error: {e}")

def post_filter():
    all_filters_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='All filters']")))
    scroll_and_click(all_filters_btn)
    # Step 2: Click the 'Latest' radio button

    time.sleep(2)
    radio = driver.find_elements(By.XPATH, "//input[@type='radio']")
    print(f"Total Radio found: {len(radio)}")

    select_ids = [
        "advanced-filter-sortBy-date_posted",
        "advanced-filter-datePosted-past-24h",
        "advanced-filter-contentType-photos",
    ]

    for r in radio:
        try:
            radio_id = r.get_attribute("id")
            if radio_id in select_ids:
                label = driver.find_element(By.XPATH, f"//label[@for='{radio_id}']")
                driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", label)
                label.click()
                time.sleep(0.1)
            if radio_id:
               continue
        except Exception as e:
            print(f"Error clicking checkbox: {e}")
    # scroll_to_load()
    show = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Show results')]")))
    show.click()
    time.sleep(2)

def scroll_check_Post():
     scroll_pause = 4
     screen_height = driver.execute_script("return window.innerHeight")
     scroll_height = driver.execute_script("return document.body.scrollHeight")

     current_position = 0
     while current_position < scroll_height:
        driver.execute_script(f"window.scrollTo(50, {current_position});")
        time.sleep(scroll_pause)
        current_position += screen_height
        scroll_height = driver.execute_script("return document.body.scrollHeight")
     try:
        wait.until(EC.presence_of_element_located((
            By.CSS_SELECTOR,
            "a[href*='/in/']"
        )))
     except:
        print("No profile links found on page.")
        return []

     time.sleep(3)

     anchors = driver.find_elements(
        By.CSS_SELECTOR,
       "a[href*='/in/']"
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

Post()   
post_filter()
scroll_check_Post()
def education():
  # Check education section for "Currently Studying"
  for link in all_profiles:
    driver.get(link)
    time.sleep(3)
    found_show_all = False

    try:
        education_link = wait.until(EC.presence_of_element_located((By.ID, "navigation-index-see-all-education")))
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", education_link)
        time.sleep(1)
        education_link.click()
        print(f"Clicked 'Show all education' on: {link}")
        found_show_all = True
        time.sleep(2)
    except Exception as e:
        print(f"'Show all education' link not found for: {link}")

    try:
        edu_entries = driver.find_elements(By.XPATH, "//section[contains(@id, 'education')]//li")
        for entry in edu_entries:
            text = entry.text.lower()

            # Check for direct keywords
            if "present" in text or "currently" in text:
                if link not in currently_studying_profiles:
                    currently_studying_profiles.append(link)
                    print(f"Currently studying (keyword): {link}")
                break

            # Define date regex patterns
            date_patterns = [
                r'\b(\w+\s\d{4})\s*[-–—]\s*(\w+\s\d{4}|present|currently)\b',
                r'\b(\d{4})\s*[-–—]\s*(\d{4}|present|currently)\b'
            ]

            for pattern in date_patterns:
                date_matches = re.findall(pattern, text)
                for start, end in date_matches:
                    try:
                        if end.lower() in ["present", "currently"] or 'present' in end.lower() or 'currently' in end.lower():
                            if link not in currently_studying_profiles:
                                currently_studying_profiles.append(link)
                                print(f"Currently studying (ongoing): {link}")
                            break
                        end_year_match = re.search(r'\d{4}', end)
                        if end_year_match:
                            end_year = int(end_year_match.group())
                            if end_year >= 2025:
                                if link not in currently_studying_profiles:
                                    currently_studying_profiles.append(link)
                                    print(f"Currently studying (year ≥ 2025): {link}")
                                break
                    except Exception as e:
                        print(f"Date parse error: {e}")
    except Exception as e:
        print(f"Error checking education for {link}: {e}")
 
 
education()
#  Save all profiles and filtered ones
df_all = pd.DataFrame({'Profile Links': all_profiles})
df_all.to_excel('linkedin_all_profiles.xlsx', index=False)

df_current = pd.DataFrame({'Currently Studying Profiles': currently_studying_profiles})
df_current.to_excel('linkedin_currently_studying_profiles.xlsx', index=False)

print(" Profile data saved successfully.")
driver.quit()
