# -*- coding: utf-8 -*-
"""
Created on Sat Jan  4 10:56:24 2021

@author: Nadia, Lobna, Arnaud (élèves Data Analystes de la Wild Code School)
"""

#les imports
import pandas as pd
import folium
import numpy
import streamlit as st
from streamlit_folium import folium_static
from streamlit import caching
import base64
import psycopg2

# HOST = "127.0.0.1"
# USER = "xxx"
# PASSWORD = "xxxx"
# DATABASE = "xxx"
# # Open connection
# conn = psycopg2.connect("host=%s dbname=%s user=%s password=%s" % (HOST, DATABASE, USER, PASSWORD))
# # Open a cursor to send SQL commands
# cur = conn.cursor()
# # Execute a SQL SELECT command
# sql = "SELECT * FROM public.ville"
# cur.execute(sql)
# # Fetch data line by line
# raw = cur.fetchone()
# while raw:
#     print (raw[0])
#     print (raw[1])
#     raw = cur.fetchone()
# # Close connection
# conn.close()


#TITRE
title_main = st.markdown("<h1 style='text-align: center; color: black;'>INDICE DE PERFORMANCE ENVIRONNEMENTALE</h1>"
, unsafe_allow_html=True)
image_main = st.markdown('![Region Sud](https://nsm09.casimages.com/img/2020/12/17//20121704061016813117177105.jpg)'
, unsafe_allow_html=True)



#SIDEBAR
title_sbar = st.sidebar.title("INFORMATIONS STRUCTURE ORGANISATRICE")

#NOM STRUCTURE
name_struc_input = st.sidebar.text_input("Nom de la structure")

#NBR PERSONNE ASSOS
nb_struc_input = st.sidebar.text_input("Nombre de personnes composant la structure")

#NOM MANIF SPORT
name_manif_input = st.sidebar.text_input("Nom de la manifestation sportive")

# LISTE DEROULANTE VILLE
#connection au serveur SQL
# conn = psycopg2.connect("host=%s dbname=%s user=%s password=%s" % (HOST, DATABASE, USER, PASSWORD))
conn_ville = psycopg2.connect(
    host="xxx",
    user="xxx",
    password="xxx",
    database="xxx"
    )
#appel du dataframe Ville
df_ville = pd.read_sql("SELECT * FROM public.ville",conn_ville)    
localisation = st.sidebar.selectbox("Lieu de la manifestation", (df_ville['commune']))


map_sb_cb = st.sidebar.checkbox('Montrer la carte')
if map_sb_cb:
#LOCALISATION FOLIUM
    df_localisation = df_ville[df_ville['commune']==localisation]
    m = folium.Map(location=[df_localisation['longitude'],df_localisation['latitude']],zoom_start=12)
    folium.Marker(location=[df_localisation['longitude'],df_localisation['latitude']],
                  popup = f'Nom: {localisation}').add_to(m)
    folium_static(m)
conn_ville.close()
#DUREE MANIFESTATION
nb_jour_input = st.sidebar.text_input("Durée de la manifestation (en jours)")

#TYPE ACTIVITE
type_sport_input = st.sidebar.text_input("Type d’activité sportive")

#TYPE DE PARTICIPANTS
particip_sb = st.sidebar.selectbox("Niveau sportif",
    ('Amateur','Professionnel'))

#NBR PARTICIPANTS
nb_particip_input = st.sidebar.text_input("Nombre de participants")


#fonction pour créer le df avec les informations de la sidebar
@st.cache(allow_output_mutation=True)
def get_data_side():
    return []

if st.sidebar.button("Enregistrer les saisies"):
    if nb_jour_input == "":
        nb_jour_input = 0
    if nb_particip_input == "":
        nb_particip_input = 0
    get_data_side().append({"nom": name_struc_input, 
                       "nbr_personne_structure": nb_struc_input, 
                       "nom_manifestation_sportive": name_manif_input,
                       "lieu_manifestation":localisation,
                       "duree_manifestation": nb_jour_input,
                       "type_activite": type_sport_input,
                       "type_participants": particip_sb,
                       "nbr_participants": nb_particip_input})
    df_side = pd.DataFrame(get_data_side())

    conn_side = psycopg2.connect(
        host="xxx",
        user="xxx",
        password="xxx",
        database="xxx"
        )
    cursor = conn_side.cursor()
    cols = ",".join([str(i) for i in df_side.columns.tolist()])
    for i,row in df_side.iterrows():
        #attention si chiffre non rempli erreur pour enregistrer les données
        sql = "INSERT INTO public.information_structure ("+cols+") VALUES("+"%s,"*(len(row)-1)+"%s)"
    cursor.execute(sql, tuple(row))
    conn_side.commit()
    st.sidebar.write("Données enregistrées.")
    conn_side.close()


conn_id_assoc = psycopg2.connect(
    host="xxx",
    user="xxx",
    password="xxx",
    database="xxx"
    )
#appel du dataframe Ville
id_asso = pd.read_sql("SELECT MAX(id_information_structure) FROM public.information_structure",conn_id_assoc)    
df_last_asso = id_asso['max']

id_asso['max'] = id_asso['max'].astype(int)

id_asso = id_asso['max'][0].tolist()
#print(type(id_asso))
#df_last_asso = pd.to_numeric(df_last_asso, downcast='integer')
#print(type(df_last_asso))
conn_id_assoc.close()

@st.cache(allow_output_mutation=True)
def get_data_gestion_dechet():
    return []
@st.cache(allow_output_mutation=True)
def get_data_eco():
    return []
@st.cache(allow_output_mutation=True)
def get_data_eau():
    return []
@st.cache(allow_output_mutation=True)
def get_data_elec():
    return []
@st.cache(allow_output_mutation=True)
def get_data_mouillage():
    return []
@st.cache(allow_output_mutation=True)
def get_data_deplacement():
    return []
@st.cache(allow_output_mutation=True)
def get_data_qualite_vehicule():
    return []
