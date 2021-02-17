# mint-scraper

## Usage
In a command line with current directory set to your mint-scraper folder:
`python net_worth.py`

On first use or to update: type 'y' as a response when asking if you want to update from mint.
Enter your mint email and mint password and a Chromium window will open and will scrape the necessary data.

This will likely get messed up in a number of scenarios like 2FA or if the password is incorrect.

## Pre-requisite Libraries
- Selenium
- pandas
- numpy

## Drivers
- Download the chromium driver and add it to your PATH (environment variables): https://sites.google.com/a/chromium.org/chromedriver/downloads
