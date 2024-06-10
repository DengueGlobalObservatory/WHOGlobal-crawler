# Data scraper for global dengue data
This repository contains scripts to scrape global dengue data using R and Python. The workflows are automated using GitHub Actions.

## Structure
### `scraper`
- **`All-job.py`**: A Python script that runs Selenium to download global dengue data from the [WHO Global Dengue Dashboard](https://worldhealthorg.shinyapps.io/dengue_global/). Datasets will be added automatically to the Downloads folder only if the data reporting date has been updated on the website. 

### `.github/workflows`
- **`All-Action.yaml`**: A GitHub Actions workflow file to run the `All-job.py` script.

