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
            location=location,
            create=True,
        ), follow_redirects=True)

    def add_event(self, title, initial_date, final_date, link, hour):
        return self.app.post('/admin/add_evento/', data=dict(
            final_date=final_date,
            initial_date=initial_date,
            link=link,
            title=title,
            hour=hour,
        ), follow_redirects=True)

    def delete_event(self, index, title, initial_date, final_date, link, hour):
        return self.app.post('/admin/deletar_evento/', data=dict(
            index=index,
            final_date=final_date,
            initial_date=initial_date,
            link=link,
            title=title,
            hour=hour,
            create=True
        ), follow_redirects=True)

    def add_subject(self, name, description, workload_in_hours, credits, requirement):
        return self.app.post('/admin/add_disciplinas/', data=dict(
            name=name,
            description=description,
            workload_in_hours=workload_in_hours,
            credits=credits,
            requirement=requirement,
            create=True
        ), follow_redirects=True)

    def delete_subject(self, name, description, workload_in_hours, credits, requirement, index):
        return self.app.post('/admin/deletar_disciplinas/', data=dict(
            index=index,
            name=name,
            description=description,
            workload_in_hours=workload_in_hours,
            credits=credits,
            requirement=requirement,
            create=True
        ), follow_redirects=True)


    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        response = self.login('ppgp-teste', 'luccas')
        assert b'Bem-vindo' in response.data
        response = self.login('ppgcc-teste', 'luccas')
        assert b'Erro' in response.data
        response = self.login('ppgp-teste', 'lucas')
        assert b'Erro' in response.data
        response = self.login('ppgic-teste', 'luccas')
        assert b'Bem-vindo' in response.data

###############################################################################################
#Tests involving reports
###############################################################################################

    def test_add_report_ok(self):
        #When all fields are filled correctly
        self.login('ppgic-teste', 'luccas')
        time = datetime.now()
        time = time.strftime('%d/%m/%Y %H:%M')
        response = self.add_report(time, 'Novas diretrizes no combate a corrupção', 'Pedro Lenza', 'Setor V Sala i4')
        assert b'sucesso' in response.data
        self.logout()

    def test_add_report_no_data(self):
        #When fields are filled with ""
        self.login('ppgic-teste', 'luccas')
        response = self.add_report('', '', '', '')
        assert b'Erros no preenchimento' in response.data

    def test_add_report_some_blank(self):
        #When some fields are left blank
        self.login('ppgic-teste', 'luccas')
        time = datetime.now()
        time = time.strftime('%d/%m/%Y %H:%M')
        response = self.add_report(time, '', 'João Vinicius', 'Setor IV Sala i4')
        assert b'Erros no preenchimento' in response.data

    def test_remove_report(self):
        #Correct deleting
        self.login('ppgic-teste', 'luccas')
        time = datetime.now()
        time = time.strftime('%d/%m/%Y %H:%M')
        response = self.delete_report('0', time, 'Novas diretrizes...', 'João Vinicius', 'Setor IV Sala i4')
        assert b'sucesso' in response.data