@st.cache(allow_output_mutation=True)
def get_data_qualite_installation():
    return []
#INDICATEURS
indicat_title = st.title('LES INDICATEURS')


#INDICATEURS1 (5=25)
indic01_header = st.header("GESTION ET VALORISATION DES DÉCHETS")
point01= 0

selectbox_01= st.selectbox('Réduction des déchets ?',('-','Oui (plusieurs choix possibles)','Non'))
rr01 = ""
rr02 = ""
rr03 = ""
if selectbox_01=='Oui (plusieurs choix possibles)':
    a01=st.checkbox('Dispositif zéro bouteilles plastique ')
    if a01:
        point01= point01 + 2
        rr01 = "Dispositif zéro bouteilles plastique"
    a02=st.checkbox('Emballages écoresponsables')
    if a02:
        point01= point01 + 2
        rr02 = "Emballages écoresponsables"
    a03=st.checkbox('Couverts durables ')
    if a03:
        point01= point01 + 1
        rr03 = "Couverts durables"
elif selectbox_01=='Non':
    point01=point01 + 0.2
else:
    point01 = point01 + 0


    
selectbox_02= st.selectbox('Tri Sélectif ?',('-','Oui','Non'))
if selectbox_02=='Oui':
    point01= point01 + 5
elif selectbox_02=='Non':
    point01=point01 + 0.2
else:
    point01 = point01 + 0
    
selectbox_03= st.selectbox("Collecte et traitement d'autres déchets ?",
                           ('-','Oui (plusieurs choix possibles)','Non'))
s01 = " "
s02 = " "
s03 = " "
s04 = " "
s05 = " "
if selectbox_03=='Oui (plusieurs choix possibles)':
    c01=st.checkbox('Mégots')
    if c01:
        point01= point01 + 1
        s01 = "Mégots"
    c02=st.checkbox('Biodéchets')
    if c01:
        point01= point01 + 1
        s02 = "Biodéchets"
    c03=st.checkbox('Capsules de café/thé')
    if c01:
        point01= point01 + 1
        s03 = "Capsules de café/thé"
    c04=st.checkbox('Stickers')
    if c01:
        point01= point01 + 1
        s04 = "Stickers"
    c05=st.checkbox('Gourdes')
    if c01:
        point01= point01 + 1
        s05 = "Gourdes"
elif selectbox_03=='Non':
    point01=point01 + 0.2
else:
    point01 = point01 + 0
    
selectbox_04= st.selectbox('Actions de valorisation et gestion des déchets sportifs ?',('-','Oui','Non'))
if selectbox_04=='Oui':
    point01= point01 + 5
elif selectbox_04=='Non':
    point01=point01 + 0.2
else:
    point01 = point01 + 0
    
selectbox_05= st.selectbox('Restauration sur place ?',('-','Oui (plusieurs choix possibles)','Non'))
t01 = ""
t02 = ""
t03 = "" 
t04 = ""  
t05 = ""
if selectbox_05=='Oui (plusieurs choix possibles)':
    e01=st.checkbox('Local/Circuits courts ')
    if e01:
        point01= point01 + 1
        t01="Local/Circuits courts"
    e02=st.checkbox('BIO')
    if e02:
        point01= point01 + 1
        t02="BIO"
    e03=st.checkbox('Couverts biodégradables ou durables')
    if e03:
        point01= point01 + 1
        t03="Couverts biodégradables ou durables"
    e04=st.checkbox('Doggy bag')
    if e04:
        point01= point01 + 1
        t04="Doggy bag"
    e05=st.checkbox('Consigne de vaisselles ou de bouteilles')
    if e05:
        point01= point01 + 1
        t05="Consigne de vaisselles ou de bouteilles"
elif selectbox_05=='Non':
    point01=point01 + 0.2
else:
    point01 = point01 + 0


if 15<point01<=25:
    wst = st.write("Résultat de l'indicateur:")
    image_Smiley_content = 'https://nsm09.casimages.com/img/2021/01/29//mini_21012902491716813117235674.jpg'
    st.image(image_Smiley_content,use_column_width=False)
elif 10<point01<=15:
    wst = st.write("Résultat de l'indicateur:")
    image_Smiley_neutre = 'https://nsm09.casimages.com/img/2021/01/29//mini_21012902491716813117235675.jpg'
    st.image(image_Smiley_neutre,use_column_width=False)
    sh_01 = st.subheader("RECOMMANDATIONS:")
    sm_01 = st.markdown("""<p>Renseignez-vous auprès de votre Mairie concernant 
les solutions de tri sélectif.
<p>La commune est-elle engagée dans un programme zero dechet plastique ?</p>
<p>Positionnez vos poubelles de tri de manière stratégique, afin d’en faciliter 
l’accès au grand public et aux compétiteurs.</p>
<p>Savez-vous qu’il existe des associations locales spécialisées dans la collecte 
des déchets (Les Alchimistes, Les Petites Choses, etc) ou mettant à disposition 
un annuaire des acteurs locaux engagés (ARBE, CPIE) ? N’hésitez pas à les contacter !</p>
<p>Pour une alimentation plus sûre et plus durable, privilégiez une 
restauration locale afin de faire travailler nos producteurs régionaux.</p>
<p>Des commerces engagés peuvent délivrer gratuitement de l’eau pour 
remplir des gourdes ou acceptent des boxs pour acheter des aliments (cf réseau vrac).</p>
<p>Des communes mettent à disposition des fontaines à eau dans l’espace public.</p>"""
, unsafe_allow_html=True)    
elif 0<point01<=10:
    wst = st.write("Résultat de l'indicateur:")
    image_Smiley_triste = 'https://nsm09.casimages.com/img/2021/01/29//mini_21012902491716813117235676.jpg'
    st.image(image_Smiley_triste,use_column_width=False)
    sh_01 = st.subheader("RECOMMANDATIONS:")
    sm_01 = st.markdown("""<p>Renseignez-vous auprès de votre Mairie concernant 
les solutions de tri sélectif.
<p>La commune est-elle engagée dans un programme zero dechet plastique ?</p>
<p>Positionnez vos poubelles de tri de manière stratégique, afin d’en faciliter 
l’accès au grand public et aux compétiteurs.</p>
<p>Savez-vous qu’il existe des associations locales spécialisées dans la collecte 
des déchets (Les Alchimistes, Les Petites Choses, etc) ou mettant à disposition 
un annuaire des acteurs locaux engagés (ARBE, CPIE) ? N’hésitez pas à les contacter !</p>
<p>Pour une alimentation plus sûre et plus durable, privilégiez une 
restauration locale afin de faire travailler nos producteurs régionaux.</p>
<p>Des commerces engagés peuvent délivrer gratuitement de l’eau pour 
remplir des gourdes ou acceptent des boxs pour acheter des aliments (cf réseau vrac).</p>
<p>Des communes mettent à disposition des fontaines à eau dans l’espace public.</p>"""
, unsafe_allow_html=True)
else:
    st.write("")

