"""
All data **MUST** be only manipulated through this middleware,
and not directly using Pymongo nor other API wrapper. And also,
all DAOs **SHOULD** be created using factory methods.
"""
from threading import Thread
import sys

from models.clients.mongo import DB
from models.clients import api_sistemas


class AbstractDAO(object):

    def __init__(self, collection: str):
        raise NotImplementedError("Tried to create instance from abstract class.")

    def find_all(self):
        raise NotImplementedError("Not implemented method inherited from an abstract class.")

    def find_one(self, conditions: dict):
        raise NotImplementedError("Not implemented method inherited from an abstract class.")

    def find(self, conditions: dict):
        raise NotImplementedError("Not implemented method inherited from an abstract class.")

    def count(self, conditions: dict):
        raise NotImplementedError("Not implemented method inherited from an abstract class.")


    def insert_one(self, document: dict):
        raise NotImplementedError("Not implemented method inherited from an abstract class.")

    def insert_many(self, document: list):
        raise NotImplementedError("Not implemented method inherited from an abstract class.")

    def update(self, document: dict):
        raise NotImplementedError("Not implemented method inherited from an abstract class.")

    def delete(self, document: dict):
        raise NotImplementedError("Not implemented method inherited from an abstract class.")



class GenericMongoDAO(AbstractDAO):
    """
    Implements a generic middleware for accessing MongoDB.

    Note that this instance itself don't represent anything at domain,
    it's just useful for accessing dictionaries that stands for documents
    from a certain database collection.
    """

    def __init__(self, collection: str, owner_post_graduation_id: str = None):
        """
        Don't use this constructor directly as you're probably doing now.
        Use its factory instead!

        Create an instance for starting using data access methods.

        All data access will assume as context the given collection.
        Also, will add a 'ownerProgram' search parameter as
        owner_post_graduation_id to all data filterings. Collection
        name must never be None.
        """
        self.collection = collection
        self.owner_post_graduation_id = owner_post_graduation_id

    def find_all(self):
        """
        Gets a list of all the documents from the collection.
        TODO: retrieve only logical alive documents (maybe a 'alive_only=True' param?)
        """
        return DB[self.collection].find_all()

    def find_one(self, conditions: dict = None):
        """
        Gets a single found document with the given conditions, returns it as dict.
        TODO: retrieve only logical alive documents (maybe a 'alive_only=True' param?)
        """
        if conditions is None:
            conditions = {}
        if self.owner_post_graduation_id is not None:
            conditions['ownerProgram'] = self.owner_post_graduation_id
        return DB[self.collection].find_one(conditions)

    def find(self, conditions: dict = None):
        """
        Filters documents from database collection. The given dictionary param
        represents the filter json. Returns a list of dicts, where each of them
        is a found document.
        TODO: retrieve only logical alive documents (maybe a 'alive_only=True' param?)
        """
        if conditions is None:
            conditions = {}
        if self.owner_post_graduation_id is not None:
            conditions['ownerProgram'] = self.owner_post_graduation_id
	#Ex: return DB['gradesOfSubjects'].find(5a15ca97d818ecf5068593c9) <- Sendo esse número o id do programa de pós-graduação
        return DB[self.collection].find(conditions)

    def count(self, conditions: dict = None):
        """
        Find the number of documents inside collection
        """
        if conditions is None:
            conditions = {}
        if self.owner_post_graduation_id is not None:
            conditions['ownerProgram'] = self.owner_post_graduation_id
        return DB[self.collection].count(conditions)


    def insert_one(self, conditions: dict, document: dict):
        """
        Insert a document as dict into the collection and returns its new id if it worked.
        TODO: insert an alive document
        """
        if conditions is None:
            conditions = {}
        if self.owner_post_graduation_id is not None:
            conditions['ownerProgram'] = self.owner_post_graduation_id
        return DB[self.collection].insert(document)

    def insert_many(self, document: list):
        """
        TODO: Insert a list of documents into the collection and returns a list of their
        new ids if it worked.
        """
        raise NotImplementedError("Tried to call an update function without implementing it.")

    def find_one_and_update(self, conditions: dict, update: dict):
        """
        Finds a single document and updates it, returning the original.
        """
        if conditions is None:
            conditions = {}
        if self.owner_post_graduation_id is not None:
            conditions['ownerProgram'] = self.owner_post_graduation_id
        return DB[self.collection].find_one_and_update(conditions, update)

    def delete(self, document: dict):
        """
        TODO: Logical delete. So the document still recorded at persistence,
        but can no longer be retrieved using regular CRUD methods.
        """
        raise NotImplementedError("Need to implement update function for logical deleting it.")

