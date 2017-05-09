
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
                'number': '+55 84 3342-2288 (Ramal 182)'
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
        'name': 'Obrigatórias',
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
        'name': 'Eletivas',
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
        'name': '2017.1',
        'week': [
            {
                'day': 'Segunda',
                'classes': [
                    {
                        'subject': 'Teoria Geral da Administração Pública',
                        'hour': '14:00',
                        'isMandatory': true
                    },
                    {
                        'subject': 'Instituições Políticas Brasileiras',
                        'hour': '16:00',
                        'isMandatory': true
                    }
                ]
            },
            {
                'day': 'Quinta',
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
