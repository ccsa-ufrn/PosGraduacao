"""Scraping functions lib."""
import re
import math
import sys

import requests
from bs4 import BeautifulSoup


def get_final_report_details(tr):
    final_report = {
        'date': tr.find(headers='t1').text.strip(),
        'author': tr.find(headers='t3').text.strip(),
        'title': tr.find(headers='t2').text.strip(),
        'link': f"https://repositorio.ufrn.br{tr.find(headers='t2').find('a').get('href')}",
    }
    return final_report

class RIScraper(object):
    """Scraping UFRN's Institutional Repository."""

    @staticmethod
    def _reports_collection_url(pg_initials, modality):
        pg_initials = pg_initials.upper()
        if modality != 'phd':
            dic_initials = {
                'PPGP' : 'jspui/handle/123456789/12031/',
                'PPGA' : 'jspui/handle/123456789/11886/',
                'PPGCC' : 'jspui/handle/123456789/23373/',
                'PPGD' : 'jspui/handle/123456789/11997/',
                'PPGECO' : 'jspui/handle/123456789/11999/',
                'PPGIC' : 'jspui/handle/123456789/24097/',
                'PPGSS' : 'jspui/handle/123456789/12057/',
                'PPGTUR' : 'jspui/handle/123456789/12062/'
            }
        else:
            dic_initials = { 'PPGA' : 'jspui/handle/123456789/11887/' }

        return RIScraper.root() + dic_initials[pg_initials]

    @staticmethod
    def root():
        """Root of all RIs links."""
        return 'https://repositorio.ufrn.br/'

    @staticmethod
    def final_reports_list(pg_initials, page, modality):
        """
        Return a list of final reports (dicts).
        Page param should be an integer beginning by 1
        """
        page -= 1

        url = RIScraper._reports_collection_url(pg_initials, modality)
        url += '?offset=' + str(page * 20)
        print(url, file=sys.stderr)

        final_reports = list()

        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.select(".table tr")[1:]

        page_info = list(filter(lambda x: x.isnumeric(), soup.find(class_='browse_range').text.replace('\n', '').split(' ')))[-1]

        max_page = math.ceil((int(page_info)/20)) if page_info is not None else 1
        return list(map(get_final_report_details, table)), int(max_page)

    @staticmethod
    def miscelaneous_list(list_url):
        """
        Return a list of miscelaneous (dicts).
        """
        miscelaneous_list = list()
        for url in list_url:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            table = soup.select("td[headers]")
            len_table = len(table)
            for element in range(0, len_table, 3):
                date = table[element]
                title = table[element + 1]
                author = table[element + 2]

                miscelaneous_list.append({
                    'author': author.text.strip(),
                    'title': title.text.strip(),
                    'year': date.text.split('-')[2].strip(),
                    'link': RIScraper.root() + title.find('a').get('href')[1:]
                })

        return miscelaneous_list, 1
