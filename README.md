# NSF Awards Scraper

This tool helps search and analyze NSF (National Science Foundation) awards related to AI and data-driven approaches.

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Run the scraper:
```bash
python nsf_awards_scraper.py
```

## Output

The script will generate two files with timestamps:
- A JSON file containing the raw data
- A CSV file for easier analysis in spreadsheet software

The script will also print:
- Number of awards found
- Top funding programs
- Average award amount

## Customization

You can modify the `search_terms` variable in the script to search for different keywords or topics. The current search focuses on AI and data-driven approaches. 