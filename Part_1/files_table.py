import csv

def file_csv_partecipant(file_input, file_output):
    #utilizzo di un set per tenere traccia delle righe distinte poichè il set è una struttura dati che può contenere solo valori unici
    righe_distinte = set()

    #apertura file in modalità lettura
    with open(file_input, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        #aggiungo al set solo i record del file che si differenziano per gli attributi considerati di seguito
        for riga in csv_reader:
            chiave_distinta = (riga["participant_age_group"], riga["participant_gender"], riga["participant_status"], riga["participant_type"])
            righe_distinte.add(chiave_distinta)

    #apertura file di output in modalità scrittura
    with open(file_output, 'w', newline='') as csv_output_file:
        #scrittura intestazione file
        fieldnames = ["participant_age_group", "participant_gender", "participant_status", "participant_type"]
        csv_writer = csv.DictWriter(csv_output_file, fieldnames=fieldnames)
        csv_writer.writeheader()

        #scrittura righe del file
        for chiave_distinta in righe_distinte:
            attributo1, attributo2, attributo3, attributo4 = chiave_distinta
            csv_writer.writerow({"participant_age_group": attributo1, "participant_gender": attributo2, "participant_status": attributo3, "participant_type": attributo4})

#path dei file e chiamata di funzione
file_input = "/content/police_with_geoinfo.csv"
file_output = "/content/Participant_temp.csv"
file_csv_partecipant(file_input, file_output)

#funzione per l'aggiunta della colonna partencipant_id al file precedentemente creato
def aggiungi_participant_id(file_input, file_output):
    with open(file_input, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        header = next(csv_reader)  #lettura intestazione file

        righe = []
        for i, riga in enumerate(csv_reader): #id generato con enumerate partendo da zero e incrementando di 1 ogni volta
            participant_id = str(i)
            righe.append([participant_id] + riga) #aggiunto ad ogni riga come primo attributo della riga

    with open(file_output, 'w', newline='') as csv_output_file:
        csv_writer = csv.writer(csv_output_file)
        header.insert(0, "participant_id")  #Inserimento del nome della nuova colonna nell'intestazione
        csv_writer.writerow(header)  # Scrittura dell'intestazione

        #scrittura delle righe
        for riga in righe:
            csv_writer.writerow(riga)

#path dei file e chiamata di funzione
file_input = "/content/Participant_temp.csv"
file_output = "/content/Participant.csv"
aggiungi_participant_id(file_input, file_output)

"""File Gun"""

def file_csv_gun(file_input, file_output):
    righe_distinte = set()

    with open(file_input, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        for riga in csv_reader:
            chiave_distinta = (riga["gun_stolen"], riga["gun_type"])
            righe_distinte.add(chiave_distinta)

    with open(file_output, 'w', newline='') as csv_output_file:
        fieldnames = ["gun_stolen", "gun_type"]
        csv_writer = csv.DictWriter(csv_output_file, fieldnames=fieldnames)
        csv_writer.writeheader()

        for chiave_distinta in righe_distinte:
            attributo1, attributo2= chiave_distinta
            csv_writer.writerow({"gun_stolen": attributo1, "gun_type": attributo2})


file_input = "/content/police_with_geoinfo.csv"
file_output = "/content/Gun_temp.csv"
file_csv_gun(file_input, file_output)

def aggiungi_gun_id(file_input, file_output):
    with open(file_input, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        header = next(csv_reader)

        righe = []
        for i, riga in enumerate(csv_reader):
            gun_id = str(i)
            righe.append([gun_id] + riga)

    with open(file_output, 'w', newline='') as csv_output_file:
        csv_writer = csv.writer(csv_output_file)
        header.insert(0, "gun_id")
        csv_writer.writerow(header)

        for riga in righe:
            csv_writer.writerow(riga)

file_input = "/content/Gun_temp.csv"
file_output = "/content/Gun.csv"
aggiungi_gun_id(file_input, file_output)

"""File Geography"""

import csv

def file_csv_geo(file_input, file_output):
    righe_distinte = dict()

    with open(file_input, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        for riga in csv_reader:
            chiave_distinta = (riga["latitude"], riga["longitude"])

            #Aggiunta delle colonne "city", "state" e "continent" oltre alla latitudine e longitudine
            if chiave_distinta not in righe_distinte:
                righe_distinte[chiave_distinta] = {
                    "latitude": chiave_distinta[0],
                    "longitude": chiave_distinta[1],
                    "city": riga["city"],
                    "state": riga["state"],
                    "continent": riga["continent"]
                }

    with open(file_output, 'w', newline='') as csv_output_file:
        fieldnames = ["latitude", "longitude", "city", "state", "continent"]
        csv_writer = csv.DictWriter(csv_output_file, fieldnames=fieldnames)
        csv_writer.writeheader()

        #Scrittura delle chiavi distinte con le colonne aggiuntive nel file di output
        csv_writer.writerows(righe_distinte.values())

file_input = "/content/police_with_geoinfo.csv"
file_output = "/content/Geography_temp.csv"
file_csv_geo(file_input, file_output)

def aggiungi_geo_id(file_input, file_output):
    with open(file_input, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        header = next(csv_reader)

        righe = []
        for i, riga in enumerate(csv_reader):
            geo_id = str(i)
            righe.append([geo_id] + riga)

    with open(file_output, 'w', newline='') as csv_output_file:
        csv_writer = csv.writer(csv_output_file)
        header.insert(0, "geo_id")
        csv_writer.writerow(header)

        for riga in righe:
            csv_writer.writerow(riga)

file_input = "/content/Geography_temp.csv"
file_output = "/content/Geography.csv"
aggiungi_geo_id(file_input, file_output)