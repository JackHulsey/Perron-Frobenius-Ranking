import requests
import pandas as pd
from bs4 import BeautifulSoup, Comment

def scrape_cfb_schedule(year):
    """Scrapes college football schedule and results for a given year from Sports-Reference."""

    url = f"https://www.sports-reference.com/cfb/years/{year}-schedule.html"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Failed to retrieve NCAA for {year}. Check the URL or try again later.")
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", {"id": "schedule"})

    if not table:
        print(f"No schedule table found for {year}. The structure of the website may have changed.")
        return None

    # Extract headers
    headers = [th.text.strip() for th in table.find("thead").find_all("th")]

    # Extract NCAA rows (ignore headers)
    rows = []
    for tr in table.find("tbody").find_all("tr"):
        cells = [td.text.strip().replace("\xa0", " ") for td in tr.find_all(["th", "td"])]
        if cells:  # Ensure the row is not empty
            rows.append(cells)

    # Convert to DataFrame
    df = pd.DataFrame(rows)


    # Save to CSV
    csv_filename = f"NCAA/{year}.txt"
    df.to_csv(csv_filename, index=False, header=False)
    print(f"Data for {year} saved as {csv_filename}")
    return True

def get_college_football_rankings_espn(year, records): # this pulls from espn but only goes back to 2007
    url = f"https://www.espn.com/college-football/rankings/_/poll/1/year/{year}"
    headers = {"User-Agent": "Mozilla/5.0"}  # Prevent potential blocking
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("Failed to retrieve NCAA.")
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

def get_college_football_rankings_broken(year, records):
    # URL for the 2024 AP football rankings
    url = f"https://www.collegepollarchive.com/football/ap/seasons.cfm?seasonid={year}"

    headers = {
        "User-Agent": "Mozilla/5.0"  # Prevent blocking by the website
    }

    # Send a GET request to the page
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("Failed to retrieve NCAA.")
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
        if len(columns) > 1:  # Ensure there is enough NCAA in the row
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
    return rankings, ranking_indices

def get_college_football_rankings(year: int):
    # Format Wikipedia page title
    #wiki_year = f'{year}-{year + 1}' if year >= 2006 else str(year)
    if year >= 2006:
        url = f"https://en.wikipedia.org/wiki/{year}_NCAA_Division_I_FBS_football_rankings"
    else:
        url = f"https://en.wikipedia.org/wiki/{year}_NCAA_Division_I-A_football_rankings"
    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError(f"Failed to load page: {url}")

    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the table with caption containing 'Final' and 'AP'
    final_ap_table = None
    i = 0
    for table in soup.find_all("table", class_="wikitable"):
        final_ap_table = table
        break

    if not final_ap_table:
        raise ValueError("Final AP Poll table not found.")

    # Get the last <td> from each row (skipping header)
    teams = []
    for row in final_ap_table.find_all("tr")[1:]:
        tds = row.find_all("td")
        if not tds or len(tds) < 2:
            continue
        last_td = tds[len(tds) - 3]
        team_text = last_td.get_text(strip=True)
        team_name = team_text.split("(")[0]  # Remove (record) if present
        team_name = team_name.replace(" ", "").replace("ʻ", '')
        if team_name and team_name != 'None' and not team_name.startswith('Dropped:'):
            teams.append(team_name)

    if not teams:
        raise ValueError("No team names found from last <td>s.")

    # Write the team names to a text file
    with open(f'rankings/AP/Week_14/{year}.txt', 'w', encoding="utf-8") as file:
        for team in teams:
            file.write(f"{team}\n")

    print(f"Team names have been successfully saved to 'rankings/AP/{year}.txt'.")