import re

class TextAnalyzer:
    def __init__(self, config):
        self.config = config
        self.load_config()

    def load_config(self):
        # Load the configuration from the config file
        pass

    def analyze(self, text):
        countries = self.config['tax_groups']
        offshore_words = self.config['offshore_words']

        country_counts = {group: 0 for group in countries}
        offshore_mentions = {word: 0 for word in offshore_words}
        countries_found = []

        sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)

        for sentence in sentences:
            for group, country_list in countries.items():
                for country in country_list:
                    if country in sentence:
                        country_counts[group] += 1
                        if country not in countries_found:
                            countries_found.append(country)
                        for word in offshore_words:
                            if word in sentence:
                                offshore_mentions[word] += 1

        return country_counts, offshore_mentions, countries_found