#INDICATEURS2 (2=10)
indic02_header = st.header("SENSIBILISATION A L’ÉCORESPONSABILITÉ")
point02= 0

selectbox06= st.selectbox('Campagne d’informations grand public dédiée sur site ?',
                          ('-','Oui (plusieurs choix possibles)','Non'))
u01 = ""
u02 = ""
u03 = ""
u04 = ""
if selectbox06=='Oui (plusieurs choix possibles)':
    f01=st.checkbox('Actions de sensibilisation sur site via une association spécialisée')
    if f01:
        point02= point02 + 2
        u01 = "Actions de sensibilisation sur site via une association spécialisée"
    f02=st.checkbox('Panneaux d’affichage informatifs')
    if f02:
        point02= point02 + 1
        u02 = "Panneaux d’affichage informatifs"
    f03=st.checkbox('Jeux concours')
    if f03:
        point02= point02 + 1
        u03 = "Jeux concours"
    f04=st.checkbox('Réseaux sociaux')
    if f04:
        point02= point02 + 1
        u04 = "Réseaux sociaux"
elif selectbox06== 'Non':
    point02=point02 + 0.5
else:
    point02 = point02 + 0
    
selectbox07= st.selectbox('Actions de formation auprès des personnels d’organisation ?',('-','Oui','Non'))
if selectbox07=='Oui':
    point02= point02 + 5
elif selectbox07=='Non':
    point02=point02 + 0.5
else:
    point02 = point02 + 0
    
if 5.5<point02<=10:
    wst = st.write("Résultat de l'indicateur:")
    image_Smiley_content = 'https://nsm09.casimages.com/img/2021/01/29//mini_21012902491716813117235674.jpg'
    st.image(image_Smiley_content,use_column_width=False)
elif 1<point02<=5.5:
    wst = st.write("Résultat de l'indicateur:")
    image_Smiley_neutre = 'https://nsm09.casimages.com/img/2021/01/29//mini_21012902491716813117235675.jpg'
    st.image(image_Smiley_neutre,use_column_width=False)
    sh_02 = st.subheader("RECOMMANDATIONS:")
    sm_02 = st.markdown("""<p>Connaissez-vous la plateforme 
<a href="http://www.remed-zero-plastique.org/" target="_blank">ReMed Zéro Plastique</a>
, un réseau qui rassemble et fédère à l’échelle de la Région SUD, toute organisation 
ou partie prenante souhaitant contribuer à la réduction des déchets sauvages qui 
aboutissent en Méditerranée ?</p>
<p>Votre commune ou l'intercommunalité peuvent déjà avoir développé des 
outils de communication.</p>
<p>Les Parcs naturels mènent régulièrement des actions de sensibilisation.</p>
<p>Le site de CITEO met à dispo des kits de communication.</p>
<p>Savez-vous que la Ligue Sud de Voile a lancé une campagne d’informations 
nommée 'Ecorégatier'?</p>"""
, unsafe_allow_html=True)
elif 0<point02<=1:
    wst = st.write("Résultat de l'indicateur:")
    image_Smiley_triste = 'https://nsm09.casimages.com/img/2021/01/29//mini_21012902491716813117235676.jpg'
    st.image(image_Smiley_triste,use_column_width=False)
    sh_02 = st.subheader("RECOMMANDATIONS:")
    sm_02 = st.markdown("""<p>Connaissez-vous la plateforme 
<a href="http://www.remed-zero-plastique.org/" target="_blank">ReMed Zéro Plastique</a>
, un réseau qui rassemble et fédère à l’échelle de la Région SUD, toute organisation 
ou partie prenante souhaitant contribuer à la réduction des déchets sauvages qui 
aboutissent en Méditerranée ?</p>
<p>Votre commune ou l'intercommunalité peuvent déjà avoir développé des 
outils de communication.</p>
<p>Les Parcs naturels mènent régulièrement des actions de sensibilisation.</p>
<p>Le site de CITEO met à dispo des kits de communication.</p>
<p>Savez-vous que la Ligue Sud de Voile a lancé une campagne d’informations 
nommée 'Ecorégatier'?</p>"""
, unsafe_allow_html=True)
else:
    st.write("")
    
#INDICATEURS3 (2=10)
indic03_header = st.header("CONSOMMATION D’EAU")
point03= 0

water_input = st.number_input("""Quantité estimée d’eau potable en Litre qui sera consommée 
pendant la manifestation:""", step = 0.1)
#formule de calcul à déterminer pour pondérer le poids de la quantité en litre par utilisateur

selectbox08= st.selectbox("Solutions de réduction de la consommation d’eau ? ",
                          ('-','Oui (plusieurs choix possibles)','Non'))
