"""
Data scrapper for final reports listing from SIGAA.
"""

import requests

from bs4 import BeautifulSoup

def ppgp_find_all():
    with open('Minerva/scrapping/final_reports_5678.html') as final_reports_html_file:
        reports_response_html = final_reports_html_file.read()

    reports_soup = BeautifulSoup(reports_response_html, 'html.parser')
    reports_listings = reports_soup.find_all('div', id='listagem_tabela')

    final_reports_by_year = {}

    for reports_listing in reports_listings:
        scrapped_year = str(int(reports_listing.find(id='group_lt').text))
        final_reports_by_year[scrapped_year] = []

        for reports_row in reports_listing.find_all('tr'):
            report_datas = reports_row.find_all('td')
            
            if len(report_datas) == 3:
                _, report_infos ,_ = report_datas

                if len(report_infos.find_all('li')) == 6:
                    author, title, counselor, date, _, abstract = report_infos.find_all('li')
                elif len(report_infos.find_all('li')) == 5:
                    author, title, date, _, abstract = report_infos.find_all('li')
                    counselor = None
                
                final_reports_by_year[scrapped_year].append({
                    'author': author.text.strip(),
                    'title': title.text.strip(),
                    'counselor': counselor.text.strip() if counselor else None,
                    'date': date.text.strip(),
                    'abstract': abstract.text.strip()
                })

    return final_reports_by_year



l = ppgp_find_all()
for y in l:
    print(y + ':')
    for i in l[y]:
        print('\t' + i['author'])
