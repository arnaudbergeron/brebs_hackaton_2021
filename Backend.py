import numpy as np
import pandas as pd
import math
import random



def simulation_data_habitant(N): #Simule une population d'habitant inscrit sur le site web
  list_city = ["Montreal", "Toronto", "Quebec", "Winnipeg", "Ottawa", "Calgary", "Vancouver","Edmonton", "Mississauga", "Laval", "Halifax", "Saskatoon", "Hamilton", "Brampton", "Gatineau", "Saint-Jerome"]
  list_language = ["Anglais", "Francais", "Aucune", "Espagnol", "Italien", "Mandarin", "Allemand", "Russe", "Portugais", "Japonais", "Hindi", "Bengali", "Panjabi", "Coreen", "Vietnamien", "Roumain", "Turc", "Arabe"]
  list_interest = ["Chien", "Chat", "Animaux", "Sport", "Film","Lecture", "Ski", "Randonner",  "Jeux video", "Cuisine", "Musique", "Art", "Photographie", "Humour", "Benevolat", "Nature", "Automobile"]

  array_habitant_canada = np.empty([N,6], dtype=np.dtype('U100'))

  for i in range(N): #Pour générer N habitants du canada
    city = random.choice(list_city)
    first_language = random.choice(list_language[:2]) #Première langue entre Français et Anglais
    seconde_language = random.choice([x for x in list_language[:3] if x != first_language]) #Seconde langue différente de la première et pour avoir plus de personne billingue dans la population, environ 66% de la population billingue
    language_learn = random.choice(list_language[3:18]) #Langue à apprendre différente de langue connu et ne peux pas être aucune
    first_interest = random.choice(list_interest)
    seconde_interest = random.choice([x for x in list_interest if x != first_interest]) #Second intérêt différent du premier
    habitant = np.array([[city, first_language, seconde_language, language_learn, first_interest, seconde_interest]])
    array_habitant_canada[i] = habitant
  return array_habitant_canada

def simulation_data_immigrant(N): #Simule une population d'immigrant inscrit sur le site web
  list_city = ["Montreal", "Toronto", "Quebec", "Winnipeg", "Ottawa", "Calgary", "Vancouver","Edmonton", "Mississauga", "Laval", "Halifax", "Saskatoon", "Hamilton", "Brampton", "Gatineau", "Saint-Jerome"]
  list_language = ["Anglais", "Francais", "Aucune", "Espagnol", "Italien", "Mandarin", "Allemand", "Russe", "Portugais", "Japonais", "Hindi", "Bengali", "Panjabi", "Coreen", "Vietnamien", "Roumain", "Turc", "Arabe"]
  list_interest = ["Chien", "Chat", "Animaux", "Sport", "Film","Lecture", "Ski", "Randonner",  "Jeux video", "Cuisine", "Musique", "Art", "Photographie", "Humour", "Benevolat", "Nature", "Automobile"]

  array_habitant_canada = np.empty([N,6], dtype=np.dtype('U100'))

  for i in range(N): #Pour générer 500 immigrants au canada
    city = random.choice(list_city)
    first_language = random.choice(list_language[3:18])
    if (random.randint(1,4) == 1): #Pour avoir moins de billingue
      seconde_language = random.choice([x for x in list_language[3:18] if x != first_language]) #Seconde langue différente de la première
    else:
      seconde_language = "Aucune"
    language_learn = random.choice(list_language[:2]) #Langue à apprendre Anglais ou Francais
    first_interest = random.choice(list_interest)
    seconde_interest = random.choice([x for x in list_interest if x != first_interest]) #Second intérêt différent du premier
    habitant = np.array([[city, first_language, seconde_language, language_learn, first_interest, seconde_interest]])
    array_habitant_canada[i] = habitant
  return array_habitant_canada

pd_df_habitant = pd.DataFrame(simulation_data_habitant(1000))
pd_df_immi = pd.DataFrame(simulation_data_immigrant(1000))



pd_df_habitant.columns = ['ville', 'langue1', 'langue2', 'langue_apprendre', 'passion1', 'passion2']
pd_df_immi.columns = ['ville', 'langue1', 'langue2', 'langue_apprendre', 'passion1', 'passion2']
pd_df_habitant['id'] = pd_df_habitant.index
pd_df_immi['id'] = pd_df_immi.index

def recommend_parfaites_queb_immi(pd_df_habitant, df_immi, id): #Fait le match entre un habitant et plusieurs immigrants selon le ID du l'habitant
    langue_parles = [pd_df_habitant.iloc[id][1], pd_df_habitant.iloc[id][2]]
    langue_voulues = pd_df_habitant.iloc[id][3]
    ville = pd_df_habitant.iloc[id][0]
    #check if there are compatibilities with language they want to learn and what the immigrants speak
    resultats_langue = np.where((df_immi['langue1'] == str(langue_voulues))|(df_immi['langue2'] == str(langue_voulues)), df_immi['id'], np.nan)
    resultats_ville = np.where(df_immi['ville'] == ville, df_immi['id'], np.nan) #check if there is a match in city
    resultats_langue2 = np.where(((df_immi['langue_apprendre'] == str(langue_parles[0])) | (df_immi['langue_apprendre'] == str(langue_parles[1]))), df_immi['id'], np.nan)
    resultats_prem = np.where(resultats_langue == resultats_ville, resultats_ville, np.nan)
    resultats = pd.DataFrame(np.where(resultats_prem == resultats_langue2, resultats_ville, np.nan))
    resultats.dropna(inplace=True)   

    return np.array(resultats) #retourne la liste de tous les immigrants qui match avec l'habitant


print("Habitant au Canada :")
print(pd_df_habitant.iloc[0])
print()
print("Immigrant au Canada :")
print(pd_df_immi.iloc[recommend_parfaites_queb_immi(pd_df_habitant, pd_df_immi, 0)[0]])