class StudentSigaaDAO(AbstractDAO):

    def __init__(self, id_course: int):
        self.ENDPOINT = api_sistemas.API_URL_ROOT
        self.ENDPOINT += 'discente/v0.1/discentes?situacao-discente=1&id-curso='
        self.ENDPOINT += str(id_course)
        self.ENDPOINT += '&limit=100'

    def find_all(self):
        raise NotImplementedError("Not implemented method inherited from an abstract class.")

    def find_one(self, conditions):
        raise NotImplementedError("Not implemented method inherited from an abstract class.")

    def find(self, conditions: dict = {}):
        bearer_token = api_sistemas.retrieve_token()
        return self._parse(api_sistemas.get_public_data(self.ENDPOINT, bearer_token))

    def _parse(self, students_from_sigaa):
        students = []
        for student_from_sigaa in students_from_sigaa:
            students.append({
                'name': student_from_sigaa['nome-discente'].title(),
                'class': str(student_from_sigaa['matricula']),
            })
        return students

    def insert_one(self, document: dict):
        raise NotImplementedError("Data from SIGAA are read-only.")

    def insert_many(self, document: list):
        raise NotImplementedError("Data from SIGAA are read-only.")

    def update(self, document: dict):
        raise NotImplementedError("Data from SIGAA are read-only.")

    def delete(self, document: dict):
        raise NotImplementedError("Data from SIGAA are read-only.")

class ClassesSigaaDAO(AbstractDAO):

    def __init__(self, id_unit: int, year: int, period: int):
        self.ENDPOINT = api_sistemas.API_URL_ROOT
        self.ENDPOINT += 'turma/v0.1/turmas?id-unidade={id_unit}&ano={year}&periodo={period}&limit=100&id-situacao-turma=1%2C2%2C3'
        self.ENDPOINT = self.ENDPOINT.format(id_unit=id_unit, year=year, period=period)
        self._classes = []
        self._professors = []
        self._bearer_token = None

    def find_all(self):
        raise NotImplementedError("Not implemented method inherited from an abstract class.")

    def find_one(self, conditions):
        raise NotImplementedError("Not implemented method inherited from an abstract class.")

    def find(self, conditions: dict = {}):
        self._bearer_token = api_sistemas.retrieve_token()
        return self._parse(api_sistemas.get_public_data(self.ENDPOINT, self._bearer_token))

    def _parse(self, classes_from_sigaa):
        classes_id = []
        for class_from_sigaa in classes_from_sigaa:
            self._classes.append({
                'component_name': class_from_sigaa['nome-componente'].title(),
                'component_code': class_from_sigaa['codigo-componente'],
                'hours': class_from_sigaa['descricao-horario'],
                'id_class': class_from_sigaa['id-turma'],
            })
            classes_id.append(class_from_sigaa['id-turma'])

        threads = []
        for i in range(len(classes_id)):
            process = Thread(target=self.get_professor, args=[classes_id[i]])
            threads.append(process)
            process.start()
        for process in threads:
            process.join()
        return self._classes

    def get_professor(self, id_class: str):
        url = api_sistemas.API_URL_ROOT
        url += 'turma/v0.1/participantes?id-turma={id_class}&id-tipo-participante=1'
        url = url.format(id_class=id_class)
        result = api_sistemas.get_public_data(url, self._bearer_token)
        for grade in range(len(self._classes)):
            if self._classes[grade]['id_class'] == id_class:
                for professor in result:
                    self._classes[grade]['professor_name'] = professor['nome'].title()

    def insert_one(self, document: dict):
        raise NotImplementedError("Data from SIGAA are read-only.")

    def insert_many(self, document: list):
        raise NotImplementedError("Data from SIGAA are read-only.")

    def update(self, document: dict):
        raise NotImplementedError("Data from SIGAA are read-only.")

    def delete(self, document: dict):
        raise NotImplementedError("Data from SIGAA are read-only.")

