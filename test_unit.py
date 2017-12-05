import os 
import unittest

from app import APP as app_de_teste 
from pymongo import MongoClient

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
            nick = nick,
            password = password), follow_redirects=True)

    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        response = self.login('correct_login', 'correct_password')
        assert b'Bem-vindo' in response.data
        response = self.login('incorrect_login', 'correct_password')
        assert b'Erro' in response.data
        response = self.login('correct_login', 'incorrect_password')
        assert b'Erro' in response.data

if __name__ == "__main__":
       unittest.main()



