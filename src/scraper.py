import requests
from bs4 import BeautifulSoup
import yaml
import json
from urllib.parse import urljoin, urlparse
from analyzer import TextAnalyzer

class WebScraper:
    def __init__(self, config_path):
        with open(config_path, 'r') as file:
            self.config = yaml.safe_load(file)
        self.analyzer = TextAnalyzer(self.config)
        self.visited_urls = set()
        self.results = {}

    def fetch_website_content(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            print(f"Successfully retrieved {url}")
            return response.text
        else:
            print(f"Failed to retrieve {url}")
            return None

    def scrape(self):
        for website in self.config['websites']:
            self.scrape_website(website)
        self.save_results()

    def scrape_website(self, url, root_url=None):
        if root_url is None:
            root_url = url
        if url in self.visited_urls:
            return
        self.visited_urls.add(url)
        content = self.fetch_website_content(url)
        if content:
            self.analyze_content(root_url, content)
            try:
                soup = BeautifulSoup(content, 'html.parser')
                for link in soup.find_all('a', href=True):
                    next_url = urljoin(url, link['href'])
                    if self.is_valid_url(next_url, url):
                        self.scrape_website(next_url, root_url)
            except Exception as e:
                print(f"Error parsing {url}: {e}")

    def is_valid_url(self, url, base_url):
        parsed_url = urlparse(url)
        return parsed_url.scheme in ('http', 'https') and urlparse(base_url).netloc == parsed_url.netloc

    def analyze_content(self, root_url, content):
        text = self.extract_text(content)
        country_counts, offshore_mentions, countries_found = self.analyzer.analyze(text)
        if root_url not in self.results:
            self.results[root_url] = {
                "country_counts": {group: 0 for group in self.config['tax_groups']},
                "offshore_mentions": {word: 0 for word in self.config['offshore_words']},
                "countries_found": []
            }
        for group, count in country_counts.items():
            self.results[root_url]["country_counts"][group] += count
        for word, count in offshore_mentions.items():
            self.results[root_url]["offshore_mentions"][word] += count
        self.results[root_url]["countries_found"].extend(countries_found)
        self.results[root_url]["countries_found"] = list(set(self.results[root_url]["countries_found"]))

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

if __name__ == "__main__":
    scraper = WebScraper('config.yaml')
    scraper.scrape()