"""Scraping functions lib."""
import re

import requests
from bs4 import BeautifulSoup


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
        url += 'browse?type=dateissued&sort_by=2&order=DESC&rpp={qtt}&etal=-1&null=&offset={first}'
        url = url.format(qtt=10, first=page*10)

        final_reports = list()

        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.select("td[headers]")
        len_table = len(table)
        for element in range(0, len_table, 3):
            date = table[element]
            title = table[element + 1]
            author = table[element + 2]

            final_reports.append({
                'author': author.text.strip(),
                'title': title.text.strip(),
                'year': date.text.split('-')[2].strip(),
                'link': RIScraper.root() + title.find('a').get('href')[1:]
            })

        page_info = soup.find('div', {'class': 'panel-heading text-center'})

        page_info = page_info.text.replace('\n', '')
        search = r'.*Mostrando resultados [0-9]+ a [0-9]+ de (?P<max_page>[0-9]+).*'
        match = re.match(search, page_info)

        max_page = match.group('max_page') if match is not None else -1

        return final_reports, int(max_page)

