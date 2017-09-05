
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
        'sigaaCode': '1672',
        'isSignedIn': true,
        'oldURL': 'https://sigaa.ufrn.br/sigaa/public/programa/portal.jsf?lc=pt_BR&id=5679'
    },
    {
        'name': 'Administração',
        'initials': 'PPGA',
        'sigaaCode': undefined,
        'isSignedIn': false,
        'oldURL': 'https://sigaa.ufrn.br/sigaa/public/programa/portal.jsf?lc=pt_BR&id=74'
    },
    {
        'name': 'Ciências Contábeis',
        'initials': 'PPGCC',
        'sigaaCode': undefined,
        'isSignedIn': false,
        'oldURL': 'https://sigaa.ufrn.br/sigaa/public/programa/portal.jsf?lc=pt_BR&id=9066'
    },
    {
        'name': 'Direito',
        'initials': 'PPGD',
        'sigaaCode': undefined,
        'isSignedIn': false,
        'oldURL': 'https://sigaa.ufrn.br/sigaa/public/programa/portal.jsf?lc=pt_BR&id=404'
    },
    {
        'name': 'Economia',
        'initials': 'PPGECO',
        'sigaaCode': undefined,
        'isSignedIn': false,
        'oldURL': 'https://sigaa.ufrn.br/sigaa/public/programa/portal.jsf?lc=pt_BR&id=434'
    },
    {
        'name': 'Gestão da Informação e do Conhecimento',
        'initials': 'PPGIC',
        'sigaaCode': undefined,
        'isSignedIn': false,
        'oldURL': 'https://sigaa.ufrn.br/sigaa/public/programa/portal.jsf?lc=pt_BR&id=9196'
    },
    {
        'name': 'Serviço Social',
        'initials': 'PPGSS',
        'sigaaCode': undefined,
        'isSignedIn': false,
        'oldURL': 'https://sigaa.ufrn.br/sigaa/public/programa/portal.jsf?lc=pt_BR&id=376'
    },
    {
        'name': 'Turismo',
        'initials': 'PPGTUR',
        'sigaaCode': undefined,
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
                'description': 'Compreensão dos campos da política, das políticas públicas e da administração pública; O Contexto decisório da Administração Pública; O Contexto organizacional da Administração Pública; O Contexto normativo da Administração Pública; Teoria das Organizações e Administração Pública; Novos paradigmas da gestão pública.',
                'workloadInHours': 30,
                'credits': 2
            },
            {
                'name': 'Instituições Políticas Brasileiras',
                'description': 'A evolução das instituições democráticas no Brasil  as relações entre o Estado e a sociedade civil; A Evolução da relação entre os Poderes Executivo e Legislativo no âmbito dos partidos e do sistema partidário. As Medidas Provisórias e a Delegação na Democracia Brasileira. As Gramáticas Políticas e o Processo de Nation Buildin.',
                'workloadInHours': 30,
                'credits': 2
            },
            {
                'name': 'Ciclo de Políticas Públicas',
                'description': 'Introdução à política pública: origens e conceitos. Modelos e processos de análise. Análise cíclica de políticas públicas, fundamentos e bases teórico-metodológicas, com destaque para as suas fases: problema, construção da agenda, formulação, implementação e avaliação de políticas públicas. Principais contribuições e críticas ao modelo cíclico. Análise sequencial de políticas públicas brasileiras.',
                'workloadInHours': 30,
                'credits': 2
            },
            {
                'name': 'Metodologia da Pesquisa',
                'description': 'Natureza do conhecimento; O que é conhecer e seus problemas; O conhecimento, seus níveis e características; O Processo de construção da ciência; Objetivo e papéis da ciência, teoria e fato; Relacionamento entre ciência, teoria, fato, pesquisa e método; O método científico (os métodos e técnicas de pesquisa); A pesquisa e tipos de pesquisa; Passos formais de Estudos Científicos; Etapas para elaboração de pesquisa bibliográfica; Etapas para elaboração de projeto de pesquisa de campo; Relatórios científicos; Conceito; Tipos: trabalho de síntese, resenha, trabalho de divulgação, informes científicos; Relatórios e monografias  ensaios, dissertação e tese; Estrutura (introdução, desenvolvimento e conclusão); Redação de trabalhos científicos.',
                'workloadInHours': 30,
                'credits': 2
            },
            {
                'name': 'Seminário de Dissertação/Projeto de Intervenção',
                'description': 'O projeto de pesquisa; Os elementos constitutivos do Projeto de Pesquisa  Introdução, objeto, problema, objetivos, procedimentos metodológicos, referências bibliográficas; Projeto de dissertação; Projeto de Intervenção  etapas e elementos; Oficinas de apresentação do Projeto de dissertação ou do Projeto de Intervenção.',
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
                'description': 'O Papel do Estado em Economia Capitalista. Orçamento Público. Orçamento na Constituição Federal. Gasto Público. Receita Pública. Déficit Público. Dívida Pública. Medição do Resultado do Setor Público. Federalismo Fiscal. Previdência Social.',
                'workloadInHours': 30,
                'credits': 2
            },
            {
                'name': 'Inovação na Gestão Pública',
                'description': 'Inovação, Inovação no setor público; Difusão da Inovação; Barreiras à Inovação no Setor Público; Governança Eletrônica; Novos Mecanismos de Participação e Controle Social; Empreendedorismo no Setor Público.',
                'workloadInHours': 30,
                'credits': 2
            },
            {
                'name': 'Instituições e Regulação',
                'description': 'A Globalização a Crise do Capitalismo e a Redefinição do padrão de intervenção do Estado no mundo; Os anos 90 e as reformas de mercado na América Latina; A Reforma patrimonial e as privatizações no Brasil; As Agências Reguladoras; Os diversos setores de regulação e suas agências federais e estaduais: energia, telefonia, recursos hídricos, saúde e os contratos de gestão hospitalares.',
                'workloadInHours': 30,
                'credits': 2
            },
            {
                'name': 'Contratualização e Gestão por Resultados',
                'description': 'A Nova Gestão Pública. Gestão para resultados no setor público: estrutura, requisitos e implementação. Contratualização de resultados no setor público. Contratos de gestão. Cultura de resultados. Avaliação da gestão pública. Indicadores e avaliação de desempenho. Responsabilização por controle de resultados. Limites do gerencialismo.',
                'workloadInHours': 30,
                'credits': 2
            },
            {
                'name': 'Responsabilização, Transparência e Controle Social',
                'description': 'Administração pública voltada para o cidadão; Responsabilização na administração pública; Responsabilização por competição administrada; Responsabilização pelo controle social; Responsabilização pelo controle de resultados; Transparência na gestão pública; Transparência e interface com o cidadão; Mecanismos de Participação cidadã; Cidadania e políticas públicas; Formas de controle; Controle social e burocracia; Limites e possibilidades do controle social.',
                'workloadInHours': 30,
                'credits': 2
            },
            {
                'name': 'Estado e Políticas Públicas Comparadas',
                'description': 'Teorias e modelos analíticos de políticas públicas; Coordenação, autonomia e controle de políticas públicas nos diferentes níveis de governo; Características das diversas políticas públicas sociais e econômicas; Implementação em diferentes contextos institucionais, sociais e econômicos; O papel da sociedade civil; análise comparada internacional de diferentes trajetórias de policies.',
                'workloadInHours': 30,
                'credits': 2
            },
            {
                'name': 'Federalismo e Políticas Públicas',
                'description': 'Federalismo, políticas públicas e problemas de coordenação vertical e horizontal. Intersetorialidade na formulação e implementação de políticas públicas. Mecanismos institucionais de gestão. Estudos de casos setoriais.',
                'workloadInHours': 30,
                'credits': 2
            },
            {
                'name': 'Avaliação de Políticas Públicas',
                'description': 'Principais aportes teóricos e metodológicos da avaliação de políticas públicas: modelos, conceitos, processos, atores e categorias analíticas referentes ao monitoramento das políticas públicas e, principalmente, avaliação de balanço e conclusiva de políticas públicas. Tipos de avaliação: tradicional e pluralista: fundamentos, diferenças e especificidades de cada abordagem; Path Dependance e suas aplicações a situações concretas; tendências contemporâneas de avaliação baseadas em participação e negociação entre instituições e atores envolvidos.',
                'workloadInHours': 30,
                'credits': 2
            },
            {
                'name': 'Políticas Sociais no Brasil',
                'description': 'Marcos Constitucionais; O conceito de cidadania social na CF/88; o papel dos municípios na CF/88; definição de competências nas décadas de 1990 e 2000: normatização federal e execução municipal; as política de saúde e educação e sua coordenação federativa; A municipalização da educação fundamental; o SUS e a atenção básica à saúde pelos municípios; política de assistência social.',
                'workloadInHours': 30,
                'credits': 2
            },
            {
                'name': 'Atores, Processos e Instrumentos na Ação Pública',
                'description': 'Conceitos, metodologias e categorias analíticas referentes à análise da ação pública que contempla atores, representações, instituições, processos e resultados dessa ação (LASCOUMES e LE GALÈS). Mudanças nas relações Estado x Sociedade e processos de negociação e de coordenação inovadores. O Estado e demais atores que integram a ação pública. Aportes teóricos para a compreensão da ação pública como a análise de redes, a análise cognitiva e a sociologia da ação coletiva.',
                'workloadInHours': 30,
                'credits': 2
            },
            {
                'name': 'Planejamento na Gestão Pública',
                'description': ' Natureza e Evolução do Planejamento na Gestão Pública; Abordagens conceituais sobre Planejamento na Gestão Pública; Origem, Trajetória, Crise e Ressurgimento do Planejamento na Gestão Pública Brasileira; Metodologias de Planejamento; Usos da informação para o monitoramento e avaliação de planos.',
                'workloadInHours': 30,
                'credits': 2
            },
            {
                'name': 'Gestão de Pessoas no Setor Público',
                'description': 'As pessoas e os sistemas de gestão nas organizações; Características da gestão de pessoas no Setor Público; Gestão de competências e gestão de conhecimento; Formas contratuais e regimes de trabalho; Carreiras: estruturação dos cargos e funções no Setor Público; Treinamento, desenvolvimento e educação nas organizações públicas; Avaliação de Desempenho Individual; Remuneração e gestão por competências; Motivação, clima e qualidade de vida no trabalho; Metodologia para avaliação da gestão dos recursos humanos no setor público; Tendências e desafios à gestão de pessoas no Setor Público.',
                'workloadInHours': 30,
                'credits': 2
            },
            {
                'name': 'Tópicos Especiais em Gestão Pública I',
                'description': 'O tema abordado é variável.',
                'workloadInHours': 30,
                'credits': 2
            },
            {
                'name': 'Tópicos Especiais em Gestão Pública II',
                'description': 'O tema abordado é variável.',
                'workloadInHours': 15,
                'credits': 1
            },
            {
                'name': 'Tópicos Especiais em Gestão Pública III',
                'description': 'O tema abordado é variável.',
                'workloadInHours': 30,
                'credits': 2
            },
            {
                'name': 'Tópicos Especiais em Gestão Pública IV',
                'description': 'O tema abordado é variável.',
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
                'day': 'Quinta',
                'classes': [
                    {
                        'subject': 'Responsabilização, Transparência e Controle Social',
                        'hour': '08:00',
                        'isMandatory': false
                    },
                    {
                        'subject': 'Gestão de Pessoas no Setor Público',
                        'hour': '09:00',
                        'isMandatory': false
                    },
                    {
                        'subject': 'Tópicos Especiais em Gestão Pública III - Análise de Redes Sociais',
                        'hour': '14:00',
                        'isMandatory': false
                    },
                    {
                        'subject': 'Teoria Geral da Administração Pública',
                        'hour': '19:00',
                        'isMandatory': true
                    }
                ]
            },
            {
                'day': 'Sexta',
                'classes': [
                    {
                        'subject': 'Inovação na Gestão Pública',
                        'hour': '08:30',
                        'isMandatory': false
                    },
                    {
                        'subject': 'Instituições Políticas Brasileiras',
                        'hour': '14:00',
                        'isMandatory': true
                    }
                ]
            }
        ]
    },
    {
        'ownerProgram': PPGP_ID,
        'title': 'Turma 2016',
        'week': [
            {
                'day': 'Quinta',
                'classes': [
                    {
                        'subject': 'Gestão de Pessoas no Setor Público',
                        'hour': '09:00',
                        'isMandatory': false
                    },
                    {
                        'subject': 'Responsabilização, Transparência e Controle Social',
                        'hour': '14:00',
                        'isMandatory': false
                    },
                    {
                        'subject': 'Tópicos Especiais em Gestão Pública III - Análise de Redes Sociais',
                        'hour': '14:00',
                        'isMandatory': false
                    }
                ]
            },
            {
                'day': 'Sexta',
                'classes': [
                    {
                        'subject': 'Inovação na Gestão Pública',
                        'hour': '08:30',
                        'isMandatory': false
                    },
                    {
                        'subject': 'Seminário de Dissertação/Projeto de Intervenção',
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
                'name': 'Instituto Nacional de Colonização e Reforma Agrária SR-19',
                'initials': 'INCRARN',
                'logoFile': 'logo-incrarn.jpg'
            },
            {
                'name': 'Universidade Federal do Rio Grande do Norte',
                'initials': 'UFRN',
                'logoFile': 'logo-ufrn.jpg'
            },
            {
                'name': 'Instituto Federal de Educação, Ciência e Tecnologia de Sergipe',
                'initials': 'IFS',
                'logoFile': 'logo-ifs.jpg'
            },
            {
                'name': 'Instituto Federal da Paraíba',
                'initials': 'IFPB',
                'logoFile': 'logo-ifpb.jpg'
            },
            {
                'name': 'Assembleia Legislativa do Estado Rio Grande do Norte',
                'initials': 'ALRN',
                'logoFile': 'logo-alrn.jpg'
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
                'email': 'aline_nelson@hotmail.com'
            },
            {
                'name': 'Antônio Alves Filho',
                'rank': 'Professor',
                'lattes': 'http://lattes.cnpq.br/4852627579601532',
                'email': 'antonioalvesfil@gmail.com'
            },
            {
                'name': 'Dinah dos Santos Tinoco',
                'rank': 'Professor',
                'lattes': 'http://lattes.cnpq.br/8281386555414820',
                'email': 'dinahtinoco@uol.com.br'
            },
            {
                'name': 'Djalma Freire Borges',
                'rank': 'Professor',
                'lattes': null,
                'email': 'djalma.freire.borges@gmail.com'
            },
            {
                'name': 'Hironobu Sano',
                'rank': 'Professor',
                'lattes': 'http://buscatextual.cnpq.br/buscatextual/visualizacv.jsp?id=K4707946H6',
                'email': 'hiro.sano@gmail.com'
            },
            {
                'name': 'Ítalo Fittipaldi',
                'rank': 'Colaborador',
                'lattes': null,
                'email': 'italofittipaldi@gmail.com'
            },
            {
                'name': 'Jomária Mata de Lima Alloufa',
                'rank': 'Professor',
                'lattes': 'http://lattes.cnpq.br/9209334172096854',
                'email': 'jalloufa@yahoo.com.br'
            },
            {
                'name': 'Káio César Fernandes',
                'rank': 'Colaborador',
                'lattes': null,
                'email': 'kaio@ufersa.edu.br'
            },
            {
                'name': 'Maria Arlete Duarte de Araujo',
                'rank': 'Professor',
                'lattes': 'http://lattes.cnpq.br/8538092783362714',
                'email': 'mariaarlete1956@gmail.com'
            },
            {
                'name': 'Maria Teresa Pires Costa',
                'rank': 'Professor',
                'lattes': 'http://lattes.cnpq.br/2406703224108111',
                'email': 'teresapires.psi@gmail.com'
            },
            {
                'name': 'Pamela de Medeiros Brandao',
                'rank': 'Professor',
                'lattes': 'http://lattes.cnpq.br/9451364933481439',
                'email': 'pamela_brandao@yahoo.com.br'
            },
            {
                'name': 'Richard Medeiros de Araújo',
                'rank': 'Colaborador',
                'lattes': null,
                'email': 'richardmaraujo@uol.com.br'
            },
            {
                'name': 'Thiago Ferreira Dias',
                'rank': 'Professor',
                'lattes': 'http://lattes.cnpq.br/9579256535097635',
                'email': 'tfdpe@yahoo.com.br'
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
                'time': new Date(2017, 06, 25, 14, 00, 00, 00),
                'title': 'Direcionamento Estratégico Da Assembleia Legislativa Do Rio Grande Do Norte',
                'author': 'Carlos Eduardo Artioli Russo',
                'location': 'Sala D4 do Setor V'
            }
        ]
    }
]);


