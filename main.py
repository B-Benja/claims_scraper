## scraping number of patent claims
import csv
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


G_PATENTS = 'https://patents.google.com/patent/'
INPUT_CSV = 'input.csv'
OUTPUT_CSV = 'output.csv'
ERROR_DB = 'errors.csv'

i = 0
with open(INPUT_CSV, 'r') as input:
    file = csv.reader(input, delimiter=',')
    for row in file:
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
            # get everything claims related
                claims = soup.find('section', {'itemprop': 'claims'})

                # get the number of all claims
                claims_total = int(claims.find('span', {'itemprop': 'count'}).text)

                # number of dependent claims
                claims_dep = len(claims.findAll('div', {'class': 'claim-dependent'}))

                # number of independent claims (there is no clear way to identify independent claims;
                # therefore no. indep. claims = total - dep. claims)
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
        i += 1