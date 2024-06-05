library(RSelenium)
library(rvest)

rs_driver_object = rsDriver(
                    remoteServerAddr = "localhost",
                    browser = 'firefox',
                   # chromever = '125.0.6422.114',
                   # extraCapabilities = eCaps,
                   port = 4444L
                   )

remDr = rs_driver_object$client

remDr$open()
remDr$navigate('https://worldhealthorg.shinyapps.io/dengue_global/')
# remDr$getPageSource()
remDr$findElement(using = "id", "closeModal")$clickElement() # find and click "I accept" button
remDr$findElement(using = "xpath", value = "//a[@data-value='dl_data']")$clickElement() # find and click "download data" in the menu
remDr$findElement(using = "id", "dl_all_data")$clickElement() # download global data


# # close browser
# remDr$close()
