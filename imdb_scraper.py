import requests
from bs4 import BeautifulSoup
import pandas as pd

# Target URL: Box Office Mojo (Owned by IMDb) - Top Movies of 2024
url = "https://www.boxofficemojo.com/year/world/"

# Headers to mimic a real browser
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}


def scrape_box_office():
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        movies = []

        # Select all rows in the table
        rows = soup.select('tr')

        # Loop through rows (skip the first one because it's the header)
        for row in rows[1:]:
            cols = row.select('td')

            if len(cols) > 2:
                rank = cols[0].text.strip()
                title = cols[1].text.strip()
                worldwide_gross = cols[2].text.strip()
                domestic_gross = cols[3].text.strip()

                movies.append({
                    'Rank': rank,
                    'Movie Title': title,
                    'Worldwide Gross': worldwide_gross,
                    'Domestic Gross': domestic_gross
                })

        # Convert to DataFrame
        df = pd.DataFrame(movies)

        # Save to CSV
        df.to_csv('box_office_data.csv', index=False)
        print(f"Scraped {len(movies)} movies successfully. Saved to box_office_data.csv")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    scrape_box_office()