

from selenium import webdriver 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#driver = webdriver.Chrome() 
#driver.get('https://worldhealthorg.shinyapps.io/dengue_global/')
#time.sleep(3)

chrome_options = Options()
options = [
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

driver = webdriver.Chrome(service=Service(), options=chrome_options)


# Navigate to the URL
url = 'https://worldhealthorg.shinyapps.io/dengue_global/'
driver.get(url)

# Wait for the "I accept" button to be clickable and then click it
accept_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "closeModal"))
)
accept_button.click()

# Find and click the "Download Data" link in the menu
download_link = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//a[@data-value='dl_data']"))
)
download_link.click()

# Click the button to download all data
download_all_data_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "dl_all_data"))
)
download_all_data_button.click()    


driver.quit()
