
use minerva;

print("Inserindo pós graduações...");

db.postGraduations.insertMany([
    {
        'name': 'Gestão Pública',
        'initials': 'PPGP',
        'attendance': {
            'building': 'Administração do CCSA',
            'floor': 'Térreo',
            'room': 'A10',
            'opening': 'Segunda à Sexta-Feira (08:00 às 11:30 e 13:30 às 17:00)'
        },
        'email': 'ppgp.ufrn@gmail.com',
        'phones': [
            {
                'type': 'Fixo',
                'number': '+55 84 3342-2288 (Ramal 189)'
            },
            {
                'type': 'Claro',
                'number': '+55 84 9 9474-6765'
            }
        ],
        'isSignedIn': true,
        'oldURL': 'https://sigaa.ufrn.br/sigaa/public/programa/portal.jsf?lc=pt_BR&id=5679'
    },
    {
        'name': 'Administração',
        'initials': 'PPGA',
        'isSignedIn': false,
        'oldURL': 'https://sigaa.ufrn.br/sigaa/public/programa/portal.jsf?lc=pt_BR&id=74'
    },
    {
        'name': 'Ciências Contábeis',
        'initials': 'PPGCC',
        'isSignedIn': false,
        'oldURL': 'https://sigaa.ufrn.br/sigaa/public/programa/portal.jsf?lc=pt_BR&id=9066'
    },
    {
        'name': 'Direito',
        'initials': 'PPGD',
        'isSignedIn': false,
        'oldURL': 'https://sigaa.ufrn.br/sigaa/public/programa/portal.jsf?lc=pt_BR&id=404'
    },
    {
        'name': 'Economia',
        'initials': 'PPGECO',
        'isSignedIn': false,
        'oldURL': 'https://sigaa.ufrn.br/sigaa/public/programa/portal.jsf?lc=pt_BR&id=434'
    },
    {
        'name': 'Gestão da Informação e do Conhecimento',
        'initials': 'PPGIC',
        'isSignedIn': false,
        'oldURL': 'https://sigaa.ufrn.br/sigaa/public/programa/portal.jsf?lc=pt_BR&id=9196'
    },
    {
        'name': 'Serviço Social',
        'initials': 'PPGSS',
        'isSignedIn': false,
        'oldURL': 'https://sigaa.ufrn.br/sigaa/public/programa/portal.jsf?lc=pt_BR&id=376'
    },
    {
        'name': 'Turismo',
        'initials': 'PPGTUR',
        'isSignedIn': false,
        'oldURL': 'https://sigaa.ufrn.br/sigaa/public/programa/portal.jsf?lc=pt_BR&id=4295'
    }
]);

PPGP_ID = db.postGraduations.findOne({'initials': 'PPGP'})._id;

print("Inserindo linhas de pesquisa...");

db.researchLines.insertMany([
    {
        'ownerProgram': PPGP_ID,
        'name': 'Gestão e Políticas Públicas',
        'description': 'Tem como foco de estudo os processos de modernização da administração pública, nas esferas federal, estadual e municipal. A estratégia de análise é a partir da abordagem da inovação na gestão pública, tanto nos aspectos gerenciais quanto políticos, e, dessa forma, busca investigar temas como a contratualização e gestão por resultados, flexibilização, intersetorialidade, transparência, accountability, participação social, territorialidade, relações intergovernamentais, bem como temáticas específicas, como gestão de pessoas, processos, finanças etc. Em relação às políticas públicas, esta linha visa a atuação do Estado por meio de seus aparatos institucionais, dos seus mecanismos regulatórios e dos processos de participação social em vários âmbito geográficos; bem como envolve a análise das etapas de formulação, implementação e avaliação de políticas públicas.'
    }
]);

print("Inserindo grades de disciplinas...");

