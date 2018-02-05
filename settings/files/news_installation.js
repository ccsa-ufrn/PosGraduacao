use posgrad;

print("Inserindo notícias...");
PPGP_ID = db.postGraduations.findOne({'initials': 'PPGP'})._id;
PPGA_ID = db.postGraduations.findOne({'initials': 'PPGA'})._id;
PPGCC_ID = db.postGraduations.findOne({'initials': 'PPGCC'})._id;
PPGD_ID = db.postGraduations.findOne({'initials': 'PPGD'})._id;
PPGECO_ID = db.postGraduations.findOne({'initials': 'PPGECO'})._id;
PPGIC_ID = db.postGraduations.findOne({'initials': 'PPGIC'})._id;
PPGSS_ID = db.postGraduations.findOne({'initials': 'PPGSS'})._id;
PPGTUR_ID = db.postGraduations.findOne({'initials': 'PPGTUR'})._id;
db.news.insertMany([
    {
        'ownerProgram': PPGP_ID,
        'news' : [
          {
            'title': 'Lorem ipsum',
            'headline' : 'quod consequatur ex culpa labore tenetur voluptatem qui consequatur aut ut voluptas sapiente similique recusandae nemo quis qui et cumque',
            'body' : 'Atque veniam fuga magnam culpa necessitatibus. Consequatur dolorem magnam aut quod repellat temporibus vel natus. Possimus et est possimus aut ad est atque qui. Corrupti recusandae veritatis quia sed totam aspernatur qui. Esse aliquam magni ullam culpa possimus consequuntur. Dolores sint optio velit harum maiores ut. Rerum corrupti perspiciatis ipsa velit nisi saepe. Ex nostrum qui culpa. Voluptatibus molestiae ab mollitia reprehenderit. consectetur ex.'
          }
        ]
    },
    {
        'ownerProgram': PPGA_ID,
        'news': [],
    },
    {
        'ownerProgram': PPGCC_ID,
        'news': [],
    },
    {
        'ownerProgram': PPGD_ID,
        'news': [],
    },
    {
        'ownerProgram': PPGECO_ID,
        'news': [],
    },
    {
        'ownerProgram': PPGIC_ID,
        'news': [],
    },
    {
        'ownerProgram': PPGSS_ID,
        'news': [],
    },
    {
        'ownerProgram': PPGTUR_ID,
        'news': [],
    }
]);