v01 = ""
v02 = ""
v03 = ""
v04 = ""
if selectbox08=='Oui (plusieurs choix possibles)':
    h01=st.checkbox('Réducteur de débit extérieur (type tuyaux de rinçage)')
    if h01:
        point03= point03 + 1
        v01="Réducteur de débit extérieur (type tuyaux de rinçage)"
    h02=st.checkbox('Réducteur de débit intérieur (type douches)')
    if h02:
        point03= point03 + 1
        v02="Réducteur de débit intérieur (type douches)"
    h03=st.checkbox('Chasse d’eau à vitesse')
    if h03:
        point03= point03 + 1
        v03="Chasse d’eau à vitesse"
    h04=st.checkbox('Autres solutions')
    if h04:
        point03= point03 + 2
        v04="Autres solutions"
elif selectbox08=='Non':
    point03=point03 + 0.5
else:
    point03 = point03 + 0
    
selectbox09= st.selectbox('Récupération des eaux de pluie ?',('-','Oui','Non'))
if selectbox09=='Oui':
    point03= point03 + 5
elif selectbox09=='Non':
    point03=point03 + 0.5
else:
    point03 = point03 + 0

if 5.5<point03<=10:
    wst = st.write("Résultat de l'indicateur:")
    image_Smiley_content = 'https://nsm09.casimages.com/img/2021/01/29//mini_21012902491716813117235674.jpg'
    st.image(image_Smiley_content,use_column_width=False)
elif 1<point03<=5.5:
    wst = st.write("Résultat de l'indicateur:")
    image_Smiley_neutre = 'https://nsm09.casimages.com/img/2021/01/29//mini_21012902491716813117235675.jpg'
    st.image(image_Smiley_neutre,use_column_width=False)
    sh_03 = st.subheader("RECOMMANDATIONS:")
    sm_03 = st.markdown("""<p>Savez-vous qu'un réducteur d'eau réduit le débit mais 
pas la capacité d'usage ?</p>""", unsafe_allow_html=True)
elif 0<point03<=1:
    wst = st.write("Résultat de l'indicateur:")
    image_Smiley_triste = 'https://nsm09.casimages.com/img/2021/01/29//mini_21012902491716813117235676.jpg'
    st.image(image_Smiley_triste,use_column_width=False)
    sh_03 = st.subheader("RECOMMANDATIONS:")
    sm_03 = st.markdown("""<p>Savez-vous qu'un réducteur d'eau réduit le débit mais 
pas la capacité d'usage ?</p>""", unsafe_allow_html=True)
else:
    st.write("")
    
#INDICATEURS4 (3=15)
indic04_header = st.header("CONSOMMATION ÉLECTRIQUE")
point04= 0

kwh_input = st.number_input("""Quantité estimée d'électricité en kW.h qui sera consommée 
pendant la manifestation:""", step = 0.1)
#formule de calcul à déterminer pour pondérer le poids de la quantité de kW.h par utilisateur

selectbox10= st.selectbox("Energies renouvelables ? ",('-','Oui (plusieurs choix possibles)','Non'))
w01 = ""
w02 = ""
w03 = ""
w04 = ""
if selectbox10=='Oui (plusieurs choix possibles)':
    j01=st.checkbox('Panneaux solaires')
    if j01:
        point04= point04 + 1
        w01 = "Panneaux solaires"
    j02=st.checkbox('Électricité verte (abonnement spécifiques)')
    if j02:
        point04= point04 + 1
        w02 = "Électricité verte (abonnement spécifiques)"
    j03=st.checkbox('Energie hydraulique grâce aux courants marins')
    if j03:
        point04= point04 + 1
        w03 = "Energie hydraulique grâce aux courants marins"
    j04=st.checkbox("Autres types d'énergies")
    if j04:
        point04= point04 + 2
        w04 = "Autres types d'énergies"
elif selectbox10=='Non':
    point04=point04 + 0.33
else:
    point04 = point04 + 0
    
selectbox11= st.selectbox("Solutions de réduction de consommation électrique ?",
                          ('-','Oui (plusieurs choix possibles)','Non'))
x01=""
x02=""
x03=""
x04=""
if selectbox11=='Oui (plusieurs choix possibles)':
    k01=st.checkbox('Détecteur de mouvements')
    if k01:
        point04= point04 + 1
        x01="Détecteur de mouvements"
    k02=st.checkbox('Mise en veille automatique du matériel informatique')
    if k02:
        point04= point04 + 1
        x02="Mise en veille automatique du matériel informatique"
    k03=st.checkbox('Utilisation de lampes basse consommation')
    if k03:
        point04= point04 + 1
        x03="Utilisation de lampes basse consommation"
    k04=st.checkbox('Autres réductions')
    if k04:
        point04= point04 + 2
        x04="Autres réductions"
elif selectbox11 =='Non':
    point04=point04 + 0.33
else:
    point04 = point04 + 0
    
selectbox12= st.selectbox("Production autonome en énergies renouvelables ?",('-','Oui','Non'))
if selectbox12=='Oui':
    point04= point04 + 5
elif selectbox12=='Non':
    point04=point04 + 0.34
else:
    point04 = point04 + 0


if 8<point04<=15:
    wst = st.write("Résultat de l'indicateur:")
    image_Smiley_content = 'https://nsm09.casimages.com/img/2021/01/29//mini_21012902491716813117235674.jpg'
    st.image(image_Smiley_content,use_column_width=False)