db.gradesOfSubjects.insertMany([
    {
        'ownerProgram': PPGP_ID,
        'title': 'Obrigatórias',
        'minCredits': 10,
        'minSubjectsQtt': 5,
        'subjects': [
            {
                'name': 'Teoria Geral da Administração Pública',
                'workloadInHours': 30,
                'credits': 2
            },
            {
                'name': 'Instituições Políticas Brasileiras',
                'workloadInHours': 30,
                'credits': 2
            },
            {
                'name': 'Ciclo das Políticas Públicas',
                'workloadInHours': 30,
                'credits': 2
            },
            {
                'name': 'Metodologia da Pesquisa',
                'workloadInHours': 30,
                'credits': 2
            },
            {
                'name': 'Seminário de Dissertação/Projeto de Intervenção',
                'workloadInHours': 30,
                'credits': 2
            }
        ]
    },
    {
        'ownerProgram': PPGP_ID,
        'title': 'Eletivas',
        'minCredits': 14,
        'minSubjectsQtt': 7,
        'subjects': [
            {
                'name': 'Orçamento e Finanças Públicas',
                'workloadInHours': 30,
                'credits': 2
            },
            {
                'name': 'Inovação na Gestão Pública',
                'workloadInHours': 30,
                'credits': 2
            },
            {
                'name': 'Instituições e Regulação',
                'workloadInHours': 30,
                'credits': 2
            },
            {
                'name': 'Contratualização e Gestão por Resultados',
                'workloadInHours': 30,
                'credits': 2
            },
            {
                'name': 'Responsabilização, Transparência e Controle Social',
                'workloadInHours': 30,
                'credits': 2
            },
            {
                'name': 'Estado e Políticas Públicas Comparadas',
                'workloadInHours': 30,
                'credits': 2
            },
            {
                'name': 'Federalismo e Políticas Públicas',
                'workloadInHours': 30,
                'credits': 2
            },
            {
                'name': 'Avaliação de Políticas Públicas',
                'workloadInHours': 30,
                'credits': 2
            },
            {
                'name': 'Políticas Sociais no Brasil',
                'workloadInHours': 30,
                'credits': 2
            },
            {
                'name': 'Atores, Processos e Instrumentos na Ação Pública',
                'workloadInHours': 30,
                'credits': 2
            },
            {
                'name': 'Planejamento na Gestão Pública',
                'workloadInHours': 30,
                'credits': 2
            },
            {
                'name': 'Gestão de Pessoas no Setor Público',
                'workloadInHours': 30,
                'credits': 2
            },
            {
                'name': 'Tópicos Especiais em Gestão Pública I',
                'workloadInHours': 30,
                'credits': 2
            },
            {
                'name': 'Tópicos Especiais em Gestão Pública II',
                'workloadInHours': 15,
                'credits': 1
            },
            {
                'name': 'Tópicos Especiais em Gestão Pública III',
                'workloadInHours': 30,
                'credits': 2
            },
            {
                'name': 'Tópicos Especiais em Gestão Pública IV',
                'workloadInHours': 15,
                'credits': 1
            }
        ]
    }
]);

print("Inserindo agendas semanais...");

db.weeklySchedules.insertMany([
    {
        'ownerProgram': PPGP_ID,
        'title': 'Turma 2017',
        'week': [
            {
                'day': 'Quinta-feira',
                'classes': [
                    {
                        'subject': 'Gestão de Pessoas no Setor Público',
                        'hour': '09:00',
                        'isMandatory': false
                    },
                ]
            },
            {
                'day': 'Sexta-feira',
                'classes': [
                    {
                        'subject': 'Teoria Geral da Administração Pública',
                        'hour': '14:00',
                        'isMandatory': true
                    }
                ]
            }
        ]
    }
]);

print("Inserindo informações sobre as integrações...");

