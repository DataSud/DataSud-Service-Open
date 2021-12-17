import requests
import shutil
import gzip
import pandas as pd
import glob
import os
import datetime
import pysftp

now = datetime.datetime.now()
year = now.year 

# Suppression du fichier en amont
my_file="/home/user1/Projet_Python/fichier_foncier_region_sud/DVF_geoloc_"+str(year)+"_regionsud.csv"
if os.path.exists(my_file):
    os.remove(my_file)

    # Affiche l'état du dossier et cas échéant le supprime
    print("The file: {} is deleted!".format(my_file))
else:
    print("The file: {} does not exist!".format(my_file))


def GetDataAndUnzipToCSV(num_dep):
    now = datetime.datetime.now()
    year = now.year 
    try:
        url = "https://files.data.gouv.fr/geo-dvf/latest/csv/"+str(year)+"/departements/"+num_dep+".csv.gz"
        filename = url.split("/")[-1]
        with open(filename, "wb") as f:
            r = requests.get(url)
            f.write(r.content)


        with gzip.open(filename, 'rb') as f_in:
            with open(num_dep+".csv", 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
    except:
        print("problème de téléchargement pour le département" + num_dep)

GetDataAndUnzipToCSV("04")
GetDataAndUnzipToCSV("05")
GetDataAndUnzipToCSV("06")
GetDataAndUnzipToCSV("13")
GetDataAndUnzipToCSV("83")
GetDataAndUnzipToCSV("84")


path = "/home/user1/Projet_Python/fichier_foncier_region_sud" # use your path
all_files = glob.glob(path + "/*.csv")
print(len(all_files))
li = []

for filename in all_files:
    df = pd.read_csv(filename, index_col=None, header=0)
    li.append(df)

frame = pd.concat(li, axis=0, ignore_index=True)
frame.to_csv(my_file, index = False, header=True)


# Enregistrement dans le compte sftp
tablename = "DVF_geoloc_"+str(year)+"_regionsud.csv"
cnopts = pysftp.CnOpts()
cnopts.hostkeys = None
# Paramètre de connection au serveur sftp
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
    
    sftp.put('/home/user1/Projet_Python/fichier_foncier_region_sud/'+tablename,'/uploads/'+tablename)  # upload file to public/ on remote







