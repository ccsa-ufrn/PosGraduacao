use posgrad;

PPGP_ID = db.postGraduations.findOne({'initials': 'PPGP'})._id;
PPGA_ID = db.postGraduations.findOne({'initials': 'PPGA'})._id;
PPGCC_ID = db.postGraduations.findOne({'initials': 'PPGCC'})._id;
PPGD_ID = db.postGraduations.findOne({'initials': 'PPGD'})._id;
PPGECO_ID = db.postGraduations.findOne({'initials': 'PPGECO'})._id;
PPGIC_ID = db.postGraduations.findOne({'initials': 'PPGIC'})._id;
PPGSS_ID = db.postGraduations.findOne({'initials': 'PPGSS'})._id;
PPGTUR_ID = db.postGraduations.findOne({'initials': 'PPGTUR'})._id;

print("Inserindo grades de disciplinas...");

db.calendar.insertMany([
    {
        'ownerProgram': PPGP_ID,
        'events': [
          {
            'title': 'Matrícula para o período 2017.2',
            'initialDate': '17/07/2017',
            'finalDate': '21/07/2017',
            'hour' : null,
            'link': null
          },
          {
            'title': 'Início do período letivo 2017.2.',
            'initialDate': '17/07/2017',
            'finalDate': null,
            'hour' : null,
            'link': 'https://duckduckgo.com'
          },
          {
            'title': 'Hackathon UFRN',
            'initialDate': '17/07/2017',
            'finalDate': '20/07/2017',
            'hour' : null,
            'link': 'duckduckgo.com'
          },
          {
            'title': 'Palestra sobre Direito Processual Civil',
            'initialDate': '17/07/2017',
            'finalDate': '17/07/2017',
            'hour' : '13:00 a 18:00',
            'link': null
          }
        ]
    },
    {
        'ownerProgram': PPGA_ID,
        'events': []
    },
    {
        'ownerProgram': PPGCC_ID,
        'events': []
    },
    {
        'ownerProgram': PPGD_ID,
        'events': []
    },
    {
        'ownerProgram': PPGECO_ID,
        'events': []
    },
    {
        'ownerProgram': PPGIC_ID,
        'events': []
    },
    {
        'ownerProgram': PPGSS_ID,
        'events': []
    },
    {
        'ownerProgram': PPGTUR_ID,
        'events': []
    },
]);