db.integrationsInfos.insertMany([
    {
        'ownerProgram': PPGP_ID,
        'institutionsWithCovenant': [
            {
                'name': 'Ministério da Transparência, Fiscalização e Controladoria Geral da União – Unidade Regional do Rio Grande do Norte',
                'initials': 'CGURN'
            },
            {
                'name': 'Universidade Federal do Rio Grande do Norte',
                'initials': 'UFRN'
            },
            {
                'name': 'Instituto Federal de Educação, Ciência e Tecnologia de Sergipe',
                'initials': 'IFS'
            },
            {
                'name': 'Assembleia Legislativa do Estado Rio Grande do Norte',
                'initials': 'ALRN'
            }
        ],
        'participationsInEvents': [
            {
                'title': 'Laboratoire de Recherche en Management (LAREQUOI)',
                'description': 'A professora Dinah dos Santos Tinoco participou de intercâmbio no LAREQUOI da Université de Versailles St. Quentin em Yvelines, França, no período de abril a junho de 2013. No período, além de ter participado de reuniões com professores do Laboratório, foi membro da comissão de avaliação de três bancas de defesa de Doutorado, tendo previamente elaborado Relatórios Técnicos de avaliação das teses.',
                'year': 2013,
                'international': 'Yvelines, França'
            },
            {
                'title': 'Center for Latin American Studies da Faculty of Economics and Public Administration da University of Economics',
                'description': 'O professor Hironobu Sano participou, em abril de 2013, de missão para o Center for Latin American Studies da Faculty of Economics and Public Administration da University of Economics, a principal instituição de ensino superior da República Tcheca.',
                'year': 2013,
                'international': 'Praga, República Tcheca'
            },
            {
                'title': 'Grupo de Investigación en Gobierno, Administración y Políticas Públicas (GIGAPP)',
                'description': 'O professor Thiago Dias participou como congressista do GIGAPP, realizado de 27 de setembro a 02 de outubro de 2014 em Madrid, Espanha, organizado pelo Instituto Nacional de Administración Pública, onde apresentou o artigo Gestão Social e Desenvolvimento Territorial: uma olhar a partir processo de governança dos colegiados territoriais brasileiro no Grupo de Trabalho Planejamento, Gestão Pública e Participação Social.',
                'year': 2014,
                'international': 'Madrid, Espanha'
            }
        ]
    }
]);

print("Inserindo coordenação...");

db.boardsOfStaffs.insertMany([
    {
        'ownerProgram': PPGP_ID,
        'coordination': [
            {
                'name': 'Thiago Ferreira Dias',
                'rank': 'Coordenador',
                'abstract': 'Possui Doutorado em Administração pela Universidade Federal do Rio Grande do Norte (2011), Mestrado em Administração e Desenvolvimento Rural pela Universidade Federal Rural de Pernambuco (2007) e graduação em Administração pela Universidade Federal de Pernambuco (2005). De 2010 a 2013 foi professor da Universidade Federal Rural do Semi-Árido (UFERSA). De 2012 a 2013 foi coordenador da Incubadora de Iniciativas Sociais e Solidárias do Oeste Potiguar (INCUBAOESTE). Desde janeiro de 2014 é professor adjunto da Universidade Federal do Rio Grande do Norte.',
                'photo': 'http://servicosweb.cnpq.br/wspessoa/servletrecuperafoto?tipo=1&id=K4731730Y4'
            },
            {
                'name': 'Antônio Alves Filho',
                'rank': 'Vice-Coordenador',
                'abstract': 'Possui graduação em Psicologia pela Universidade Federal do Rio Grande do Norte (1993) e mestrado em Administração (1999) e doutorado em Psicologia (2012) também pela UFRN. De 2009 a 2013 foi professor adjunto da Universidade Federal de Alagoas (UFAL), no curso de Psicologia. A partir de dezembro de 2013, passou a ser professor adjunto do Departamento de Ciências Administrativas da Universidade Federal do Rio Grande do Norte. Na Psicologia atua na área da Psicologia do Trabalho e das Organizações, com ênfase em Fatores Humanos no Trabalho. Na Administração atua na área de Gestão de Pessoas. Desde 2014 é docente permanente do Programa de Pós-Graduação em Gestão Pública, UFRN.',
                'photo': 'http://servicosweb.cnpq.br/wspessoa/servletrecuperafoto?tipo=1&id=K4701984E0'
            }
        ],
        'secretariat': [
            {
                'name': 'Penélope Medeiros Filgueira Burlamaqui',
                'function': {
                    'rank': 'Secretária',
                    'description': 'Chefia a secretaria, responsável por organizar e movimentar a burocracia do setor.'
                },
                'photo': null
            },
            {
                'name': 'Marcell Guilherme Costa da Silva',
                'function': {
                    'rank': 'Bolsista',
                    'description': 'Desenvolve o sistema web, automatiza atividades da secretaria e provê um mínimo suporte técnico aos computadores.'
                },
                'photo': null
            },
            {
                'name': 'Davila Regina Silva Rodrigues',
                'function': {
                    'rank': 'Bolsista',
                    'description': 'Provê um suporte maior à administração do setor, juntamente com a secretária.'
                },
                'photo': null
            }
        ]
    }
]);

