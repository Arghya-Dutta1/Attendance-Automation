from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv
import os
import time

load_dotenv()

# ---------- Your Login Details ----------
registration_number = os.getenv("REG_NO")
password_value = os.getenv("PASSWORD")
url = "https://ums.lpu.in/lpuums/LoginNew.aspx"  # Replace with actual URL
# ----------------------------------------

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get(url)
driver.maximize_window()

wait = WebDriverWait(driver, 15)
actions = ActionChains(driver)

try:
    # Step 1: Enter Registration Number
    user_id_field = wait.until(EC.presence_of_element_located((By.ID, "txtU")))
    user_id_field.clear()
    user_id_field.send_keys(registration_number)
    print("✅ Entered Registration Number")
    time.sleep(2)  # Wait for postback trigger

    # Step 2: Wait for postback - Retry finding password field
    password_found = False
    retries = 0
    while not password_found and retries < 5:
        try:
            password_field = wait.until(EC.presence_of_element_located((By.ID, "TxtpwdAutoId_8767")))
            password_field.clear()
            password_field.send_keys(password_value)
            print("✅ Entered Password")
            password_found = True
        except Exception as e:
            print(f"⚠️ Password field not stable yet. Retrying... {e}")
            time.sleep(2)
            retries += 1

    if not password_found:
        raise Exception("❌ Failed to locate Password field after multiple retries.")

    # Step 3: Select "Home Page" from Dropdown with retry for staleness
    dropdown_found = False
    retries = 0
    while not dropdown_found and retries < 5:
        try:
            dropdown_element = wait.until(EC.presence_of_element_located((By.ID, "ddlStartWith")))
            dropdown = Select(dropdown_element)
            dropdown.select_by_visible_text("Dashboard")
            print("✅ Selected 'Dashboard'")
            dropdown_found = True
        except Exception as e:
            print(f"⚠️ Dropdown not stable yet. Retrying... {e}")
            time.sleep(2)
            retries += 1

    if not dropdown_found:
        raise Exception("❌ Failed to locate Dropdown after multiple retries.")

    # Step 4: Click Login Button with retry
    login_found = False
    retries = 0
    while not login_found and retries < 5:
        try:
            login_button = wait.until(EC.element_to_be_clickable((By.ID, "iBtnLogins150203125")))
            login_button.click()
            print("✅ Clicked Login Button")
            login_found = True
        except Exception as e:
            print(f"⚠️ Login Button not stable yet. Retrying... {e}")
            time.sleep(2)
            retries += 1

    if not login_found:
        raise Exception("❌ Failed to click Login Button after multiple retries.")
    
    # Step 5: Click the remind me later button
    remind_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Remind me later')]")))
    remind_button.click()
    print("✅ Clicked 'Remind me later' button")
    time.sleep(1)

    # Step 6: Click on the search icon to open search box
    search_icon = wait.until(EC.element_to_be_clickable((By.ID, "top-search-trigger")))
    search_icon.click()
    print("✅ Clicked Search Icon")
    time.sleep(1)  # Wait for input box to appear

    # Step 7: Type into the Search Input Box
    search_box = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input.form-control.searchmenu")))
    search_box.clear()
    search_box.send_keys("OJT/Internship Attendance")
    print("✅ Typed into Search Box")

    time.sleep(2)  # Wait for results to appear

    # Step 8: Click the result link (probably only one link appears)  
    try:
        # Wait for the link to exist
        final_attendance_link = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//a[contains(text(), 'OJT/Internship Attendance') and contains(@href, 'frmMarkOJTAttendance.aspx')]")
            )
        )

        # Click using JS Executor directly
        driver.execute_script("arguments[0].click();", final_attendance_link)
        print("✅ Clicked with JS Executor")

    except Exception as e:
        print(f"❌ Failed to click Attendance Link even with JS: {e}")
    
    # Step 9: Select the present option from the dropdown
    try:
        # Wait for the dropdown to be present
        attendance_dropdown = wait.until(
            EC.presence_of_element_located(
                (By.ID, "ctl00_cphHeading_Repeater1_ctl00_drpdwnAttendance")
            )
        )

        # Select the "PRESENT" option
        select = Select(attendance_dropdown)
        select.select_by_visible_text("PRESENT")
        print("✅ Selected 'PRESENT' from Attendance Dropdown")

        time.sleep(2)  # Wait for any postback/refresh

    except Exception as e:
        print(f"❌ Failed to select 'PRESENT' from dropdown: {e}")

    # Step 10: Click the Submit Button
    # try:
    #     # Wait for the Mark button to be clickable
    #     mark_button = wait.until(
    #         EC.element_to_be_clickable(
    #             (By.ID, "ctl00_cphHeading_Repeater1_ctl00_btnMarkAtt")
    #         )
    #     )

    #     # Click the Mark button
    #     mark_button.click()
    #     print("✅ Clicked 'Mark' Button for Attendance")

    # except Exception as e:
    #     print(f"❌ Failed to click 'Mark' button: {e}")


    time.sleep(5)  # Keep browser open for a while to observe

except Exception as e:
    print(f"❌ Final Error: {e}")

finally:
    time.sleep(5)
    driver.quit()
