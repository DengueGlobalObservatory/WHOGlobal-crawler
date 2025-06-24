import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import os
from datetime import datetime
from io import StringIO


# Fetch the webpage
url = "https://worldhealthorg.shinyapps.io/dengue_global/"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
print(soup.prettify())

# Select the paragraph containing the date
date_paragraph = soup.find('span', string=lambda t: t and "Data reported as of" in t)

# Define a regular expression pattern to match the date after "Data reported as of"
# Extract the matched date
date_string = date_paragraph.next_sibling.strip()

# Parse the input date string into a datetime object
date_string = datetime.strptime(date_string, "%d %B %Y")
# Format the datetime object into the desired format
formatted_date = date_string.strftime("%Y-%m-%d")

print(f"Extracted Date: {formatted_date}")

# Create a new DataFrame with today's date and the extracted report date
now = datetime.now() # current date and time

table = [{'Sys_date': now.strftime('%Y-%m-%d %H:%M'), 'Report_date': formatted_date}]
df_current = pd.DataFrame(table)
print(df_current)

# Access to CSV in git repo - get token from environment variable
token = os.getenv('GITHUB_TOKEN')
if not token:
    raise ValueError("GITHUB_TOKEN environment variable not set")

headers = {'Authorization': f'token {token}'}
response = requests.get("https://raw.githubusercontent.com/DengueGlobalObservatory/DengueCrawler/main/data/report_date.csv", headers=headers)

if response.status_code == 200:
    # Read the CSV content into a DataFrame
    csv_content = StringIO(response.text)
    df_main_old = pd.read_csv(csv_content)
    print(df_main_old.head())
else:
    print(f"Failed to fetch data. Status code: {response.status_code}")

# Append the new data to the existing CSV file
df_main_new = pd.concat([df_main_old, df_current])

# save to dataframe and overwrite the old file
df_main_new.to_csv("data/report_date.csv", index = False)

# Read the last date from the CSV file
df_main_new['Sys_date'] = pd.to_datetime(df_main_new['Sys_date'], format='%Y-%m-%d %H:%M')
df_main_new['Report_date'] = pd.to_datetime(df_main_new['Report_date'], format='%Y-%m-%d')

df_main_new = df_main_new.sort_values(by='Sys_date', ascending=False)

last_report_date = df_main_new['Report_date'].iloc[0]
second_last_date = df_main_new['Report_date'].iloc[1]

if last_report_date == second_last_date:
   print("No data updates")

# If the date has been updated then run Selenium and download data
else:
    print("Downloading data")
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
    # "--headless",
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
    if os.getenv('GITHUB_WORKSPACE'):
        # Running in GitHub Actions
        github_workspace = os.path.join(os.getenv('GITHUB_WORKSPACE'))
        download_directory = os.path.join(github_workspace, 'Downloads')

    else:
        # Running locally
        github_workspace = os.path.join(os.getcwd())
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



