import requests
import pandas as pd
from bs4 import BeautifulSoup


def scrape_cfb_schedule(year):
    """Scrapes college football schedule and results for a given year from Sports-Reference."""

    url = f"https://www.sports-reference.com/cfb/years/{year}-schedule.html"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Failed to retrieve data for {year}. Check the URL or try again later.")
        return

    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", {"id": "schedule"})

    if not table:
        print(f"No schedule table found for {year}. The structure of the website may have changed.")
        return

    # Extract headers
    headers = [th.text.strip() for th in table.find("thead").find_all("th")]

    # Extract data rows (ignore headers)
    rows = []
    for tr in table.find("tbody").find_all("tr"):
        cells = [td.text.strip().replace("\xa0", " ") for td in tr.find_all(["th", "td"])]
        if cells:  # Ensure the row is not empty
            rows.append(cells)

    # Convert to DataFrame
    df = pd.DataFrame(rows)


    # Save to CSV
    csv_filename = f"data/{year}.txt"
    df.to_csv(csv_filename, index=False, header=False)
    print(f"Data for {year} saved as {csv_filename}")
