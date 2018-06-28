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

######################################################
#Classes for testing scheduled reports
######################################################

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

    def edit_report(self, index, time, title, author, location):
        return self.app.post('/admin/editar_agendamento/', data=dict(
            index=index,
            time=time,
            title=title,
            author=author,
            location=location,
            create=True,
        ), follow_redirects=True)

    def check_report(self, initial):
        return self.app.get('/' + initial + '/')

##################################################
#Classes for testing events
#################################################

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

    def edit_event(self, index, title, initial_date, final_date, link, hour):
        return self.app.post('/admin/editar_evento/', data=dict(
            index=index,
            final_date=final_date,
            initial_date=initial_date,
            link=link,
            title=title,
            hour=hour,
            create=True
        ), follow_redirects=True)

    def check_event(self, initial):
        return self.app.get('/' + initial + '/calendario/')

######################################################
#Classes for testing subjects
#######################################################

    def add_subject(self, name, description, workload_in_hours, credits, requirement):
        return self.app.post('/admin/add_disciplinas/?course_type=Mestrado', data=dict(
            name=name,
            description=description,
            workload_in_hours=workload_in_hours,
            credits=credits,
            requirement=requirement,
            create=True
        ), follow_redirects=True)

    def delete_subject(self, name, description, workload_in_hours, credits, requirement, index):
        return self.app.post('/admin/deletar_disciplinas/?course_type=Mestrado', data=dict(
            index=index,
            name=name,
            description=description,
            workload_in_hours=workload_in_hours,
            credits=credits,
            requirement=requirement,
            create=True
        ), follow_redirects=True)

    def edit_subject(self, name, description, workload_in_hours, credits, requirement, index):
        return self.app.post('/admin/editar_disciplinas/?course_type=Mestrado', data=dict(
            index=index,
            name=name,
            description=description,
            workload_in_hours=workload_in_hours,
            credits=credits,
            requirement=requirement,
            create=True
        ), follow_redirects=True)

    def check_subject(self, initial):
        return self.app.get('/' + initial + '/disciplinas/')

#######################################################
#Teste professores
######################################################

    def add_professor(self, name, rank, lattes, email):
        return self.app.post('/admin/add_professors/', data=dict(
            name=name,
            rank=rank,
            lattes=lattes,
            email=email,
            create=True
        ), follow_redirects=True)

    def delete_professor(self, index, name, rank, lattes, email):
        return self.app.post('/admin/deletar_professors/', data=dict(
            index=index,
            name=name,
            rank=rank,
            lattes=lattes,
            email=email,
            create=True
        ), follow_redirects=True)

    def edit_professor(self, index, name, rank, lattes, email):
        return self.app.post('/admin/editar_professors/', data=dict(
            index=index,
            name=name,
            rank=rank,
            lattes=lattes,
            email=email,
            create=True
        ), follow_redirects=True)

    def check_professor(self, initial):
        return self.app.get('/' + initial + '/docentes/')

#################################################
#Classes for testing books
################################################

    def add_book(self, title, subtitle, authors, edition, location, publisher, year):
        return self.app.post('/admin/add_livro/', data=dict(
            title=title,
            subtitle=subtitle,
            authors=authors,
            edition=edition,
            location=location,
            publisher=publisher,
            year=year,
            create=True
        ), follow_redirects=True)

    def edit_book(self, index, title, subtitle, authors, edition, location, publisher, year):
        return self.app.post('/admin/editar_livro/', data=dict(
            index=index,
            title=title,
            subtitle=subtitle,
            authors=authors,
            edition=edition,
            location=location,
            publisher=publisher,
            year=year,
            create=True
        ), follow_redirects=True)

    def delete_book(self, index, title, subtitle, authors, edition, location, publisher, year):
        return self.app.post('/admin/deletar_livro/', data=dict(
            index=index,
            title=title,
            subtitle=subtitle,
            authors=authors,
            edition=edition,
            location=location,
            publisher=publisher,
            year=year,
            create=True
        ), follow_redirects=True)

    def check_books(self, initial):
        return self.app.get('/' + initial + '/livros/')

