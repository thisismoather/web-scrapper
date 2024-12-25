# Web Scraper for Company Website Analysis

This project is a web scraper designed to analyze company websites by counting mentions of non-U.S. countries and categorizing them into tax groups. It also tracks occurrences of specific "Offshore words" within the same sentences.

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
└── README.md             # Project documentation
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd web-scraper
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Configuration

Edit the `config.yaml` file to specify the websites to scrape and define tax groups.

## Usage

To run the web scraper, execute the following command:
```
python src/scraper.py
```

## Contributing

Feel free to submit issues or pull requests for improvements and bug fixes.

## License

This project is licensed under the MIT License.