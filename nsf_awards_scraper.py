import requests
import pandas as pd
from datetime import datetime
import json
import time

class NSFAwardsScraper:
    def __init__(self):
        self.base_url = "https://api.nsf.gov/services/v1/awards.json"
        
    def search_awards(self, keywords, printFields=None, offset=None):
        """
        Search NSF awards using keywords
        
        Args:
            keywords (str): Search terms
            printFields (list): Specific fields to return
            offset (int): Starting point for results
        """
        params = {
            'keyword': keywords,
            'printFields': ','.join(printFields) if printFields else None,
        }
        
        # Only add offset if it's provided
        if offset is not None:
            params['offset'] = offset
        
        try:
            print(f"Searching with parameters: {params}")
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
            print(f"Response status code: {response.status_code}")
            return data
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            if hasattr(e, 'response') and hasattr(e.response, 'text'):
                print(f"Response text: {e.response.text}")
            return None

    def save_results(self, results, filename):
        """Save results to a JSON file"""
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)

def main():
    scraper = NSFAwardsScraper()
    
    # Fields we want to retrieve - using correct API field names
    fields = [
        'id',
        'title',
        'startDate',
        'expDate',
        'awardeeName',
        'awardeeStateCode',
        'fundProgramName',
        'piFirstName',
        'piLastName',
        'estimatedTotalAmt',
        'abstractText'  # Adding abstract to see the research description
    ]
    
    # Broader search terms focusing on social studies of technology and innovation
    search_terms = 'sociotechnical+innovation+ethnography+qualitative+technology'
    
    # Get results
    results = scraper.search_awards(
        keywords=search_terms,
        printFields=fields
    )
    
    if results:
        if 'response' in results:
            response_data = results['response']
            
            if 'serviceNotification' in response_data:
                print("\nAPI Notifications:")
                for notification in response_data['serviceNotification']:
                    print(f"- {notification.get('notificationType', 'UNKNOWN')}: {notification.get('notificationMessage', 'No message')}")
                return
            
            if isinstance(response_data, dict) and 'award' in response_data:
                awards = pd.DataFrame(response_data['award'])
                
                if not awards.empty:
                    # Save raw results
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    scraper.save_results(results, f'nsf_awards_sts_{timestamp}.json')
                    
                    # Save to CSV
                    csv_filename = f'nsf_awards_sts_{timestamp}.csv'
                    awards.to_csv(csv_filename, index=False)
                    print(f"\nFound {len(awards)} awards related to Science & Technology Studies. Data saved to:")
                    print(f"- CSV: {csv_filename}")
                    print(f"- JSON: nsf_awards_sts_{timestamp}.json")
                    
                    print("\nSample of found awards:")
                    for _, award in awards.head().iterrows():
                        print(f"\nTitle: {award.get('title', 'N/A')}")
                        print(f"Amount: ${float(award.get('estimatedTotalAmt', 0)):,.2f}")
                        print(f"Program: {award.get('fundProgramName', 'N/A')}")
                        print(f"Institution: {award.get('awardeeName', 'N/A')}")
                        print(f"PI: {award.get('piFirstName', '')} {award.get('piLastName', '')}")
                        if 'abstractText' in award:
                            abstract = award.get('abstractText', '')
                            if abstract:
                                print(f"\nAbstract excerpt: {abstract[:300]}...")
                        print("-" * 80)
                    
                    if 'fundProgramName' in awards.columns:
                        print("\nTop funding programs for STS research:")
                        print(awards['fundProgramName'].value_counts().head())
                    
                    if 'estimatedTotalAmt' in awards.columns:
                        print("\nAverage award amount:", f"${awards['estimatedTotalAmt'].astype(float).mean():,.2f}")
                        
                    # Additional analysis
                    if 'startDate' in awards.columns:
                        awards['startDate'] = pd.to_datetime(awards['startDate'])
                        print("\nTemporal distribution:")
                        print(awards['startDate'].dt.year.value_counts().sort_index())
                        
                    # State distribution
                    if 'awardeeStateCode' in awards.columns:
                        print("\nGeographic distribution (top states):")
                        print(awards['awardeeStateCode'].value_counts().head())
                else:
                    print("\nNo awards found matching the search criteria.")
            else:
                print("\nNo awards found in the response or unexpected response structure.")
                if isinstance(response_data, dict):
                    print("Response keys:", response_data.keys())
        else:
            print("\nNo 'response' key in the API result.")
            print("Available keys:", results.keys())
    else:
        print("\nNo results returned from the API.")
        
if __name__ == "__main__":
    main() 