elif 1<point04<=8:
    wst = st.write("Résultat de l'indicateur:")
    image_Smiley_neutre = 'https://nsm09.casimages.com/img/2021/01/29//mini_21012902491716813117235675.jpg'
    st.image(image_Smiley_neutre,use_column_width=False)
    sh_04 = st.subheader("RECOMMANDATIONS:")
    sm_04 = st.markdown("""<p>Savez-vous qu’une ampoule à économie d’énergie consomme 3 à 5 fois 
moins d’énergie et dure 6 à 8 fois plus longtemps ?</p>
<p>Savez-vous que passer de 20° à 19° degrés Celsius en intérieur 
permet de réduire votre facture de 7 % ?</p>""", unsafe_allow_html=True)
elif 0<point04<=1:
    wst = st.write("Résultat de l'indicateur:")
    image_Smiley_triste = 'https://nsm09.casimages.com/img/2021/01/29//mini_21012902491716813117235676.jpg'
    st.image(image_Smiley_triste,use_column_width=False)
    sh_04 = st.subheader("RECOMMANDATIONS:")
    sm_04 = st.markdown("""<p>Savez-vous qu’une ampoule à économie d’énergie consomme 3 à 5 fois 
moins d’énergie et dure 6 à 8 fois plus longtemps ?</p>
<p>Savez-vous que passer de 20° à 19° degrés Celsius en intérieur 
permet de réduire votre facture de 7 % ?</p>""", unsafe_allow_html=True)
else:
    st.write("")
    
#INDICATEURS5 (1=5)
indic05_header = st.header("MOUILLAGES DES BATEAUX ET BOUÉES DE RÉGATES")
point05= 0

selectbox13= st.selectbox("Dispositifs de sensibilisation aux écosystèmes fragiles ?",
                          ('-','Oui (plusieurs choix possibles)','Non'))
yy01=""
yy02=""
yy03=""
if selectbox13=='Oui (plusieurs choix possibles)':
    m01=st.checkbox('Mouillages hors herbiers de posidonie ?')
    if m01:
        point05= point05 + 2
        yy01="Mouillages hors herbiers de posidonie ?"
    m02=st.checkbox("Utilisation d’applications dédiées de type DONIA ?")
    if m02:
        point05= point05 + 1
        yy02="Utilisation d’applications dédiées de type DONIA ?"
    m03=st.checkbox("Utilisation de bouées géostationnaires ?")
    if m03:
        point05= point05 + 2
        yy03="Utilisation de bouées géostationnaires ?"
elif selectbox13=='Non':
    point05=point05 + 1
else:
    point05 = point05 + 0
    
if 2<point05<=5:
    wst = st.write("Résultat de l'indicateur:")
    image_Smiley_content = 'https://nsm09.casimages.com/img/2021/01/29//mini_21012902491716813117235674.jpg'
    st.image(image_Smiley_content,use_column_width=False)
elif 1<point05<=2:
    wst = st.write("Résultat de l'indicateur:")
    image_Smiley_neutre = 'https://nsm09.casimages.com/img/2021/01/29//mini_21012902491716813117235675.jpg'
    st.image(image_Smiley_neutre,use_column_width=False)
    sh_05 = st.subheader("RECOMMANDATIONS:")
    sm_05 = st.markdown("""<p>Connaissez-vous l’application mobile DONIA, qui permet à tous les 
amoureux de la mer d’échanger des informations tout en contribuant à protéger les 
écosystèmes marins sensibles ?</p>
<p>Le <a href="http://www.shom.fr/" target="_blank">SHOM</a> a pour mission de 
connaître et décrire l’environnement physique marin dans ses relations avec l’atmosphère, 
avec les fonds marins et les zones littorales, d’en prévoir l’évolution et d’assurer 
la diffusion des informations correspondantes.</p>"""
, unsafe_allow_html=True)
elif 0<point05<=1:
    wst = st.write("Résultat de l'indicateur:")
    image_Smiley_triste = 'https://nsm09.casimages.com/img/2021/01/29//mini_21012902491716813117235676.jpg'
    st.image(image_Smiley_triste,use_column_width=False)
    sh_05 = st.subheader("RECOMMANDATIONS:")
    sm_05 = st.markdown("""<p>Connaissez-vous l’application mobile DONIA, qui permet à tous les 
amoureux de la mer d’échanger des informations tout en contribuant à protéger les 
écosystèmes marins sensibles ?</p>
<p>Le <a href="http://www.shom.fr/" target="_blank">SHOM</a> a pour mission de 
connaître et décrire l’environnement physique marin dans ses relations avec l’atmosphère, 
avec les fonds marins et les zones littorales, d’en prévoir l’évolution et d’assurer 
la diffusion des informations correspondantes.</p>"""
, unsafe_allow_html=True)
else:
    st.write("")
    
#INDICATEURS6 (1=5)
indic06_header = st.header("DÉPLACEMENT DES ÉQUIPAGES ET DU PUBLIC")
point06= 0

km_input = st.number_input("""Distance en KM du domicile de l'association vers le 
lieu de la manifestation:""", step = 0.1)
#formule de calcul à déterminer pour pondérer le poids du ratio km par utilisateur

checkbox01= st.write("Modes de déplacements des équipages (plusieurs choix possibles):")
z01=st.checkbox("A pied")
z02=st.checkbox("A vélo")
z03=st.checkbox("Transports en commun")
z04=st.checkbox("Covoiturage")
z05=st.checkbox("Voitures électriques ou hybrides")
z06=st.checkbox("Véhicules individuels")
zz01 = ""
zz02 = ""
zz03 = ""
zz03 = ""
zz04 = ""
# if z01 and z02:
#     point06= point06 + 5
#     zz01.append("à pied et à vélo")
# elif z01 or z02:
#     point06= point06 + 3
#     zz01.append("à pied ou à vélo")
# elif z03 or z04:
#     point06= point06 + 2
#     zz01.append("Transports en commun ou Covoiturage")
# elif z05:
#     point06= point06 + 1
#     zz01.append("Voitures électriques ou hybrides")
# else:
#     point06 = point06 + 0
#     zz01.append("véhicules individuels")

if z01 or z02:
    point06= point06 + 5
    zz01="à pied ou à vélo"
if z03 or z04:
    point06= point06 + 2
    zz02 = "Transports en commun ou Covoiturage"
if z05:
    point06= point06 + 1
    zz03="Voitures électriques ou hybrides"
if z06:
    point06 = point06 + 0
    zz04="véhicules individuels"
    
