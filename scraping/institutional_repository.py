"""Scraping functions lib."""
import requests

from bs4 import BeautifulSoup


class RIScraper(object):
    """Scraping UFRN's institutional repository."""

    @staticmethod
    def _reports_collection_url(pg_initials):
        pg_initials = pg_initials.upper()

        if pg_initials == 'PPGP':
            return 'https://repositorio.ufrn.br/jspui/handle/123456789/12031/'
        else:
            return None

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
                'date': date.text.split('-')[2].strip(),
                'url_sufix': title.find('a').get('href')[1:]
            })

        return final_reports
