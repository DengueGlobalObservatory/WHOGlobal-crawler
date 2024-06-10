import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import os

# Fetch the webpage
url = "https://worldhealthorg.shinyapps.io/dengue_global/"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Select the paragraph containing the date
date_paragraph = soup.find_all('p')[30].get_text(strip=True)

# Define a regular expression pattern to match the date after "Data reported as of"
pattern = r"; Data reported as of\n\s*(\d+\s+[A-Za-z]+\s+\d+)"

# Search for the pattern in the text
match = re.search(pattern, str(soup), re.MULTILINE)

# Extract the date after "Data reported as of"
# Search for the pattern in the text
if match:
    # Extract the matched date
    date = match.group(1)
    print(f"Extracted Date: {date}")

    # Create a new DataFrame with today's date and the extracted report date
    table = [{'Sys_date': pd.Timestamp.now(), 'Report_date': pd.to_datetime(date)}]
    table = pd.DataFrame(table)
    print(table)

else:
    print("No date found after 'Data reported as of'")



# Append the new data to the existing CSV file
# Set the download directory to the GitHub repository folder
github_workspace = os.getenv('GITHUB_WORKSPACE')
csv_path = os.path.join(github_workspace, 'data/report_date.csv')
df = pd.read_csv(csv_path)
df = pd.concat([df, table])

# update and save CSV
df.to_csv(csv_path, index=False)

# Read the last date from the CSV file
df['Sys_date'] = pd.to_datetime(df['Sys_date'])
df['Report_date'] = pd.to_datetime(df['Report_date'])

df = df.sort_values(by='Sys_date', ascending=False)

last_report_date = df['Report_date'].iloc[0]
second_last_date = df['Report_date'].iloc[1]



if last_report_date == second_last_date: 
    print("No data updates")

# If the date has been updated then run Selenium and download data
else: 
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    import time
    
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



