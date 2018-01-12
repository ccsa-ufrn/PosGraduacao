import os
import unittest

from datetime import datetime, date
from app import APP as app_de_teste

class BasicTests(unittest.TestCase):

    def setUp(self):
        app_de_teste.config['TESTING'] = True
        app_de_teste.config['WTF_CSRF_ENABLED'] = False
        app_de_teste.config['DEBUG'] = False
        self.app = app_de_teste.test_client()

    def tearDown(self):
        pass

    def login(self, nick, password):
        return self.app.post('/admin/login/', data=dict(
            nick=nick,
            password=password), follow_redirects=True)

    def logout(self):
        return self.app.get('/admin/logout/', follow_redirects=True)

    def add_project(self):
        return self.app.get('/admin/add_projetos/', follow_redirects=True)

    def test_project(self):
        self.login('ppgp-teste', 'luccas')
        self.add_project()

if __name__ == "__main__":
    unittest.main()
