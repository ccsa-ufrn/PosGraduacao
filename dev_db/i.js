
use minerva;

db.post_graduations.insertMany([
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
