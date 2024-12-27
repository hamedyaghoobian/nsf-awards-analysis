# NSF Awards Analysis Tool

A Python-based tool for analyzing National Science Foundation (NSF) awards data, specifically focused on AI, data science, and sociotechnical research proposals.

## Features

- Search NSF awards database using customizable keywords
- Analyze funding patterns and distributions
- Generate comprehensive reports in markdown format
- Identify relevant proposals based on research focus
- Track funding trends across institutions and programs

## Installation

1. Clone the repository:
```bash
git clone https://github.com/hamedyaghoobian/nsf-awards-analysis.git
cd nsf-awards-analysis
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Scraping NSF Awards Data

Run the scraper to fetch awards data:
```bash
python nsf_awards_scraper.py
```

This will:
- Search the NSF database using predefined keywords
- Save results in both CSV and JSON formats
- Include award details like title, amount, PI, and institution

### Analyzing Awards

Run the analysis script to process the collected data:
```bash
python analyze_nsf_awards.py
```

This will:
- Generate a comprehensive markdown report
- Provide statistical analysis of awards
- Identify relevant proposals
- Offer research recommendations

## Output Files

The tool generates several types of files:

1. **CSV Files**: Raw award data in tabular format
   - `nsf_awards_ai_data_[timestamp].csv`
   - `nsf_awards_sociotech_[timestamp].csv`

2. **JSON Files**: Complete award data including all fields
   - `nsf_awards_ai_data_[timestamp].json`
   - `nsf_awards_sociotech_[timestamp].json`

3. **Analysis Report**: Comprehensive markdown report
   - `nsf_awards_analysis.md`

## Analysis Features

The analysis includes:
- Basic statistics (award counts, total funding, averages)
- Temporal distribution of awards
- Top funding programs
- Leading institutions
- Relevant awards based on keywords
- Research recommendations

## Contributing

Feel free to submit issues and enhancement requests! 