########################################################
#Classes for articles
########################################################

    def add_article(self, title, subtitle, authors, edition, location, publisher, number, pages, date):
        return self.app.post('/admin/add_artigo/', data=dict(
            title=title,
            subtitle=subtitle,
            authors=authors,
            edition=edition,
            location=location,
            publisher=publisher,
            number=number,
            pages=pages,
            date=date,
            create=True
        ), follow_redirects=True)

    def edit_article(self,index, title, subtitle, authors, edition, location, publisher, number, pages, date):
        return self.app.post('/admin/editar_artigo/', data=dict(
            index=index,
            title=title,
            subtitle=subtitle,
            authors=authors,
            edition=edition,
            location=location,
            publisher=publisher,
            number=number,
            pages=pages,
            date=date,
            create=True
        ), follow_redirects=True)

    def delete_article(self,index, title, subtitle, authors, edition, location, publisher, number, pages, date):
        return self.app.post('/admin/deletar_artigo/', data=dict(
            index=index,
            title=title,
            subtitle=subtitle,
            authors=authors,
            edition=edition,
            location=location,
            publisher=publisher,
            number=number,
            pages=pages,
            date=date,
            create=True
        ), follow_redirects=True)

    def check_article(self, initial):
        return self.app.get('/' + initial + '/artigos/')

########################################################
#Classes for testing participations 
########################################################
    
    def add_participation(self, title, description, year, international):
        return self.app.post('admin/intercambios/', data=dict(
            title=title,
            description=description,
            year=year,
            location=international,
            create=True
        ), follow_redirects=True)

    def edit_participation(self, index, title, description, year, international):
        return self.app.post('admin/editar_intercâmbio/', data=dict(
            index=index,
            title=title,
            description=description,
            year=year,
            location=international,
            create=True
        ), follow_redirects=True)

    def delete_participation(self, index, title, description, year, international):
        return self.app.post('admin/deletar_intercâmbio/', data=dict(
            index=index,
            title=title,
            description=description,
            year=year,
            location=international,
            create=True
        ), follow_redirects=True)
    
    def check_participation(self, initial):
        return self.app.get('/' + initial + '/intercambios/')

########################################################
#Classes for testing staff
#######################################################

    def add_staff(self, name, rank, abstract, function, photo):
        return self.app.post('admin/add_servidor/', data=dict(
            name=name,
            rank=rank,
            abstract=abstract,
            function=function,
            photo=photo,
            create=True
        ), follow_redirects=True)

    def edit_staff(self, index, name, rank, abstract, function, photo):
        return self.app.post('admin/add_servidor/', data=dict(
            index=index,
            name=name,
            rank=rank,
            abstract=abstract,
            function=function,
            photo=photo,
            create=True
        ), follow_redirects=True)

########################################################
#Tests for login
#######################################################

    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        response = self.login('ppgp-teste', 'luccas')
        assert b'Bem vindo' in response.data
        response = self.login('ppgcc-teste', 'luccas')
        assert b'Erro' in response.data
        response = self.login('ppgp-teste', 'lucas')
        assert b'Erro' in response.data
        response = self.login('ppgic-teste', 'luccas')
        assert b'Bem vindo' in response.data

