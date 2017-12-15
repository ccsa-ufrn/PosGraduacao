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

db.gradesOfSubjects.insertMany([
    {
        'ownerProgram': PPGA_ID,
        'title': 'Obrigatórias-Doutorado',
        'minCredits': 10,
        'minSubjectsQtt': 5,
        'subjects': []
    },
    {
        'ownerProgram': PPGA_ID,
        'title': 'Eletivas-Doutorado',
        'minCredits': 14,
        'minSubjectsQtt': 7,
        'subjects': []
    }
]);
