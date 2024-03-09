"""Weather Data Web Scraper"""

import pandas as pd

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

NYC_DEC_2023_WEATHER_DATA_URL = (
    "https://www.wunderground.com/history/monthly/us/ny/new-york-city/KLGA/date/2023-12"
)

options = webdriver.ChromeOptions()
options.add_argument("--headless")
browser = webdriver.Chrome(options=options)
browser.get(NYC_DEC_2023_WEATHER_DATA_URL)

try:
    element = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "observation-title"))
    )

    html = browser.page_source
finally:
    browser.quit()

# find table object by class name
soup = BeautifulSoup(html, "html.parser")
table = soup.find("table", {"class": "days ng-star-inserted"})


# extract the data from html table
# source : https://www.webscrapingapi.com/find-out-how-to-scrape-html-table-with-python
data = []

for row in table.find_all("tr"):

    cols = row.find_all("td")

    # Extracting the table headers

    if len(cols) == 0:

        cols = row.find_all("th")

    cols = [ele.text.strip() for ele in cols]

    data.append([ele for ele in cols if ele])  # Get rid of empty values

print(data)

df = pd.DataFrame(data)

df.to_csv("data/weather/Scraped-NYC-Weather-Dec-2023.csv")


# processing
df = pd.read_csv("data/weather/Scraped-NYC-Weather-Dec-2023.csv")
df["Index"] = df.index
header_rows = df[df["0"] == "Max"].reset_index(drop=True)

# extract Temperature table only
start_idx = header_rows.loc[0].at["Index"] + 1
end_idx = header_rows.loc[1].at["Index"]

temp_df = df.iloc[start_idx:end_idx].copy()
temp_df.rename(columns={"0": "MaxTemp", "1": "AvgTemp", "2": "MinTemp"}, inplace=True)
temp_df.reset_index(drop=True, inplace=True)

# assign day values
temp_df["Day"] = temp_df.index + 1

final_df = temp_df[["Day", "MaxTemp", "AvgTemp", "MinTemp"]]
final_df = final_df.astype({"MaxTemp": float, "AvgTemp": float, "MinTemp": float})


def fahrenheit_to_celsius(temp_in_fahrenheit: float):
    """Takes a Fahrenheit temperature, retunrs a corresponding Celsius temp."""

    return round((temp_in_fahrenheit - 32) * 5 / 9, 2)


# convert temperatures from °F to °C
final_df[["MaxTempInCelsius", "AvgTempInCelsius", "MinTempInCelsius"]] = final_df[
    ["MaxTemp", "AvgTemp", "MinTemp"]
].apply(fahrenheit_to_celsius)


final_df.to_csv("data/weather/final-nyc-weather-data.csv")
print(final_df)
