import re
from types import NoneType

from bs4 import BeautifulSoup
import pandas as pd
import requests
import random
import time


class CoffeeScraper:
    def __init__(self):
        self.base_url = "https://coffeelove.pl/pl/c/Kawa/46"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        self.data = []

    def fetch_page(self, url):
        try:
            time.sleep(random.uniform(1, 3))  # Be respectful to the server
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return BeautifulSoup(response.content, "html.parser")
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None

    def parse_coffee_list(self, soup):
        coffee_links = []
        products = soup.select('a[href*="/pl/p/"]')
        if not products:
            print("No products found on this page!")
            return []

        for product in products:
            coffee_links.append(product["href"])
        return coffee_links

    def parse_coffee_details(self, coffee_url):
        soup = self.fetch_page(coffee_url)

        if not soup:
            print(f"Failed to fetch details for {coffee_url}")
            return None

        coffee_data = {"origin": "Unknown", "region": "Unknown", "variety": "Unknown"}

        origin = ""
        origin_parent = soup.find_all(string=re.compile(r"pochodzenie", re.IGNORECASE))
        if len(origin_parent) > 0:
            origin = origin_parent[0].find_next("a")

        if origin != "":
            coffee_data["origin"] = origin.text.strip()
        else:
            coffee_data["origin"] = ""

        region = ""
        region_parent = soup.find_all(
            "strong", string=re.compile(r"region", re.IGNORECASE)
        )

        if len(region_parent) > 0:
            region = region_parent[0].find_next(
                "div", class_="xs_product_parameter_item_title"
            )

        if region != "":
            coffee_data["region"] = region.text.strip()
        else:
            coffee_data["region"] = region

        variety = ""
        variety_parent = soup.find_all(string=re.compile(r"odmiana", re.IGNORECASE))

        if len(variety_parent) > 0:
            variety = variety_parent[0].find_next(
                "div", class_="xs_product_parameter_item_title"
            )

        if variety != "" and not isinstance(variety, NoneType):
            coffee_data["variety"] = variety.text.strip()
        else:
            coffee_data["variety"] = variety

        self.data.append(coffee_data)

    def scrape(self):
        visited_urls = set()
        page_url = self.base_url

        while page_url:
            if page_url in visited_urls:
                print(f"Page already visited: {page_url}")
                break

            visited_urls.add(page_url)

            soup = self.fetch_page(page_url)

            if not soup:
                break

            coffee_links = self.parse_coffee_list(soup)
            if not coffee_links:
                print("No more coffee products found. Stopping.")
                break

            for link in coffee_links:
                coffee_url = f"https://coffeelove.pl{link}"

                if coffee_url not in visited_urls:
                    self.parse_coffee_details(coffee_url)
                    visited_urls.add(coffee_url)

            next_page_tag = soup.find("link", rel="next")
            page_url = next_page_tag["href"] if next_page_tag else None

    def save_to_tsv(self, filename="../../data/01_raw/coffeelove_data.tsv"):
        if not self.data:
            print("No data to save!")
            return

        df = pd.DataFrame(self.data)
        df.to_csv(filename, index=False, sep="\t")

        print(f"Data saved to {filename}")


if __name__ == "__main__":
    scraper = CoffeeScraper()
    scraper.scrape()
    scraper.save_to_tsv()
