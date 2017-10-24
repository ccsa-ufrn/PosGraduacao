"""Scraping functions lib."""
import re

import requests
from bs4 import BeautifulSoup


class RIScraper(object):
    """Scraping UFRN's Institutional Repository."""

    @staticmethod
    def _reports_collection_url(pg_initials):
        pg_initials = pg_initials.upper()

        if pg_initials == 'PPGP':
            return RIScraper.root() + 'jspui/handle/123456789/12031/'
        else:
            return None

    @staticmethod
    def root():
        """Root of all RIs links."""
        return 'https://repositorio.ufrn.br/'

    @staticmethod
    def final_reports_list(pg_initials, page):
        """
        Return a list of final reports (dicts).
        Page param should be an integer beginning by 1
        """
        page -= 1

        url = RIScraper._reports_collection_url(pg_initials)
        url += 'browse?type=dateissued&sort_by=2&order=DESC&rpp={qtt}&etal=-1&null=&offset={first}'
        url = url.format(qtt=10, first=page*10)

        final_reports = list()

        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        table = soup.find('table', summary='This table browses all dspace content')
        rows = table.find_all('tr')
        del rows[0]

        for row in rows:
            date, title, author = row.find_all('td')

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
