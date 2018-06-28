"""Scraping functions lib."""
import re
import sys

import requests
from bs4 import BeautifulSoup


class SigaaScraper(object):
    """Scraping SIGAA pos-graduation website."""

    @staticmethod
    def _reports_collection_url(pg_initials):
        pg_initials = pg_initials.upper()
        dic_initials = {
            'PPGP' : '5679',
            'PPGA' : '74',
            'PPGCC' : '9066',
            'PPGD' : '404',
            'PPGECO' : '434',
            'PPGIC' : '9196',
            'PPGSS' : '376',
            'PPGTUR' : '4295'
        }

        return SigaaScraper.root() + dic_initials[pg_initials]

    @staticmethod
    def root():
        """Root of all Sigaa pos-graduation links."""
        return 'https://sigaa.ufrn.br/sigaa/public/programa/equipe.jsf?lc=pt_BR&id='

    @staticmethod
    def professors_list(pg_initials):
        """
        Return a list of final reports (dicts).
        Page param should be an integer beginning by 1
        """

        url = SigaaScraper._reports_collection_url(pg_initials)

        professors_list = {} 

        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        group_lts = soup.select('#conteudo #listagem_tabela #group_lt')
        table_lts = soup.select('#conteudo #listagem_tabela #table_lt')
        for group in range(0, len(group_lts)):
            groups_list = []
            for tr in table_lts[group].select('tbody tr'):
                tds = tr.select('td')
                if(tds[4].find('a')):
                    lattes = tds[4].find('a').get('href')
                else:
                    lattes = 'Não encontrado'
                if(tds[5].find('a')):
                    email = tds[5].find('a').get('href')[7:]
                else:
                    email = 'Não encontrado'
                groups_list.append({
                    'name': tds[0].text.strip(),
                    'rank': tds[1].text.strip(),
                    'level': tds[2].text.strip(),
                    'phone': tds[3].text.strip(),
                    'lattes': lattes,
                    'email': email,
                })
            groups_list.pop(0)
            professors_list[group_lts[group].text.strip()] = groups_list
        return professors_list