###############################################################################################
#Tests involving reports
###############################################################################################

    def test_add_report_ok(self):
        #When all fields are filled correctly
        self.login('ppgic-teste', 'luccas')
        time = datetime.now()
        time = time.strftime('%d/%m/%Y %H:%M')
        self.add_report(time, 'Novas diretrizes no combate a corrupção', 'Pedro Lenza', 'Setor V Sala i4')
        result = self.check_report('PPGIC')
        assert b'Novas diretrizes' in result.data

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

    def test_edit_report(self):
        #Correct editing 
        self.login('ppgic-teste', 'luccas')
        time = datetime.now()
        time = time.strftime('%d/%m/%Y %H:%M')
        self.edit_report('0', time, 'Novas diretrizes...', 'João Vinicius', 'Setor IV Sala i4')
        result = self.check_report('PPGIC')
        assert b'Novas diretrizes...' in result.data

    def test_remove_report(self):
        #Correct deleting
        self.login('ppgic-teste', 'luccas')
        time = datetime.now()
        time = time.strftime('%d/%m/%Y %H:%M')
        self.delete_report('0', time, 'Novas diretrizes...', 'João Vinicius', 'Setor IV Sala i4')
        result = self.check_report('PPGIC')
        assert b'Novas diretrizes...' not in result.data

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
        self.add_event('Evento Teste', initial_date, final_date, 'https://google.com', '16:00')
        result = self.check_event('PPGIC')
        assert b'Evento Teste' in result.data

    def test_add_event_all_final_date_equals_initial(self):
        #Initial_date and final_date are equals
        self.login('ppgic-teste', 'luccas')
        initial_date = date(2017, 12, 7)
        initial_date = initial_date.strftime('%d/%m/%Y')
        final_date = date(2017, 12, 7)
        final_date = final_date.strftime('%d/%m/%Y')
        self.add_event('Inicial igual final', initial_date, final_date, 'https://google.com', '16:00')
        result = self.check_event('PPGIC')
        assert b'Inicial igual final' in result.data

    def test_add_event_all_no_hour(self):
        #No value in hour field
        self.login('ppgic-teste', 'luccas')
        initial_date = date(2017, 12, 7)
        initial_date = initial_date.strftime('%d/%m/%Y')
        final_date = date(2017, 12, 7)
        final_date = final_date.strftime('%d/%m/%Y')
        self.add_event('Evento sem hora',initial_date, final_date, 'https://google.com','')
        result = self.check_event('PPGIC')
        assert b'Evento sem hora' in result.data

    def test_add_event_no_final_date(self):
        #No value in final_date field
        self.login('ppgic-teste', 'luccas')
        initial_date = date(2017, 12, 7)
        initial_date = initial_date.strftime('%d/%m/%Y')
        final_date = date(2017, 12, 7)
        final_date = final_date.strftime('%d/%m/%Y')
        self.add_event('Evento sem data final', initial_date, '', 'https://google.com', '16:00')
        result = self.check_event('PPGIC')
        assert b'Evento sem data final' in result.data

    def test_add_event_no_link(self):
        #No value in link field
        self.login('ppgic-teste', 'luccas')
        initial_date = date(2017, 12, 7)
        initial_date = initial_date.strftime('%d/%m/%Y')
        final_date = date(2017, 12, 8)
        final_date = final_date.strftime('%d/%m/%Y')
        self.add_event('Evento sem link', initial_date, final_date, '' , '16:00')
        result = self.check_event('PPGIC')
        assert b'Evento sem link' in result.data

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

    def test_edit_event(self):
        #Edit event
        self.login('ppgic-teste', 'luccas')
        initial_date = date(2017, 12, 7)
        initial_date = initial_date.strftime('%d/%m/%Y')
        final_date = date(2017, 12, 7)
        final_date = final_date.strftime('%d/%m/%Y')
        self.edit_event('0', 'Evento Teste editado',initial_date, final_date, 'https://google.com','')
        result = self.check_event('PPGIC')
        assert b'Evento Teste editado' in result.data

    def test_delete_event(self):
        #Delete event
        self.login('ppgic-teste', 'luccas')
        initial_date = date(2017, 12, 7)
        initial_date = initial_date.strftime('%d/%m/%Y')
        final_date = date(2017, 12, 7)
        final_date = final_date.strftime('%d/%m/%Y')
        self.delete_event('0', 'Evento Teste editado',initial_date, final_date, 'https://google.com','')
        result = self.check_event('PPGIC')
        assert b'Evento Teste editado' not in result.data

###############################################################################################
#Tests involving subjects
###############################################################################################

    def test_subject_all_good(self):
        #Add subjects with everything ok
        self.login('ppgic-teste', 'luccas')
        self.add_subject('Nome exemplo tudo tranquilo', 'Descrição exemplo Descrição exemplo Descrição exemplo Descrição exemplo Descrição exemplo Descrição exemplo Descrição exemplo Descrição exemplo Descrição exemplo Descrição exemplo', '20', '3', 'Eletivas')
        result = self.check_subject('PPGIC')
        assert b'Nome exemplo' in result.data


    def test_subject_int_not_good(self):
        #Add subjects with credits and workload not numbers
        self.login('ppgic-teste', 'luccas')
        response = self.add_subject('Nome exemplo', 'Descrição exemplo Descrição exemplo Descrição exemplo Descrição exemplo Descrição exemplo Descrição exemplo Descrição exemplo Descrição exemplo Descrição exemplo Descrição exemplo', 'string', 'string','Eletivas')
        assert b'Erros' in response.data

    def test_edit_subject_all_good(self):
        #Delete subjects
        self.login('ppgic-teste', 'luccas')
        self.edit_subject('Nome exemplo editado', 'Descrição exemplo Descrição exemplo Descrição exemplo Descrição exemplo Descrição exemplo Descrição exemplo Descrição exemplo Descrição exemplo Descrição exemplo Descrição exemplo', '20', '4','Eletivas', '0')
        result = self.check_subject('PPGIC')
        assert b'Nome exemplo editado' in result.data

    def test_delete_subject_all_good(self):
        #Delete subjects
        self.login('ppgic-teste', 'luccas')
        self.delete_subject('Nome exemplo editado', 'Descrição exemplo Descrição exemplo Descrição exemplo Descrição exemplo Descrição exemplo Descrição exemplo Descrição exemplo Descrição exemplo Descrição exemplo Descrição exemplo', '20', '4','Eletivas', '0')
        result = self.check_subject('PPGIC')
        assert b'Nome exemplo editado' not in result.data

