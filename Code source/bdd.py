###################################bdd###############################
import mysql.connector
conn = mysql.connector.connect(host="127.0.0.1",
                               user="********", password="*******", 
                               database="calculateur")
cursor = conn.cursor()
#####ajouter une donnée à la base de données##########
reference = ("Confiture de fraise 250g", 10, 10)
cursor.execute("""INSERT INTO event (Nom, Organisateur, Resultat) VALUES(%s, %s, %s)""", reference)
conn.commit()
#####récupérer une donnée de la base de données#######
cursor.execute("""SELECT Nom, Organisateur, resultat FROM event""")
rows = cursor.fetchall()
for row in rows:
   st.markdown('{0} : {1} - {2}'.format(row[0], row[1], row[2]))
######################################################
conn.close()
#####################################################################