###############################################################################################
#Tests involving events
###############################################################################################

    def test_add_event_all(self):
        #Everything good and all fields inserted
        self.login('ppgic-teste', 'luccas')
        initial_date = date(2017, 12, 1)
        initial_date = initial_date.strftime('%d/%m/%Y')
        final_date = date(2017, 12, 7)
        final_date = final_date.strftime('%d/%m/%Y')
        response = self.add_event('Evento Teste', initial_date, final_date, 'https://google.com', '16:00')
        assert b'sucesso' in response.data

    def test_add_event_all_final_date_equals_initial(self):
        #Initial_date and final_date are equals
        self.login('ppgic-teste', 'luccas')
        initial_date = date(2017, 12, 7)
        initial_date = initial_date.strftime('%d/%m/%Y')
        final_date = date(2017, 12, 7)
        final_date = final_date.strftime('%d/%m/%Y')
        response = self.add_event('Evento Teste', initial_date, final_date, 'https://google.com', '16:00')
        assert b'sucesso' in response.data

    def test_add_event_all_no_hour(self):
        #No value in hour field
        self.login('ppgic-teste', 'luccas')
        initial_date = date(2017, 12, 7)
        initial_date = initial_date.strftime('%d/%m/%Y')
        final_date = date(2017, 12, 7)
        final_date = final_date.strftime('%d/%m/%Y')
        response = self.add_event('Evento Teste',initial_date, final_date, 'https://google.com','')
        assert b'sucesso' in response.data

    def test_add_event_no_final_date(self):
        #No value in final_date field
        self.login('ppgic-teste', 'luccas')
        initial_date = date(2017, 12, 7)
        initial_date = initial_date.strftime('%d/%m/%Y')
        final_date = date(2017, 12, 7)
        final_date = final_date.strftime('%d/%m/%Y')
        response = self.add_event('Evento Teste', initial_date, '', 'https://google.com', '16:00')
        assert b'sucesso' in response.data

    def test_add_event_no_link(self):
        #No value in link field
        self.login('ppgic-teste', 'luccas')
        initial_date = date(2017, 12, 7)
        initial_date = initial_date.strftime('%d/%m/%Y')
        final_date = date(2017, 12, 8)
        final_date = final_date.strftime('%d/%m/%Y')
        response = self.add_event('Evento Teste', initial_date, final_date, '' , '16:00')
        assert b'sucesso' in response.data

    def test_add_event_nothing(self):
        #Nothing inserted
        self.login('ppgic-teste', 'luccas')
        initial_date = date(2017, 12, 7)
        initial_date = initial_date.strftime('%d/%m/%Y')
        final_date = date(2017, 12, 8)
        final_date = final_date.strftime('%d/%m/%Y')
        response = self.add_event('', '', '', '', '')
        assert b'Erro' in response.data

    def test_add_event_all_no_title(self):
        #Title not inserted
        self.login('ppgic-teste', 'luccas')
        initial_date = date(2017, 12, 7)
        initial_date = initial_date.strftime('%d/%m/%Y')
        final_date = date(2017, 12, 8)
        final_date = final_date.strftime('%d/%m/%Y')
        response = self.add_event('',initial_date, final_date, '16:00 a 18:00', 'https://google.com')
        assert b'Erro' in response.data

    def test_add_event_all_no_initial_date(self):
        #Initial date not inserted
        self.login('ppgic-teste', 'luccas')
        initial_date = date(2017, 12, 7)
        initial_date = initial_date.strftime('%d/%m/%Y')
        final_date = date(2017, 12, 8)
        final_date = final_date.strftime('%d/%m/%Y')
        response = self.add_event('Evento teste','', final_date, '16:00 a 18:00', 'https://google.com')
        assert b'Erro' in response.data

    def test_delete_event(self):
        #Delete event
        self.login('ppgic-teste', 'luccas')
        initial_date = date(2017, 12, 7)
        initial_date = initial_date.strftime('%d/%m/%Y')
        final_date = date(2017, 12, 7)
        final_date = final_date.strftime('%d/%m/%Y')
        response = self.delete_event('0', 'Evento Teste',initial_date, final_date, 'https://google.com','')
        assert b'sucesso' in response.data

###############################################################################################
#Tests involving subjects
###############################################################################################

    def test_subject_all_good(self):
        #Add subjects with everything ok
        self.login('ppgp-teste', 'luccas')
        response = self.add_subject('Nome exemplo', 'Descrição exemplo Descrição exemplo Descrição exemplo Descrição exemplo Descrição exemplo Descrição exemplo Descrição exemplo Descrição exemplo Descrição exemplo Descrição exemplo', '20', '3', 'Eletivas')
        assert b'sucesso' in response.data

    def test_subject_int_not_good(self):
        #Add subjects with credits and workload not numbers
        self.login('ppgp-teste', 'luccas')
        response = self.add_subject('Nome exemplo', 'Descrição exemplo Descrição exemplo Descrição exemplo Descrição exemplo Descrição exemplo Descrição exemplo Descrição exemplo Descrição exemplo Descrição exemplo Descrição exemplo', 'string', 'string','Eletivas')
        assert b'erro' in response.data

    def test_delete_subject_all_good(self):
        #Delete subjects
        self.login('ppgp-teste', 'luccas')
        response = self.delete_subject('Nome exemplo', 'Descrição exemplo Descrição exemplo Descrição exemplo Descrição exemplo Descrição exemplo Descrição exemplo Descrição exemplo Descrição exemplo Descrição exemplo Descrição exemplo', '20', '4','Eletivas', '0')
        assert b'sucesso' in response.data

if __name__ == "__main__":
    unittest.main()
