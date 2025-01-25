from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import time
import random


class CoffeeScraper:
    def __init__(self):
        self.base_url = "https://coffeelove.pl/pl/c/Kawa/46"
        self.data = []
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(service=Service(), options=chrome_options)

    def fetch_page(self, url):
        try:
            self.driver.get(url)
            time.sleep(random.uniform(2, 4))  # Allow time for dynamic content to load
            return BeautifulSoup(self.driver.page_source, 'html.parser')
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None

    def parse_coffee_list(self, soup):
        coffee_links = []
        products = soup.select('a.product-item-photo')  # Adjust this selector to match the actual HTML
        if not products:
            print("No products found on this page!")
            return []

        for product in products:
            coffee_links.append(product['href'])
        print(f"Found {len(coffee_links)} product links.")
        return coffee_links

    def parse_coffee_details(self, coffee_url):
        print(f"Fetching details from {coffee_url}...")
        soup = self.fetch_page(coffee_url)

        if not soup:
            print("Failed to fetch details for this product.")
            return None

        coffee_data = {'url': coffee_url, 'pochodzenie': 'Unknown', 'region': 'Unknown', 'odmiana': 'Unknown'}

        # Adjust selectors based on actual HTML structure
        details = soup.find('div', class_='product-attributes')
        if details:
            pochodzenie = details.find(text='Pochodzenie')
            if pochodzenie:
                coffee_data['pochodzenie'] = pochodzenie.find_next('span').text.strip()

            region = details.find(text='Region')
            if region:
                coffee_data['region'] = region.find_next('span').text.strip()

            odmiana = details.find(text='Odmiana')
            if odmiana:
                coffee_data['odmiana'] = odmiana.find_next('span').text.strip()

        print(f"Scraped details: {coffee_data}")
        return coffee_data

    def scrape(self):
        page_url = self.base_url
        while page_url:
            print(f"Scraping: {page_url}")
            soup = self.fetch_page(page_url)

            if not soup:
                break

            coffee_links = self.parse_coffee_list(soup)
            if not coffee_links:
                print("No more coffee products found. Stopping.")
                break

            for link in coffee_links:
                coffee_url = f"https://coffeelove.pl{link}"
                coffee_details = self.parse_coffee_details(coffee_url)
                if coffee_details:
                    self.data.append(coffee_details)

            # Find next page link
            next_page_tag = soup.find('link', rel='next')
            page_url = next_page_tag['href'] if next_page_tag else None

    def save_to_csv(self, filename='../../data/01_raw/coffeelove_data.csv'):
        if not self.data:
            print("No data to save!")
            return

        df = pd.DataFrame(self.data)
        df.to_csv(filename, index=False)
        print(f"Data saved to {filename}")

    def close(self):
        self.driver.quit()

if __name__ == "__main__":
    scraper = CoffeeScraper()
    scraper.scrape()
    scraper.save_to_csv()
    scraper.close()
