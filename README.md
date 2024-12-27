# Web Scraper for Company Website Analysis

This project is a web scraper designed to analyze company websites by counting mentions of non-U.S. countries and categorizing them into tax groups. It also tracks occurrences of specific "offshore words" within the same sentences.

## Project Structure

```
web-scraper
├── src
│   ├── scraper.py        # Main logic for the web scraper
│   ├── analyzer.py       # Text analysis and categorization
│   ├── config.py         # Configuration settings
│   └── utils
│       └── helpers.py    # Utility functions for text processing
├── requirements.txt      # Project dependencies
├── config.yaml           # Scraper configuration settings
├── websites.dta          # Stata file containing website URLs
└── README.md             # Project documentation
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd web-scraper
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv .venv
   .venv\Scripts\activate  # On Windows
   source .venv/bin/activate  # On macOS/Linux
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Configuration

Edit the `config.yaml` file to specify the websites to scrape and define tax groups and offshore words.

### config.yaml
```yaml
websites:
  - https://www.abbott.com/

tax_groups:
  low_tax:
    - Andorra
    - Andorran
    - Anguilla
    # ...other countries...
  medium_tax:
    - Cyprus
    - Cypriot
    # ...other countries...
  high_tax:
    - Germany
    - France

offshore_words:
  - offshore
  - tax haven
  - shell company
  - secrecy jurisdiction
  # ...other words...
```

## Usage

To run the web scraper, execute the following command:
```
python src/scraper.py <num_sites>
```
- `<num_sites>`: Number of sites to scrape or "all" to scrape all sites listed in `websites.dta`.

### Example Commands

To scrape a specific number of sites (e.g., 5 sites):
```
python src/scraper.py 5
```

To scrape all sites:
```
python src/scraper.py all
```

## Input

- `config.yaml`: Configuration file specifying tax groups and offshore words.
- `websites.dta`: Stata file containing the list of website URLs to scrape.

## Output

The scraper generates two output files:
1. `results.json`: JSON file containing the analysis results.
2. `results.dta`: Stata file containing the analysis results.

### Example Output (results.json)
```json
{
    "https://www.aarcorp.com": {
        "country_counts": {
            "low_tax": 785,
            "medium_tax": 757,
            "high_tax": 242
        },
        "offshore_mentions": {
            "offshore": 0,
            "tax haven": 0,
            "shell company": 0,
            "secrecy jurisdiction": 0,
            "sales": 80,
            "markets": 4,
            "customers": 268,
            "distribution": 26,
            "marketing": 170,
            "revenues": 0,
            "distributors": 0,
            "revenue": 2,
            "export": 2,
            "customer": 448,
            "distributor": 20,
            "demand": 14,
            "stores": 0,
            "consumer": 0,
            "marketed": 0,
            "distribute": 0,
            "distributes": 0,
            "distributed": 0,
            "shipments": 8,
            "dealers": 0,
            "clients": 0,
            "wholesale": 0,
            "exports": 2,
            "store": 2,
            "marketplace": 0,
            "consumers": 0,
            "dealer": 0,
            "exported": 0,
            "client": 6,
            "distributing": 0,
            "distributions": 0,
            "demands": 4,
            "distributorship": 0,
            "exporting": 0,
            "wholesalers": 0,
            "receivable": 0,
            "receivables": 0,
            "suppliers": 0,
            "import": 14,
            "supplier": 4,
            "imports": 0,
            "imported": 0,
            "importation": 0,
            "vendors": 0,
            "subcontractors": 0,
            "subcontractor": 2,
            "vendor": 0,
            "importing": 0,
            "subcontract": 2,
            "purchase and from": 0,
            "purchased and from": 0,
            "subsidiaries": 16,
            "subsidiary": 86,
            "facilities": 58,
            "facility": 84,
            "venture": 46,
            "plant": 0,
            "exploration": 0,
            "plants": 0,
            "ventures": 4,
            "warehouse": 64,
            "storage": 4,
            "factory": 0,
            "warehouses": 30,
            "warehousing": 0,
            "factories": 0,
            "manufacturing": 24,
            "production": 6,
            "manufactured": 0,
            "manufacture": 32,
            "manufactures": 0,
            "produced": 4,
            "producing": 0,
            "produce": 16,
            "produces": 0,
            "productions": 0
        },
        "countries_found": [
            "Malta",
            "Germany",
            "Bahrain",
            "Maltese",
            "Hong Kong",
            "Netherlands",
            "Mauritius",
            "Puerto Rico",
            "Costa Rica",
            "Belize",
            "Panama",
            "Swiss",
            "Dutch",
            "Switzerland",
            "France",
            "Luxembourg",
            "Lebanon",
            "Bahamas",
            "Ireland",
            "Singapore",
            "Samoa"
        ]
    }
}
```

## Contributing

Feel free to submit issues or pull requests for improvements and bug fixes.

## License

This project is licensed under the MIT License.