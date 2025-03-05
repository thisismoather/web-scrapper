import requests
from bs4 import BeautifulSoup
import yaml
import json
import pandas as pd
import argparse
from urllib.parse import urljoin, urlparse
from datetime import datetime, timedelta
from time import sleep
from analyzer import TextAnalyzer

class WebScraper:
    def __init__(self, config_path='config.yaml', websites_path='websites.dta', num_sites=None, num_years=1, delay=1, frequency='Q'):
        with open(config_path, 'r') as file:
            self.config = yaml.safe_load(file)
        self.analyzer = TextAnalyzer(self.config)
        self.visited_urls = set()
        self.results = {}
        self.websites = self.load_websites(websites_path, num_sites)
        self.num_years = num_years
        self.delay = delay
        self.frequency = frequency
        self.failed_requests_log = 'failed_requests.log'

    def load_websites(self, websites_path, num_sites):
        df = pd.read_stata(websites_path)
        print("Columns in the Stata file:", df.columns)  # Debugging line
        urls = [self.ensure_scheme(url) for url in df['weburl'].tolist()]
        if num_sites == "all":
            return urls
        else:
            return urls[:int(num_sites)]

    def ensure_scheme(self, url):
        if not urlparse(url).scheme:
            return 'https://' + url
        return url

    def fetch_website_content(self, url):
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365 * self.num_years)
        snapshots = self.get_wayback_snapshots(url, start_date, end_date)
        contents = []
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        print(f"____________________ {url}")
        print(f"Found {len(snapshots)} snapshots for {url}")
        for snapshot in snapshots:
            print(f"Retrieving {snapshot}")
            try:
                response = requests.get(snapshot, headers=headers, timeout=60)
                if response.status_code == 200:
                    print(f"Successfully retrieved {snapshot}")
                    contents.append((snapshot, response.text))
                else:
                    print(f"Failed to retrieve {snapshot}")
                    self.log_failed_request(snapshot, response.status_code)
            except requests.RequestException as e:
                print(f"Exception occurred while retrieving {snapshot}: {e}")
                self.log_failed_request(snapshot, str(e))
            sleep(self.delay)  # Add delay between requests
        return contents

    def log_failed_request(self, url, reason):
        with open(self.failed_requests_log, 'a') as log_file:
            log_file.write(f"Failed URL: {url}, Reason: {reason}\n")

    def get_wayback_snapshots(self, url, start_date, end_date):
        snapshots = []
        api_url = f"http://web.archive.org/cdx/search/cdx?url={url}&from={start_date.strftime('%Y%m%d')}&to={end_date.strftime('%Y%m%d')}&output=json&fl=timestamp,original&collapse=digest"
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data[1:], columns=data[0])
            df['datetime'] = pd.to_datetime(df['timestamp'], format='%Y%m%d%H%M%S')
            df = df.set_index('datetime').resample(self.frequency)['timestamp'].first().dropna().reset_index()
            for _, row in df.iterrows():
                snapshot_url = f"http://web.archive.org/web/{row['timestamp']}/{url}"
                snapshots.append(snapshot_url)
        return snapshots

    def scrape(self):
        for website in self.websites:
            self.scrape_website(website)
        self.save_results()

    def scrape_website(self, url, root_url=None):
        if root_url is None:
            root_url = url
        if url in self.visited_urls:
            return
        self.visited_urls.add(url)
        print(f"Scraping {url}")
        contents = self.fetch_website_content(url)
        for snapshot, content in contents:
            if content:
                year = snapshot.split('/')[4][:4]
                self.analyze_content(root_url, content, year)
                try:
                    soup = BeautifulSoup(content, 'html.parser')
                    for link in soup.find_all('a', href=True):
                        next_url = urljoin(url, link['href'])
                        if self.is_valid_url(next_url, url):
                            print(f"Found link: {next_url}")
                            print(f"Root URL: {root_url}")
                            self.scrape_website(next_url, root_url)
                            sleep(self.delay)  # Add delay between requests
                except Exception as e:
                    print(f"Error parsing {url}: {e}")

    def is_valid_url(self, url, base_url):
        parsed_url = urlparse(url)
        return parsed_url.scheme in ('http', 'https') and urlparse(base_url).netloc == parsed_url.netloc

    def analyze_content(self, root_url, content, year):
        text = self.extract_text(content)
        country_counts, offshore_mentions, countries_found = self.analyzer.analyze(text)
        if root_url not in self.results:
            self.results[root_url] = {}
        if year not in self.results[root_url]:
            self.results[root_url][year] = {
                "country_counts": {group: 0 for group in self.config['tax_groups']},
                "offshore_mentions": {word: 0 for word in self.config['offshore_words']},
                "countries_found": []
            }
        for group, count in country_counts.items():
            self.results[root_url][year]["country_counts"][group] += count
        for word, count in offshore_mentions.items():
            self.results[root_url][year]["offshore_mentions"][word] += count
        self.results[root_url][year]["countries_found"].extend(countries_found)
        self.results[root_url][year]["countries_found"] = list(set(self.results[root_url][year]["countries_found"]))

    def extract_text(self, html_content):
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            return soup.get_text()
        except Exception as e:
            print(f"Error extracting text: {e}")
            return ""

    def save_results(self):
        with open('results.json', 'w') as file:
            json.dump(self.results, file, indent=4)
        self.save_results_stata()

    def save_results_stata(self):
        data = []
        for url, yearly_results in self.results.items():
            for year, result in yearly_results.items():
                row = {
                    "url": url,
                    "year": year,
                    **result["country_counts"],
                    **result["offshore_mentions"],
                    "countries_found": ", ".join(result["countries_found"])
                }
                data.append(row)
        df = pd.DataFrame(data)
        df.to_stata('results.dta', write_index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Web Scraper for Company Website Analysis')
    parser.add_argument('num_sites', type=str, help='Number of sites to scrape or "all" to scrape all sites')
    parser.add_argument('--num_years', type=int, default=1, help='Number of years for which data needs to be scraped')
    parser.add_argument('--delay', type=int, default=1, help='Delay between requests in seconds')
    parser.add_argument('--frequency', type=str, default='Q', help='Frequency for snapshots (e.g., "Q" for quarterly)')
    args = parser.parse_args()

    scraper = WebScraper(num_sites=args.num_sites, num_years=args.num_years, delay=args.delay, frequency=args.frequency)
    scraper.scrape()