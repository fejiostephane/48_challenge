import csv

# Étape 1 : nettoyer le CSV pour éviter l'erreur de parsing
with open("catastrophes_naturelles_formate.csv", encoding="utf-8") as f:
    lignes = f.readlines()

lignes_nettoyees = []

for ligne in lignes:
    ligne = ligne.strip()

    # Corriger les guillemets inutiles
    ligne = ligne.replace('""[', "['").replace("]""", "]").replace('"', '')

    # Corriger les virgules internes dans les listes
    if '[' in ligne and ']' in ligne:
        debut = ligne.index('[')
        fin = ligne.index(']') + 1
        liste_str = ligne[debut:fin]
        liste_corrigee = liste_str.replace(',', ';')  # remplacer les virgules par des points-virgules
        ligne = ligne[:debut] + liste_corrigee + ligne[fin:]

    lignes_nettoyees.append(ligne)

# Sauvegarder la version nettoyée
with open("catastrophes_naturelles_parseable.csv", "w", encoding="utf-8") as f:
    for ligne in lignes_nettoyees:
        f.write(ligne + "\n")
