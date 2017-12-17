import os 
import unittest

from app import APP as app_de_teste 
from pymongo import MongoClient
from models.clients.mongo import __DB_NAME as db_name
from datetime import datetime

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

    def logout(self):
        return self.app.get('/admin/logout/', follow_redirects=True)

    def add_report(self, time, title, author, location):
        return self.app.post('/admin/apresentacoes/', data=dict(
            time=time,
            title=title,
            author=author,
            location=location
        ), follow_redirects=True)
        
    def delete_report(self, index, time, title, author, location):
        return self.app.post('/admin/deletar_agendamento/', data=dict(
            index=index,
            time=time,
            title=title,
            author=author,
            location=location
        ), follow_redirects=True)

    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        response = self.login('correct_username', 'correct_password')
        assert b'Bem-vindo' in response.data
        response = self.login('incorrect_username', 'correct_password')
        assert b'Erro' in response.data
        response = self.login('correct_username', 'incorrect_password')
        assert b'Erro' in response.data
 
    def test_add_report_ok(self):
        #When all fields are filled correctly
        self.login('', '')
        time = datetime.now()
        time = time.strftime('%d/%m/%Y %H:%M')
        response = self.add_report(time, 'Novas diretrizes no combate a corrupção', 'Pedro Lenza', 'Setor V Sala i4')
        assert b'sucesso' in response.data
        self.logout()

    def test_add_report_no_data(self):
        #When fields are filled with ""
        self.login('', '')
        response = self.add_report('', '', '', '')
        assert b'Erros no preenchimento' in response.data

    def test_add_report_some_blank(self):
        #When some fields are left blank
        self.login('', '')
        time = datetime.now()
        time = time.strftime('%d/%m/%Y %H:%M')
        response = self.add_report(time,'', 'João Vinicius', 'Setor IV Sala i4')
        assert b'Erros no preenchimento' in response.data
    
    def test_delete_report_ok(self):
        #When index is correct even tough the other fields are not
        self.login('', '')
        time = datetime.now()
        time = time.strftime('%d/%m/%Y %H:%M')
        response = self.delete_report(1, time, 'Novas diretrizes no combate a corrupção', 'Pedro Lenza', 'Setor V Sala i4')
        assert b'sucesso' in response.data
        self.logout()

if __name__ == "__main__":
       unittest.main()