print("Inserindo documentos oficiais...");

db.officialDocuments.insertMany([
    {
        'ownerProgram': PPGP_ID,
        'title': 'Regimento Interno',
        'cod': '12-2015',
        'file': 'regimento_0122015consepe.pdf',
        'insertedOn': new Date(2017, 04, 03, 09, 00, 00, 00),
        'insertedBy': 'Marcell Guilherme Costa da Silva'
    },
    {
        'ownerProgram': PPGP_ID,
        'title': 'Estrutura Curricular',
        'cod': '01-2014',
        'file': 'resolucao_ESTRUTURA-CURRICULAR.docx',
        'insertedOn': new Date(2017, 04, 03, 09, 00, 00, 00),
        'insertedBy': 'Marcell Guilherme Costa da Silva'
    },
    {
        'ownerProgram': PPGP_ID,
        'title': 'Matrícula',
        'cod': '02-2014',
        'file': 'resolucao_MATRICULA.docx',
        'insertedOn': new Date(2017, 04, 03, 09, 00, 00, 00),
        'insertedBy': 'Marcell Guilherme Costa da Silva'
    },
    {
        'ownerProgram': PPGP_ID,
        'title': 'Exame de Proficiência',
        'cod': '03-2014',
        'file': 'resolucao_EXAME-DE-PROFICIENCIA.docx',
        'insertedOn': new Date(2017, 04, 03, 09, 00, 00, 00),
        'insertedBy': 'Marcell Guilherme Costa da Silva'
    },
    {
        'ownerProgram': PPGP_ID,
        'title': 'Procedimentos de Defesa',
        'cod': '04-2014',
        'file': 'resolucao_PROCEDIMENTOS-DE-DEFESA.docx',
        'insertedOn': new Date(2017, 04, 03, 09, 00, 00, 00),
        'insertedBy': 'Marcell Guilherme Costa da Silva'
    },
    {
        'ownerProgram': PPGP_ID,
        'title': 'Exame de Qualificação',
        'cod': '05-2014',
        'file': 'resolucao_EXAME-DE-QUALIFICACAO.docx',
        'insertedOn': new Date(2017, 04, 03, 09, 00, 00, 00),
        'insertedBy': 'Marcell Guilherme Costa da Silva'
    },
    {
        'ownerProgram': PPGP_ID,
        'title': 'Credenciamento Docente',
        'cod': '06-2014',
        'file': 'resolucao_CREDENCIAMENTO-DOCENTE.docx',
        'insertedOn': new Date(2017, 04, 03, 09, 00, 00, 00),
        'insertedBy': 'Marcell Guilherme Costa da Silva'
    },
    {
        'ownerProgram': PPGP_ID,
        'title': 'Resolução de Calendário',
        'cod': '07-2014',
        'file': 'resolucao_RESOLUCAO-CALENDARIO.docx',
        'insertedOn': new Date(2017, 04, 03, 09, 00, 00, 00),
        'insertedBy': 'Marcell Guilherme Costa da Silva'
    },
    {
        'ownerProgram': PPGP_ID,
        'title': 'Áreas de Concentração e Linhas de Pesquisa',
        'cod': '08-2014',
        'file': 'resolucao_LINHAS-PESQUISA.docx',
        'insertedOn': new Date(2017, 04, 03, 09, 00, 00, 00),
        'insertedBy': 'Marcell Guilherme Costa da Silva'
    },
    {
        'ownerProgram': PPGP_ID,
        'title': 'Projeto de Intervenção',
        'cod': '09-2014',
        'file': 'resolucao_PROJETO-INTERVENCAO.docx',
        'insertedOn': new Date(2017, 04, 03, 09, 00, 00, 00),
        'insertedBy': 'Marcell Guilherme Costa da Silva'
    },
    {
        'ownerProgram': PPGP_ID,
        'title': 'Aluno Especial',
        'cod': '10-2014',
        'file': 'resolucao_ALUNO-ESPECIAL.docx',
        'insertedOn': new Date(2017, 04, 03, 09, 00, 00, 00),
        'insertedBy': 'Marcell Guilherme Costa da Silva'
    }
]);
