import random
import re
import requests
import time

from bs4 import BeautifulSoup
import pandas as pd


class VarietiesScraper:
    def __init__(self, base_url="https://varieties.worldcoffeeresearch.org"):
        self.base_url = base_url
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        self.varieties_data = []

    def fetch_page(self, url):
        try:
            time.sleep(random.uniform(1, 3))
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return BeautifulSoup(response.content, "html.parser")
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None

    def extract_variety_details(self, variety_url):
        soup = self.fetch_page(variety_url)

        if not soup:
            print(f"Failed to fetch details page for {variety_url}.")
            return None

        details = {
            "url": variety_url,
            "name": "Unknown",
            "description": "Unknown",
            "characteristics": {},
        }

        name_elem = soup.select_one('h1[class*="text-"]')

        if name_elem:
            details["name"] = name_elem.text.strip()

        desc_elem = soup.select_one('div[class*="text-gray"]')
        if desc_elem:
            details["description"] = desc_elem.text.strip()

        characteristic_sections = soup.select("div.flex.flex-col.justify-start")
        print(f"Found {len(characteristic_sections)} characteristic sections.")

        for section in characteristic_sections:
            label_elem = section.select_one("span.uppercase.font-semibold")
            value_elem = section.find(
                "div", class_=re.compile(r"w-full.*text-txt-black")
            )

            if label_elem and value_elem:
                label = label_elem.text.strip()
                value = value_elem.text.strip()
                print(f"Characteristic: {label} = {value}")  # Debug
                details["characteristics"][label] = value

        return details

    def scrape_varieties(self):
        catalog_url = f"{self.base_url}/arabica/varieties"
        soup = self.fetch_page(catalog_url)

        if not soup:
            print("Failed to fetch the catalog page.")
            return

        links = soup.select('a[href*="/varieties/"]')

        unique_links = list(
            set(
                (
                    f"{self.base_url}{link['href']}"
                    if link["href"].startswith("/")
                    else link["href"]
                )
                for link in links
            )
        )

        for variety_url in unique_links:
            details = self.extract_variety_details(variety_url)
            if details:
                self.varieties_data.append(details)

    def save_to_csv(self, filename="../../data/01_raw/arabica_varieties.tsv"):
        if self.varieties_data:
            data = [
                {
                    **{
                        "url": variety["url"],
                        "name": variety["name"],
                        "description": variety["description"],
                    },
                    **variety["characteristics"],
                }
                for variety in self.varieties_data
            ]

            df = pd.DataFrame(data)
            df.to_csv(filename, index=False, sep="\t")

            print(f"Data successfully saved to {filename}")
        else:
            print("No data to save.")


if __name__ == "__main__":
    scraper = VarietiesScraper()
    scraper.scrape_varieties()
    scraper.save_to_csv()