if 3<point06<=8:
    wst = st.write("Résultat de l'indicateur:")
    image_Smiley_content = 'https://nsm09.casimages.com/img/2021/01/29//mini_21012902491716813117235674.jpg'
    st.image(image_Smiley_content,use_column_width=False)    
elif 1<point06<=3:
    wst = st.write("Résultat de l'indicateur:")
    image_Smiley_neutre = 'https://nsm09.casimages.com/img/2021/01/29//mini_21012902491716813117235675.jpg'
    st.image(image_Smiley_neutre,use_column_width=False)
    sh_06 = st.subheader("RECOMMANDATIONS:")
    sm_06 = st.markdown("""<p>Savez-vous que l’ADEME met à disposition un outil pour calculer le 
bilan carbone de votre manifestation ?</p>""", unsafe_allow_html=True)    
elif 0<point06<=1:
    wst = st.write("Résultat de l'indicateur:")
    image_Smiley_triste = 'https://nsm09.casimages.com/img/2021/01/29//mini_21012902491716813117235676.jpg'
    st.image(image_Smiley_triste,use_column_width=False)
    sh_06 = st.subheader("RECOMMANDATIONS:")
    sm_06 = st.markdown("""<p>Savez-vous que l’ADEME met à disposition un outil pour calculer le 
bilan carbone de votre manifestation ?</p>""", unsafe_allow_html=True)
else:
    st.write("")
    
#INDICATEURS7 (3=15)
indic07_header = st.header("QUALITÉ DES VEHICULES D'ASSISTANCE ET DE SÉCURITÉ")
point07= 0

selectbox14= st.selectbox('Embarcations écoconçues ?',('-','Oui','Non'))
if selectbox14=='Oui':
    point07= point07 + 5
elif selectbox14=='Non':
    point07=point07 + 0.5
else:
    point07 = point07 + 0

checkbox02= st.write('Type de motorisation des embarcations (plusieurs choix possibles):')
y01=st.checkbox('Electrique')
y02=st.checkbox('Hybride')
y03=st.checkbox('Diesel')
y04=st.checkbox('Essence')
xx01=""
xx02=""
xx03=""
if y01:
    point07= point07 + 3
    xx01 = "Electrique"
if y02:
    point07= point07 + 2
    xx02 = "Hybride"
if y03 or y04:
    point07 = point07 + 0
    xx03 = "Diesel ou Essence"

selectbox15= st.selectbox('Les produits d’entretien sont-ils biodégradables ?',('-','Oui','Non'))
if selectbox15=='Oui':
    point07= point07 + 5
elif selectbox15=='Non':
    point07=point07 + 0.5
else:
    point07 = point07 + 0

if 8<point07<=15:
    wst = st.write("Résultat de l'indicateur:")
    image_Smiley_content = 'https://nsm09.casimages.com/img/2021/01/29//mini_21012902491716813117235674.jpg'
    st.image(image_Smiley_content,use_column_width=False) 
elif 1<point07<=8:
    wst = st.write("Résultat de l'indicateur:")
    image_Smiley_neutre = 'https://nsm09.casimages.com/img/2021/01/29//mini_21012902491716813117235675.jpg'
    st.image(image_Smiley_neutre,use_column_width=False)
    sh_07 = st.subheader("RECOMMANDATIONS:")
    sm_07 = st.markdown("<p>Pensez à entretenir vos véhicules et vos embarcations.</p>", unsafe_allow_html=True)
elif 0<point07<=1:
    wst = st.write("Résultat de l'indicateur:")
    image_Smiley_triste = 'https://nsm09.casimages.com/img/2021/01/29//mini_21012902491716813117235676.jpg'
    st.image(image_Smiley_triste,use_column_width=False)
    sh_07 = st.subheader("RECOMMANDATIONS:")
    sm_07 = st.markdown("<p>Pensez à entretenir vos véhicules et vos embarcations.</p>", unsafe_allow_html=True)
else:
    st.write("")
    
#INDICATEURS8 (3=15)
indic08_header = st.header("QUALITÉ DES INSTALLATIONS ACCUEILLANTES")
point08= 0

selectbox16= st.selectbox('Le port de plaisance est-il certifié « Ports Propres » ?',('-','Oui','Non','Je ne sais pas'))
if selectbox16=='Oui':
    point08= point08 + 5
elif selectbox16=='Non':
    point08=point08 + 0.33
elif selectbox16=='Je ne sais pas':
    st.markdown("""<p>Vous pouvez le déterminer sur le site suivant: 
                <a href="https://www.ports-propres.org/ports-certifies/" target="_blank">Ports propres</a></p>""", 
                unsafe_allow_html=True)
else:
    point08 = point08 + 0
    
selectbox17= st.selectbox('La base nautique est-elle basse consommation (R12) ?',('-','Oui','Non','Je ne sais pas'))
if selectbox17=='Oui':
    point08= point08 + 5
elif selectbox17=='Non':
    point08=point08 + 0.33
else:
    point08 = point08 + 0
    
selectbox18= st.selectbox('Adhésion à une Charte zéro plastique  ?',
                          ('-','Oui (plusieurs choix possibles)','Non','Je ne sais pas'))
aa01=""
aa02=""
if selectbox18=='Oui (plusieurs choix possibles)':
    r01=st.checkbox('Charte Région')
    if r01:
        point08= point08 + 3
        aa01="Charte Région"
    r02=st.checkbox("Charte Ligue")
    if r02:
        point08= point08 + 2
        aa02="Charte Ligue"
elif selectbox18=='Non':
    point08=point08 + 0.34
else:
    point08 = point08 + 0

if 7<point08<=15:
    wst = st.write("Résultat de l'indicateur:")
    image_Smiley_content = 'https://nsm09.casimages.com/img/2021/01/29//mini_21012902491716813117235674.jpg'
    st.image(image_Smiley_content,use_column_width=False)     
