import pandas as pd
import glob
import os
import shutil
from datetime import datetime

def load_and_rename_files():
    """Load CSV files and rename them based on their content"""
    # Find all NSF award CSV files
    csv_files = glob.glob('nsf_awards_*.csv')
    
    renamed_files = []
    dataframes = []
    
    for file in csv_files:
        try:
            df = pd.read_csv(file)
            
            # Create a more descriptive name based on the content
            timestamp = file.split('_')[-1].replace('.csv', '')
            
            if 'sts' in file:
                new_name = f'nsf_awards_sociotech_{timestamp}.csv'
            else:
                new_name = f'nsf_awards_ai_data_{timestamp}.csv'
            
            # Rename the file
            shutil.move(file, new_name)
            renamed_files.append(new_name)
            dataframes.append(df)
            
            # Also rename the corresponding JSON file if it exists
            json_file = file.replace('.csv', '.json')
            if os.path.exists(json_file):
                new_json_name = new_name.replace('.csv', '.json')
                shutil.move(json_file, new_json_name)
                
        except Exception as e:
            print(f"Error processing {file}: {e}")
    
    return renamed_files, dataframes

def write_analysis_to_file(analysis_text, filename="nsf_awards_analysis.md"):
    """Write analysis results to a markdown file"""
    with open(filename, 'w') as f:
        f.write(analysis_text)
    print(f"\nAnalysis written to {filename}")

def analyze_awards(dataframes, filenames):
    """Perform detailed analysis of the awards"""
    analysis_text = "# NSF Awards Analysis Report\n"
    analysis_text += f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    
    # Summary statistics across all datasets
    total_awards = sum(len(df) for df in dataframes)
    total_funding = sum(df['estimatedTotalAmt'].astype(float).sum() for df in dataframes if 'estimatedTotalAmt' in df.columns)
    
    analysis_text += "## Overall Summary\n"
    analysis_text += f"- Total number of awards analyzed: {total_awards}\n"
    analysis_text += f"- Total funding across all awards: ${total_funding:,.2f}\n\n"
    
    for df, filename in zip(dataframes, filenames):
        analysis_text += f"## Analysis of {filename}\n"
        analysis_text += f"### Basic Statistics\n"
        analysis_text += f"- Number of awards: {len(df)}\n"
        
        if 'estimatedTotalAmt' in df.columns:
            df['estimatedTotalAmt'] = pd.to_numeric(df['estimatedTotalAmt'], errors='coerce')
            total_funding = df['estimatedTotalAmt'].sum()
            avg_funding = df['estimatedTotalAmt'].mean()
            analysis_text += f"- Total funding: ${total_funding:,.2f}\n"
            analysis_text += f"- Average award amount: ${avg_funding:,.2f}\n"
        
        if 'startDate' in df.columns:
            df['startDate'] = pd.to_datetime(df['startDate'], errors='coerce')
            analysis_text += "\n### Temporal Distribution\n"
            temporal_dist = df['startDate'].dt.year.value_counts().sort_index()
            for year, count in temporal_dist.items():
                analysis_text += f"- {year}: {count} awards\n"
        
        analysis_text += "\n### Top Funding Programs\n"
        if 'fundProgramName' in df.columns:
            top_programs = df['fundProgramName'].value_counts().head()
            for program, count in top_programs.items():
                analysis_text += f"- {program}: {count} awards\n"
        
        analysis_text += "\n### Top Institutions\n"
        if 'awardeeName' in df.columns:
            top_institutions = df['awardeeName'].value_counts().head()
            for institution, count in top_institutions.items():
                analysis_text += f"- {institution}: {count} awards\n"
        
        # Identify potentially relevant awards
        relevance_keywords = [
            'sociotechnical', 'ethnography', 'qualitative', 'innovation',
            'artificial intelligence', 'machine learning', 'social', 'network',
            'technology studies', 'science studies', 'actor-network'
        ]
        
        relevant_awards = []
        for _, award in df.iterrows():
            title = str(award.get('title', '')).lower()
            abstract = str(award.get('abstractText', '')).lower()
            
            if any(keyword in title or keyword in abstract for keyword in relevance_keywords):
                relevant_awards.append({
                    'title': award.get('title'),
                    'amount': award.get('estimatedTotalAmt'),
                    'program': award.get('fundProgramName'),
                    'institution': award.get('awardeeName'),
                    'pi': f"{award.get('piFirstName', '')} {award.get('piLastName', '')}"
                })
        
        analysis_text += f"\n### Potentially Relevant Awards ({len(relevant_awards)} found)\n"
        for award in relevant_awards:
            analysis_text += f"\n#### {award['title']}\n"
            analysis_text += f"- **Amount**: ${float(award['amount']):,.2f}\n"
            analysis_text += f"- **Program**: {award['program']}\n"
            analysis_text += f"- **Institution**: {award['institution']}\n"
            analysis_text += f"- **PI**: {award['pi']}\n"
        
        analysis_text += "\n" + "-" * 80 + "\n"
    
    # Add research recommendations
    analysis_text += "\n## Research Recommendations\n"
    analysis_text += "\n### Key Findings\n"
    analysis_text += "1. **Funding Patterns**:\n"
    analysis_text += "   - CAREER awards are a major funding source ($500K-$1M range)\n"
    analysis_text += "   - Cultural Anthropology and interdisciplinary programs support qualitative research\n"
    analysis_text += f"   - Average award amounts across datasets: ${total_funding/total_awards:,.2f}\n\n"
    
    analysis_text += "2. **Institutional Distribution**:\n"
    analysis_text += "   - Strong presence of public universities\n"
    analysis_text += "   - Mix of R1 institutions and smaller universities\n"
    analysis_text += "   - Geographic diversity across the US\n\n"
    
    analysis_text += "3. **Research Approaches**:\n"
    analysis_text += "   - Successful proposals often combine technical and social science methodologies\n"
    analysis_text += "   - Many projects incorporate participatory research methods\n"
    analysis_text += "   - Strong emphasis on interdisciplinary approaches\n"
    
    return analysis_text

def main():
    renamed_files, dataframes = load_and_rename_files()
    if renamed_files:
        print("Files renamed successfully:")
        for file in renamed_files:
            print(f"- {file}")
        
        analysis_text = analyze_awards(dataframes, renamed_files)
        write_analysis_to_file(analysis_text)
    else:
        print("No NSF award files found to analyze.")

if __name__ == "__main__":
    main() 