import csv
import requests
import json
import pysftp


tablename = "Calendrier_accompagnements_actions_France_Num.csv"

# csv header
header = ['Titre', 'Thematique', 'Type de formation', 'format', 'Chef de file du groupement', 'Description courte du programme',
'Date de debut', 'Region', 'Adresse', 'Inscription']


url= "https://data.economie.gouv.fr/explore/dataset/sessions-accompagnements-actions/download/?&format=json&refine.region=Provence-Alpes-C%C3%B4te+d%E2%80%99Azur&timezone=Europe/Berlin&lang=fr"


r = requests.get(url, stream = True)

if r.status_code == 200:
    response = r.text
    data = json.loads(response)
    i = 0
    j = 1
    output = []
    for i in range(len(data)):
        titre = data[i]['fields']['titre']
        thematique = data[i]['fields']['thematique_f']
        type_formation = data[i]['fields']['type']
        format = data[i]['fields']['format_f']
        chef_file_regroupement = data[i]['fields']['organisateur']
        description = data[i]['fields']['description']
        date = data[i]['fields']['date_s']
        region = data[i]['fields']['region']
        try:
            adresse = data[i]['fields']['adresse']
        except:
            adresse = ""
        
        inscription = data[i]['fields']['lien_inscription']

        list = [titre, thematique, type_formation, format, chef_file_regroupement, description, date, region, adresse, inscription]

        output.append(list)


print(output)
with open(tablename, 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    # write the header
    writer.writerow(header)
    writer.writerows(output)

cnopts = pysftp.CnOpts()
cnopts.hostkeys = None
# tableName = "Calendrier_accompagnements_actions_France_Num.xlsx"
with pysftp.Connection('sftp.datasud.fr', port=921, username = 'xxxx', password='xxxx', cnopts = cnopts) as sftp:
    #Se rendre dans le répertoire "/uploads" du serveur DataSUD
    sftp.cwd('/uploads')
    #Récupérer la liste des fichiers présents dans le répertoire
    directory = sftp.listdir_attr()
    for attr in directory:
        #Verifier si la table existe déjà dans le répertoire et la supprimer
        if tablename in attr.filename:
            sftp.remove(tablename)
            print(tablename, 'supprimée du serveur')
    
    sftp.put('/home/user1/Projet_Python/Accompagnement_actions_France_Numerique/'+tablename,'/uploads/'+tablename)  # upload file to public/ on remote

    
#     data = [
#     ['Albania', 28748, 'AL', 'ALB'],
#     ['Algeria', 2381741, 'DZ', 'DZA'],
#     ['American Samoa', 199, 'AS', 'ASM'],
#     ['Andorra', 468, 'AD', 'AND'],
#     ['Angola', 1246700, 'AO', 'AGO'],
# ]


    