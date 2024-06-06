from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time
import os

chrome_options = Options()    
options = [
  # Define window size here
  "--headless",
  "--disable-gpu",
  "--window-size=1920,1200",
  "--ignore-certificate-errors",
  "--disable-extensions",
  "--no-sandbox",
  "--disable-dev-shm-usage"
 ]

for option in options:
     chrome_options.add_argument(option)

# Set the download directory to the GitHub repository folder
github_workspace = os.getenv('GITHUB_WORKSPACE')
download_directory = os.path.join(github_workspace, 'Downloads')

#prefs = {"download.default_directory" : r"C:\Users\AhyoungLim\Dropbox\\"}
prefs = {"download.default_directory": download_directory,}
    
chrome_options.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(service=Service(), options = chrome_options)

driver.get('https://worldhealthorg.shinyapps.io/dengue_global/')
print(driver.title)
# with open('./GitHub_Action_Results.txt', 'w') as f:
#     f.write(f"This was written with a GitHub action {driver.title}")

# Wait for the "I accept" button to be clickable and then click it
accept_button = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.ID, "closeModal"))
)
driver.execute_script("arguments[0].scrollIntoView();", accept_button)
driver.execute_script("arguments[0].click();", accept_button)

#accept_button.click()


# Find and click the "Download Data" link in the menu
download_link = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.XPATH, "//a[@data-value='dl_data']"))
)
driver.execute_script("arguments[0].scrollIntoView();", download_link)
driver.execute_script("arguments[0].click();", download_link)

time.sleep(5)

# Click the button to download all data
download_all_data_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "dl_all_data"))
)
driver.execute_script("arguments[0].scrollIntoView();", download_all_data_button)
driver.execute_script("arguments[0].click();", download_all_data_button)

time.sleep(5)

driver.quit()