elif 1<point08<=7:
    wst = st.write("Résultat de l'indicateur:")
    image_Smiley_neutre = 'https://nsm09.casimages.com/img/2021/01/29//mini_21012902491716813117235675.jpg'
    st.image(image_Smiley_neutre,use_column_width=False)
    sh_08 = st.subheader("RECOMMANDATIONS:")
    sm_08 = st.markdown("""<p>Votre port est-il certifié « Ports Propres » et « Ports Propres actif 
en biodiversité » ou est-il simplement engagé dans la démarche ?</p>
<p>Votre port est-il adhérent à la Charte des ports de plaisance de Provence-Alpes-Côte d’Azur ?</p>
<p>La base nautique a-t-elle été récemment modernisée, en particulier en matière d’isolation ?</p>
<p>L’établissement d’accueil et/ou l’association organisatrice ont-ils adhéré à la Charte 
régionale «Zéro déchet plastique » ?</p>"""
, unsafe_allow_html=True)
elif 0<point08<=1:
    wst = st.write("Résultat de l'indicateur:")
    image_Smiley_triste = 'https://nsm09.casimages.com/img/2021/01/29//mini_21012902491716813117235676.jpg'
    st.image(image_Smiley_triste,use_column_width=False)
    sh_08 = st.subheader("RECOMMANDATIONS:")
    sm_08 = st.markdown("""<p>Votre port est-il certifié « Ports Propres » et « Ports Propres actif 
en biodiversité » ou est-il simplement engagé dans la démarche ?</p>
<p>Votre port est-il adhérent à la Charte des ports de plaisance de Provence-Alpes-Côte d’Azur ?</p>
<p>La base nautique a-t-elle été récemment modernisée, en particulier en matière d’isolation ?</p>
<p>L’établissement d’accueil et/ou l’association organisatrice ont-ils adhéré à la Charte 
régionale «Zéro déchet plastique » ?</p>"""
, unsafe_allow_html=True)
else:
    st.write("")


#INDICE
indice_title = st.title("VOTRE INDICE")

#formule simple pour calculer le total
score_total= point01+point02+point03+point04+point05+point06+point07+point08

validate = st.button('Voir mon indice')
if validate:
    score_total= point01+point02+point03+point04+point05+point06+point07+point08
    if 81<score_total<=100:
        imageA = 'https://nsm09.casimages.com/img/2021/01/18//21011803005016813117217095.jpg'
        st.image(imageA,use_column_width=True)
        wA = st.write('Excellent ! Votre indice est A.')
    elif 62<score_total<=81:
        imageB = 'https://nsm09.casimages.com/img/2021/01/18//21011803004916813117217092.jpg'
        st.image(imageB,use_column_width=True)
        wB = st.write('Très bien ! Votre indice est B.')
    elif 44<score_total<=62:
        imageC = 'https://nsm09.casimages.com/img/2021/01/18//21011803004916813117217093.jpg'
        st.image(imageC,use_column_width=True)
        wC = st.write('Bien ! Votre indice est C.')
    elif 25<score_total<=44:
        imageD = 'https://nsm09.casimages.com/img/2021/01/18//21011803005016813117217094.jpg'
        st.image(imageD,use_column_width=True)
        wD = st.write('Votre indice est D.')
    elif 6<score_total<=25:
        imageE = 'https://nsm09.casimages.com/img/2021/01/18//21011803004916813117217087.jpg'
        st.image(imageE,use_column_width=True)
        wE = st.write('Votre indice est E.')
    else: 
        not_yet = st.markdown("""Vous devez remplir les différents champs du questionnaire pour 
faire apparaitre votre indice de performance environnemental.""", unsafe_allow_html=True)

