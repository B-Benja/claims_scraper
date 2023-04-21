"""
This script scrapes the number of independent and dependent claims for patents
from Google Patents and saves the results in a CSV file.
"""

import csv
import requests
from bs4 import BeautifulSoup

G_PATENTS = 'https://patents.google.com/patent/'
INPUT_CSV = 'input.csv'
OUTPUT_CSV = 'output.csv'
ERROR_DB = 'errors.csv'

with open(INPUT_CSV, 'r') as input_file:
    file = csv.reader(input_file, delimiter=',')
    for i, row in enumerate(file):
        patent = row[0].replace(' ', '') + row[1]
        url = f'{G_PATENTS}{patent}'
        request = requests.get(url=url)

        if request.status_code == 404:
            with open(ERROR_DB, 'a') as output:
                result = csv.writer(output, delimiter=';', lineterminator='\n')
                result.writerow([row[0], row[1], 'Patent not found', url])
        else:
            soup = BeautifulSoup(request.text, 'html.parser')

            try:
                # Get everything claims related
                claims = soup.find('section', {'itemprop': 'claims'})

                # Get the total number of claims
                claims_total = int(claims.find('span', {'itemprop': 'count'}).text)

                # Get the number of dependent claims
                claims_dep = len(claims.findAll('div', {'class': 'claim-dependent'}))

                # Calculate the number of independent claims
                claims_indep = claims_total - claims_dep

                with open(OUTPUT_CSV, 'a') as output:
                    result = csv.writer(output, delimiter=';', lineterminator='\n')
                    result.writerow([row[0], row[1], claims_total, claims_indep, claims_dep, url])

            except AttributeError:
                with open(ERROR_DB, 'a') as output:
                    result = csv.writer(output, delimiter=';', lineterminator='\n')
                    result.writerow([row[0], row[1], 'No Claims found', url])

            except:
                with open(ERROR_DB, 'a') as output:
                    result = csv.writer(output, delimiter=';', lineterminator='\n')
                    result.writerow([row[0], row[1], 'Other error', url])

        print(f"Done: {i}")
