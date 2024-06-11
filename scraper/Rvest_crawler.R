library(stringr)
library(readr)
library(rvest)
library(dplyr)

# Extract the date of data report ===========================
url <- "https://worldhealthorg.shinyapps.io/dengue_global/"
web_page <- read_html(url)

# Select the paragraph containing the date
date_paragraph <- web_page %>%
  html_nodes("p:nth-child(2)") %>%
  html_text(trim = TRUE)

# Extract the date after "Data reported as of"
date_after_phrase <- gsub("^.*Data reported as of ", "", date_paragraph, perl = TRUE)
print(date_after_phrase)
date_pattern <-  "(\\d{1,2})\\s[A-Za-z]+\\s\\d{4}"
report_date <- as.Date(str_extract(date_paragraph[3], date_pattern), format = "%d %B %Y")

# create a new row of data, with todayd's date and urls number
table <- data.frame(Sys_date = Sys.time(),
                    Report_date = report_date)

# append at the end of the csv the new data
write_csv(table, file = paste0('data/report_date.csv'), append = TRUE)


# Read the last date from the CSV file
path <- "data/report_date.csv"
table <- read_csv(path)%>%
  arrange(desc(Sys_date))

last_report_date <- table$Report_date[1]
second_last_date <- table$Report_date[2]

last_report_date == second_last_date
















# Download global data =====================================
# eCaps <- list(
#   chromeOptions =
#     list(prefs = list(
#       "profile.default_content_settings.popups" = 0L,
#       "download.prompt_for_download" = FALSE,
#       "download.default_directory" = "C:/Users/AhyoungLim/Dropbox/" # downloaded file to your desired location
#     )
#     )
# )

#
#
# binman::list_versions('chromedriver') # make sure chrome version == chromedriver version
# chrome(port = 4837L, version = '125.0.6422.114')
# rs_driver_object = rsDriver(
#                     remoteServerAddr = "localhost",
#                     browser = 'firefox',
#                    # chromever = '125.0.6422.114',
#                    # extraCapabilities = eCaps,
#                    port = 4567L
#                    )
# #
# #
# remDr = rs_driver_object$client
#
# remDr$open()
# remDr$navigate('https://worldhealthorg.shinyapps.io/dengue_global/')
# # remDr$getPageSource()
# remDr$findElement(using = "id", "closeModal")$clickElement() # find and click "I accept" button
# remDr$findElement(using = "xpath", value = "//a[@data-value='dl_data']")$clickElement() # find and click "download data" in the menu
# remDr$findElement(using = "id", "dl_all_data")$clickElement() # download global data


# # close browser
# remDr$close()
#
#
# # stop the selenium server
# rd[["server"]]$stop()
#
# # and delete it
# rm(rd)