if validate:
    #gestion des déchets
    get_data_gestion_dechet().append({"_id_structure_dechets": id_asso, 
                       "reduction_dechets": str(selectbox_01) + ", " + rr01 + ", " + rr02 + ", " + rr03, 
                       "tri_selectif": str(selectbox_02),
                       "collecte_traitement_autres_dechets": str(selectbox_03) + ", " + s01 + ", " + s02 + ", " + s03 + ", " + s04 + ", " + s05,
                       "actions_valorisations_gestion_dechets_sportifs": str(selectbox_04),
                       "restauration_sur_place":str(selectbox_05) + ", " + t01 + ", " + t02 + ", " + t03 + ", " + t04 + ", " +t05})
    df_gestion_dechets = pd.DataFrame(get_data_gestion_dechet())

    #eco responsabilite
    get_data_eco().append({"_id_structure_sensibilisation_ecoresponsabilite": id_asso, 
                        "campagne_info_site": str(selectbox06) + ", " + u01 + ", " + u02 + ", " + u03 + ", " + u04, 
                        "action_formation": str(selectbox07)})
   
    df_eco = pd.DataFrame(get_data_eco())
    
    #consommation d'eau
    if water_input == "":
        water_input = 0
    get_data_eau().append({"_id_structure_consommation_eau": id_asso, 
                        "quantite_eau_potable": water_input, 
                        "reduction_consommation_eau": str(selectbox08) + ", " + v01 + ", " + v02 + ", " + v03 + ", " + v04,
                        "recuperation_eaux_pluie":str(selectbox09)})
    df_eau = pd.DataFrame(get_data_eau())

    #consommation électrique
    if kwh_input == "":
        kwh_input = 0
    get_data_elec().append({"_id_structure_consommation_electrique": id_asso, 
                        "quantite_electricite": kwh_input, 
                        "energies_renouvelables":str(selectbox10) + ", " + w01 + ", " + w02 + ", " + w03 + ", " + w04,
                        "solutions_reductions_consommations":str(selectbox11)+ ", " + x01 + ", " + x02 + ", " + x03 + ", " + x04,
                        "production_autonome_energies_renouvelables":str(selectbox12)})
    df_elec = pd.DataFrame(get_data_elec())

    #mouillage bateau
    get_data_mouillage().append({"_id_structure_mouillages": id_asso, 
                        "dispositifs_sensibilisation_ecosystemes_fragiles": str(selectbox13) + ", "+ yy01 + ", " + yy02 + ", " + yy03})
    df_mouillage = pd.DataFrame(get_data_mouillage())

    #deplacement equipages publics
    if km_input == "":
        km_input = 0
    get_data_deplacement().append({"_id_deplacement_equipages_publics": id_asso, 
                        "distance_km":km_input,
                        "modes_deplacements_equipages": zz01 + ", " + zz02 + ", " + zz03 + ", " + zz04})
    df_deplacement = pd.DataFrame(get_data_deplacement())

    #qualite vehicule assistance
    get_data_qualite_vehicule().append({"_id_structure_qualite_vehicule_assistance_securite": id_asso, 
                        "embarcations_ecoconcues":str(selectbox14),
                        "produits_entretien_biodegradables":str(selectbox15),
                        "type_motorisation_embarcation":xx01 + ", " + xx02 + ", " + xx03})
    df_qualite_vehicule = pd.DataFrame(get_data_qualite_vehicule())

    #qualite installation
    get_data_qualite_installation().append({"_id_structure_qualite_installation": id_asso, 
                        "port_plaisance_certifie_ports_propres":str(selectbox16),
                        "base_nautique_basse_consommation":str(selectbox17),
                        "adhesion_charte_zero_plastique":str(selectbox18) + ", " + aa01 + ", " + aa02 })
    df_qualite_installation = pd.DataFrame(get_data_qualite_installation())


    conn_add_data = psycopg2.connect(
        host="xxx",
        user="xxx",
        password="xxx",
        database="xxx"
        )
    cursor = conn_add_data.cursor()
    cols = ",".join([str(i) for i in df_gestion_dechets.columns.tolist()])
    #print(cols)
    for i,row in df_gestion_dechets.iterrows():
        sql = "INSERT INTO public.gestion_valorisation_dechets ("+cols+") VALUES ("+"%s,"*(len(row)-1)+"%s)"
    cursor.execute(sql, tuple(row))
    conn_add_data.commit()

    cols = ",".join([str(i) for i in df_eco.columns.tolist()])
    print(cols)
    for i,row in df_eco.iterrows():
        sql = "INSERT INTO public.sensibilisation_ecoresponsabilite ("+cols+") VALUES ("+"%s,"*(len(row)-1)+"%s)"
    cursor.execute(sql, tuple(row))
    conn_add_data.commit()

    cols = ",".join([str(i) for i in df_eau.columns.tolist()])
    print(cols)
    for i,row in df_eau.iterrows():
        sql = "INSERT INTO public.consommation_eau ("+cols+") VALUES ("+"%s,"*(len(row)-1)+"%s)"
    cursor.execute(sql, tuple(row))
    conn_add_data.commit()

    cols = ",".join([str(i) for i in df_elec.columns.tolist()])
    print(cols)
    for i,row in df_elec.iterrows():
        sql = "INSERT INTO public.consommation_electrique ("+cols+") VALUES ("+"%s,"*(len(row)-1)+"%s)"
    cursor.execute(sql, tuple(row))
    conn_add_data.commit()

    cols = ",".join([str(i) for i in df_mouillage.columns.tolist()])
    print(cols)
    for i,row in df_mouillage.iterrows():
        sql = "INSERT INTO public.mouillages_bateaux_bouees_regates ("+cols+") VALUES ("+"%s,"*(len(row)-1)+"%s)"
    cursor.execute(sql, tuple(row))
    conn_add_data.commit()

    cols = ",".join([str(i) for i in df_deplacement.columns.tolist()])
    print(cols)
    for i,row in df_deplacement.iterrows():
        sql = "INSERT INTO public.deplacement_equipages_publics ("+cols+") VALUES ("+"%s,"*(len(row)-1)+"%s)"
    cursor.execute(sql, tuple(row))
    conn_add_data.commit()

    cols = ",".join([str(i) for i in df_qualite_vehicule.columns.tolist()])
    print(cols)
    for i,row in df_qualite_vehicule.iterrows():
        sql = "INSERT INTO public.qualite_vehicule_assistance_securite ("+cols+") VALUES ("+"%s,"*(len(row)-1)+"%s)"
    cursor.execute(sql, tuple(row))
    conn_add_data.commit()

    cols = ",".join([str(i) for i in df_qualite_installation.columns.tolist()]) 
    print(cols)
    for i,row in df_qualite_installation.iterrows():
        sql = "INSERT INTO public.qualite_installation_accueillante ("+cols+") VALUES ("+"%s,"*(len(row)-1)+"%s)"
    cursor.execute(sql, tuple(row))
    conn_add_data.commit()

    conn_add_data.close()




#SAUVEGARDE
indice_save = st.title("SAUVEGARDE")
df_side = pd.DataFrame(get_data_side())

#c'est pour le moment une sauvegarde de la sidebar en .csv
#mais cela devrait être une sauvegarde de l'intégralité du questionnaire en .pdf pour l'utilisateur

@st.cache(allow_output_mutation=True)
def download_link(object_to_download, download_filename, download_link_text):
    if isinstance(object_to_download,pd.DataFrame):
        object_to_download = object_to_download.to_csv(index=False)

    b64 = base64.b64encode(object_to_download.encode()).decode()

    return f'<a href="data:file/txt;base64,{b64}" download="{download_filename}">{download_link_text}</a>'
    
end = st.selectbox("Avez-vous rempli l'intégralité du questionnaire et souhaitez-vous garder une copie de vos réponses?",
                   ['-', 'Non','Oui'])
if end == "Oui":
    if st.button('Télécharger vos réponses en .CSV'):
        tmp_download_link = download_link(df_side, 'VOS DONNÉES.csv', 'Cliquez ici pour télécharger vos données !')
        st.markdown(tmp_download_link, unsafe_allow_html=True)
        caching.clear_cache()
elif end == "Non":
    st.write("Pas de souci. Je vous invite à finir de remplir le questionnaire si ce n'est pas déjà fait.")
else:
    st.write("")