###########################################################
#Tests involving books
###########################################################

    def test_add_book(self):
        self.login('ppgic-teste', 'luccas')
        self.add_book('Grande sertao', '', 'João Guimarães Rosa', '12', 'Editora 34', 'São Paulo', '2002')
        result = self.check_books('PPGIC')
        assert b'Grande sertao' in result.data

    def test_add_book_bad_year(self):
        self.login('ppgic-teste', 'luccas')
        result = self.add_book('Grande sertao', '', 'João Guimarães Rosa', '12', 'Editora 34', 'São Paulo', 'badyear')
        assert b'Erro' in result.data

    def test_edit_book(self):
        self.login('ppgic-teste', 'luccas')
        self.edit_book('0', 'Grande sertao editado', '', 'João Guimarães Rosa', '12', 'Editora 34', 'São Paulo', '2002')
        result = self.check_books('PPGIC')
        assert b'Grande sertao editado' in result.data

    def test_delete_book(self):
        self.login('ppgic-teste', 'luccas')
        self.delete_book('0', 'Grande sertao', '', 'João Guimarães Rosa', '12', 'Editora 34', 'São Paulo', '2002')
        result = self.check_books('PPGIC')
        assert b'Grande sertao editado' not in result.data

#########################################################
#Tests involving articles
#########################################################

    def test_add_article(self):
        self.login('ppgic-teste', 'luccas')
        self.add_article('Grande sertao', '', 'João Guimarães Rosa', '12', 'São Paulo', 'Editora 34', '2', 'pag 12-20', 'jan 2012')
        result = self.check_article('PPGIC')
        assert b'Grande sertao' in result.data

    def test_add_article_bad_number(self):
        #Number not integer
        self.login('ppgic-teste', 'luccas')
        result = self.add_article('Grande sertao', '', 'João Guimarães Rosa', '12', 'São Paulo', 'Editora 34', 'badnumber', 'pag 12-20', 'jan 2012')
        assert b'Erro' in result.data

    def test_edit_article(self):
        self.login('ppgic-teste', 'luccas')
        self.edit_article('0', 'Grande sertao editado', '', 'João Guimarães Rosa', '12', 'São Paulo', 'Editora 34', '2', 'pag 12-20', 'jan 2012')
        result = self.check_article('PPGIC')
        assert b'Grande sertao editado' in result.data

    def test_delete_article(self):
        self.login('ppgic-teste', 'luccas')
        self.delete_article('0', 'Grande sertao editado', '', 'João Guimarães Rosa', '12', 'São Paulo', 'Editora 34', '2', 'pag 12-20', 'jan 2012')
        result = self.check_article('PPGIC')
        assert b'Grande sertao editado' not in result.data

##############################################################
#Tests involving participations
#############################################################

    def test_add_participation(self):
        self.login('ppgic-teste', 'luccas')
        self.add_participation('teste', 'Descricao teste', '2017', 'Paris Franca')
        result = self.check_participation('PPGIC')
        assert b'teste' in result.data

    def test_add_participation_invalid_year(self):
        self.login('ppgic-teste', 'luccas')
        result = self.add_participation('teste', 'Descricao teste','string', 'Paris Franca')
        assert b'Erro' in result.data

    def test_edit_participation(self):
        self.login('ppgic-teste', 'luccas')
        self.edit_participation('0', 'teste editado', 'Descricao teste','2017', 'Paris Franca')
        result = self.check_participation('PPGIC')
        assert b'teste editado' in result.data

    def test_delete_participation(self):
        self.login('ppgic-teste', 'luccas')
        self.delete_participation('0', 'Artigo teste editado', 'Descricao teste', '2017','Paris Franca')
        result = self.check_participation('PPGIC')
        assert b'teste editado' not in result.data

#################################################################
#Tests involving staff
#################################################################

if __name__ == "__main__":
    unittest.main()
