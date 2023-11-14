import csv
import json

"""Code to calculate Crime Gravity and then create a new file with Crime Gravity."""

#apertura file json e caricamento dati da questi file
with open('C:/Users/bianc/Desktop/LDS_Group8/Part_1/dict_partecipant_age.json', 'r') as f1_file:
    age_data = json.load(f1_file)

with open('C:/Users/bianc/Desktop/LDS_Group8/Part_1/dict_partecipant_status.json', 'r') as f2_file:
    status_data = json.load(f2_file)

with open('C:/Users/bianc/Desktop/LDS_Group8/Part_1/dict_partecipant_type.json', 'r') as f3_file:
    type_data = json.load(f3_file)

#apertura file Police_with_geoinfo.csv in modalità lettura e  Police_temp.csv in modalità scrittura
with open('C:/Users/bianc/Desktop/LDS_Group8/Part_1/Police_with_geoinfo.csv', 'r') as input_file, open('C:/Users/bianc/Desktop/LDS_Group8/Part_1/Police_temp.csv', 'w', newline='') as output_file:
    csv_reader = csv.DictReader(input_file)

    #Estrazione headers dal file csv di input
    headers = csv_reader.fieldnames
    headers.append('crime_gravity')  #aggiunta della nuova colonna crime_gravity

    #Creazione del writer per il file csv di output
    csv_writer = csv.DictWriter(output_file, fieldnames=headers)
    csv_writer.writeheader()

    for row in csv_reader:
        #Estrazione dei valori dai campi dei record
        participant_age = row['participant_age_group']
        participant_type = row['participant_type']
        participant_status = row['participant_status']

        #calcolo crime_gravity usando i dati dei file json
        crime_gravity = (
            age_data.get(participant_age, 0) *
            status_data.get(participant_status, 0) *
            type_data.get(participant_type, 0)
        )

        #aggiunta del nuovo valore
        row['crime_gravity'] = crime_gravity

        #scrittura del recordo nel file csv di output
        csv_writer.writerow(row)

"""Code to add the missing_ids as foreign key in the Police file for the Custody table."""

def aggiungi_missingIDs(file_participant, file_gun, file_geography, file_police, file_output):
    participant_data = {}
    gun_data = {}
    geography_data = {}

    #Lettura file "participant.csv" e creazione di un dizionario con le colonne di confronto come chiave
    with open(file_participant, 'r') as participant_file:
        participant_reader = csv.DictReader(participant_file)
        for row in participant_reader:
            key = (row["participant_age_group"], row["participant_status"], row["participant_type"], row["participant_gender"])
            participant_data[key] = row["participant_id"]

    #Lettura file "gun.csv" e creazione di un dizionario con le colonne di confronto come chiave
    with open(file_gun, 'r') as gun_file:
        gun_reader = csv.DictReader(gun_file)
        for row in gun_reader:
            key = (row["gun_stolen"], row["gun_type"])
            gun_data[key] = row["gun_id"]

    #Lettura file "geography.csv" e creazione di un dizionario con le colonne di confronto come chiave
    with open(file_geography, 'r') as geography_file:
        geography_reader = csv.DictReader(geography_file)
        for row in geography_reader:
            key = (row["latitude"], row["longitude"])
            geography_data[key] = row["geo_id"]

    #Apertura del file "police_with_geoinfo.csv" in modalità lettura
    with open(file_police, 'r') as police_file:
        police_reader = csv.DictReader(police_file)

        #Prende l'intestazione dal file "police_with_geoinfo.csv" e aggiunge le nuove colonne
        header = police_reader.fieldnames
        header.extend(["participant_id", "gun_id", "geo_id"])

        #Apertura file di output in modalità scrittura
        with open(file_output, 'w', newline='') as output_file:
            csv_writer = csv.DictWriter(output_file, fieldnames=header)
            csv_writer.writeheader()

            for row in police_reader:
                participant_key = (row["participant_age_group"], row["participant_status"], row["participant_type"], row["participant_gender"])
                gun_key = (row["gun_stolen"], row["gun_type"])
                geography_key = (row["latitude"], row["longitude"])

                #Aggiunta dei valori delle colonne "participant_id", "gun_id", e "geography_id" dai rispettivi dizionari
                row["participant_id"] = participant_data.get(participant_key, "")
                row["gun_id"] = gun_data.get(gun_key, "")
                row["geo_id"] = geography_data.get(geography_key, "")

                csv_writer.writerow(row)
#path dei file da utilizzare
file_participant = "C:/Users/bianc/Desktop/LDS_Group8/Part_1/Participant.csv"
file_gun = "C:/Users/bianc/Desktop/LDS_Group8/Part_1/Gun.csv"
file_geography = "C:/Users/bianc/Desktop/LDS_Group8/Part_1/Geography.csv"
file_police = "C:/Users/bianc/Desktop/LDS_Group8/Part_1//Police_temp.csv"
file_output = "C:/Users/bianc/Desktop/LDS_Group8/Part_1/Police_final.csv"
#chiamata funzione
aggiungi_missingIDs(file_participant, file_gun, file_geography, file_police, file_output)