print("Inserindo quadro de professores...");

db.boardsOfProfessors.insertMany([
    {
        'ownerProgram': PPGP_ID,
        'professors': [
            {
                'name': 'Aline Virginia Medeiros Nelson',
                'rank': 'Professor',
                'lattes': 'http://lattes.cnpq.br/0268682852336814',
                'email': 'minerva.teste@ufrn.edu.br'
            },
            {
                'name': 'Antonio Alves Filho',
                'rank': 'Professor',
                'lattes': 'http://lattes.cnpq.br/4852627579601532',
                'email': 'minerva.teste@ufrn.edu.br'
            },
            {
                'name': 'Dinah dos Santos Tinoco',
                'rank': 'Professor',
                'lattes': 'http://lattes.cnpq.br/8281386555414820',
                'email': 'minerva.teste@ufrn.edu.br'
            },
            {
                'name': 'Djalma Freire Borges',
                'rank': 'Professor',
                'lattes': null,
                'email': 'minerva.teste@ufrn.edu.br'
            },
            {
                'name': 'Fabio Resende de Araujo',
                'rank': 'Professor',
                'lattes': 'http://lattes.cnpq.br/2159396359014027',
                'email': 'minerva.teste@ufrn.edu.br'
            },
            {
                'name': 'Hironobu Sano',
                'rank': 'Professor',
                'lattes': 'http://buscatextual.cnpq.br/buscatextual/visualizacv.jsp?id=K4707946H6',
                'email': 'minerva.teste@ufrn.edu.br'
            },
            {
                'name': 'Ítalo Fittipaldi',
                'rank': 'Colaborador',
                'lattes': null,
                'email': 'minerva.teste@ufrn.edu.br'
            },
            {
                'name': 'Jomaria Mata de Lima Alloufa',
                'rank': 'Professor',
                'lattes': 'http://lattes.cnpq.br/9209334172096854',
                'email': 'minerva.teste@ufrn.edu.br'
            },
            {
                'name': 'Kaio Cesar Fernandes',
                'rank': 'Colaborador',
                'lattes': null,
                'email': 'minerva.teste@ufrn.edu.br'
            },
            {
                'name': 'Maria Arlete Duarte de Araujo',
                'rank': 'Professor',
                'lattes': 'http://lattes.cnpq.br/8538092783362714',
                'email': 'minerva.teste@ufrn.edu.br'
            },
            {
                'name': 'Maria Teresa Pires Costa',
                'rank': 'Professor',
                'lattes': 'http://lattes.cnpq.br/2406703224108111',
                'email': 'minerva.teste@ufrn.edu.br'
            },
            {
                'name': 'Pamela de Medeiros Brandao',
                'rank': 'Professor',
                'lattes': 'http://lattes.cnpq.br/9451364933481439',
                'email': 'minerva.teste@ufrn.edu.br'
            },
            {
                'name': 'Richard Medeiros de Araújo',
                'rank': 'Colaborador',
                'lattes': null,
                'email': 'minerva.teste@ufrn.edu.br'
            },
            {
                'name': 'Thiago Ferreira Dias',
                'rank': 'Professor',
                'lattes': 'http://lattes.cnpq.br/9579256535097635',
                'email': 'minerva.teste@ufrn.edu.br'
            }
        ]
    }
]);

print("Inserindo trabalhos de conclusão...");

db.finalReports.insertMany([
    {
        'ownerProgram': PPGP_ID,
        'scheduledReports': [
            {
                'time': new Date(2017, 04, 03, 09, 00, 00, 00),
                'title': 'Programa Reitoria Itinerante do IFPB: uma análise sob o enfoque da gestão participativa',
                'author': 'Adino Saraiva Bandeira',
                'location': 'Sala D4 do Setor V'
            }
        ]
    }
]);