class ProjectSigaaDAO(AbstractDAO):

    def __init__(self, program_sigaa_code: int):
        self.ENDPOINT = api_sistemas.API_URL_ROOT
	#Descobrir qual o "formato" dessa consulta
        self.ENDPOINT += 'stricto-sensu-services/services/consulta/projeto/'
        self.ENDPOINT += str(program_sigaa_code)
        self._bearer_token = None

    def find_all(self):
        raise NotImplementedError("Not implemented method inherited from an abstract class.")

    def find_one(self, conditions: dict):
        raise NotImplementedError("Not implemented method inherited from an abstract class.")

    def find(self, conditions: dict = {}):
        self._bearer_token = api_sistemas.retrieve_token()
        return self._parse(api_sistemas.get_public_data(self.ENDPOINT, self._bearer_token))

    def _parse(self, projects_from_sigaa):
        projects = []

        for project_from_sigaa in projects_from_sigaa:
            
            if not project_from_sigaa['situacaoProjeto'] == 'FINALIZADO':
                members = None #?
                members = []
                coordinators_names = []
                blocked = False

                for member in project_from_sigaa['membrosProjeto']:
                    # a certain professor is blocked... oh, my! :o
		    #wtf teste?
                    if member['nome'].title() == 'Luciano Menezes Bezerra Sampaio':
                        blocked = True

                    # convert from 'sigaa member' to a 'minerva member'
                    if 'COORDENADOR' in member['funcao'].upper():
                        coordinators_names.append(member['nome'].title())
                    else:
                        members.append({
                            'name': member['nome'].title(),
                            'general_role': member['caterogia'].capitalize(),
                            'project_role': member['funcao'].capitalize()
                        })

                    # avoid a certain professor when he's alone coordinating the project
                    if len(coordinators_names) == 1 and coordinators_names[0] == 'Washington Jose De Sousa':
                        blocked = True

                # after transfusing all members, are we really going finish the assembling? 
                if not blocked:
                    title, _, subtitle = project_from_sigaa['titulo'].rpartition(':')

                    if not title:
                        title = subtitle
                        subtitle = None

                    else:
                        subtitle = subtitle.strip()
                        subtitle = subtitle[0].upper() + subtitle[1:]

                        projects.append({
                            'title': title,
                            'subtitle': subtitle,
                            'year': project_from_sigaa['codAno'],
                            'dt_init': project_from_sigaa['dataInicio'],
                            'dt_end': project_from_sigaa['dataFim'],
                            'situation': project_from_sigaa['situacaoProjeto'].capitalize(),
                            'description': project_from_sigaa['descricao'],
                            'email': project_from_sigaa['email'],
                            'members': list(members),
                            'coordinators_names': list(coordinators_names)
                        })
        return projects

    def insert_one(self, document: dict):
        raise NotImplementedError("Data from SIGAA are read-only.")

    def insert_many(self, document: list):
        raise NotImplementedError("Data from SIGAA are read-only.")

    def update(self, document: dict):
        raise NotImplementedError("Data from SIGAA are read-only.")

    def delete(self, document: dict):
        raise NotImplementedError("Data from SIGAA are read-only.")
