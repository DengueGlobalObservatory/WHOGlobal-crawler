# Data scraper for global dengue data
This repository contains scripts to scrape global dengue data using R and Python. The workflows are automated using GitHub Actions.

## Structure
### `scraper`
- **`Rvest_crawler.R`**: An R script that extracts data using the `rvest` package and saves the results to `data/report_date.csv`.
- **`Selenium-action.py`**: A Python script that runs Selenium to download global dengue data from the [WHO Global Dengue Dashboard](https://worldhealthorg.shinyapps.io/dengue_global/).

### `.github/workflows`
- **`Rvest-Action.yaml`**: A GitHub Actions workflow file to run the `Rvest_crawler.R` script.
- **`Selenium-Action.yaml`**: A GitHub Actions workflow file to run the `Selenium-action.py` script.
