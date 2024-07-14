import os
from bs4 import BeautifulSoup

def scrape_cve_search_results_from_files(directory, output_file):
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for filename in os.listdir(directory):
            if filename.endswith(".html"):
                filepath = os.path.join(directory, filename)
                outfile.write(f"Scraping search results from: {filepath}\n")
                with open(filepath, 'r', encoding='utf-8') as file:
                    content = file.read()
                    soup = BeautifulSoup(content, 'html.parser')
                    
                    # Find the div containing the table
                    table_div = soup.find('div', id='TableWithRules')
                    if table_div:
                        # Find the table inside the div
                        table = table_div.find('table')
                        if table:
                            # Find all rows in the table body
                            rows = table.find_all('tr')
                            for row in rows:
                                # Find all cells in the row
                                cells = row.find_all('td')
                                if cells:
                                    # Extract CVE name and description
                                    cve_name = cells[0].text.strip()
                                    cve_description = cells[1].text.strip()
                                    # Write to output file
                                    outfile.write(f"Name: {cve_name}\nDescription: {cve_description}\n\n")
                        else:
                            outfile.write("No CVE search results table found.\n\n")
                    else:
                        outfile.write("No CVE search results table div found.\n\n")

# Directory containing .html files
# directory = 'cve_pages'

# # Output text file
# output_file = 'results.txt'

# # Call function to scrape search results from files and write to text file
# scrape_cve_search_results_from_files(directory, output_file)
