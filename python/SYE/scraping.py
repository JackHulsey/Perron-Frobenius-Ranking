import requests
import pandas as pd
from bs4 import BeautifulSoup


def scrape_cfb_schedule(year):
    """Scrapes college football schedule and results for a given year from Sports-Reference."""

    url = f"https://www.sports-reference.com/cfb/years/{year}-schedule.html"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Failed to retrieve data for {year}. Check the URL or try again later.")
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", {"id": "schedule"})

    if not table:
        print(f"No schedule table found for {year}. The structure of the website may have changed.")
        return None

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
    return True

def get_college_football_rankings_espn(year, records): # this pulls from espn but only goes back to 2007
    url = f"https://www.espn.com/college-football/rankings/_/poll/1/year/{year}"
    headers = {"User-Agent": "Mozilla/5.0"}  # Prevent potential blocking
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("Failed to retrieve data.")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    rankings = []

    # Find ranking table
    rows = soup.select(".Table__TBODY tr")

    for row in rows:
        team = row.select_one("span.hide-mobile") # More accurate selector for team names
        if team:
            rankings.append(team.text.strip().replace(' ', ''))

    ranking_indices = []
    for team in rankings:
        for i in range(len(records)):
            if team == records[i][0]:
                ranking_indices.append(i)
                break
            if i == len(records) - 1:
                print(team)
    print(ranking_indices)
    return rankings, ranking_indices

def get_college_football_rankings(year, records):
    # URL for the 2024 AP football rankings
    url = f"https://www.collegepollarchive.com/football/ap/seasons.cfm?seasonid={year}"

    headers = {
        "User-Agent": "Mozilla/5.0"  # Prevent blocking by the website
    }

    # Send a GET request to the page
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("Failed to retrieve data.")
        return []

    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")

    # Find the table with class "table-responsive"
    table = soup.find("table", class_="table table-sm table-hover w-auto")

    if not table:
        print("Couldn't find the table with class 'table-responsive'.")
        return []

    # Extract the top 25 teams from the table
    rankings = []
    rows = table.find_all("tr")[1:]  # Skip the header row

    for row in rows[:25]:  # Get only the top 25 teams
        columns = row.find_all("td")
        if len(columns) > 1:  # Ensure there is enough data in the row
            team = columns[3].find("a")
            if team:
                team = team.get_text(strip=True)
                team = team.strip().replace(" ", "")
                if team == "Miami(FL)":
                    team = "Miami"
            rankings.append(team)

    ranking_indices = []
    for team in rankings:
        for i in range(len(records)):
            if team == records[i][0]:
                ranking_indices.append(i)
                break
            if i == len(records) - 1:
                print(f"{team} what")
    return rankings, ranking_indices
