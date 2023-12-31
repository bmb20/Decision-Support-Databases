import csv

file_input = "C:/Users/bianc/Desktop/LDS_Group8/Part_1/Police_final.csv"
file_output = "C:/Users/bianc/Desktop/LDS_Group8/Part_1/Custody.csv"

#dati_tabella = custody_id, partecipant_id, gun_id, geo_id, date_id, crime_gravity
#funzione per creare un file custody contenente i dati della tabella
def seleziona_colonne(file_input, file_output, colonne_selezionate):
    with open(file_input, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        fieldnames = csv_reader.fieldnames

        #contiene solo le colonne che sono presenti sia in "colonne_selezionate" sia nel fieldnames del file di input
        colonne_da_scrivere = []
        for colonna in colonne_selezionate:
            if colonna in fieldnames:
                colonne_da_scrivere.append(colonna)


        #apertura file output in scrittura
        with open(file_output, 'w', newline='') as csv_output_file:
            csv_writer = csv.DictWriter(csv_output_file, fieldnames=colonne_da_scrivere)
            csv_writer.writeheader()

            for riga in csv_reader:
              #dizionario che rappresenta una singola riga da scrivere
              #ogni chiave corrisponde a un attributo e il valore associato è il valore di quel attributo per la riga corrente
                nuova_riga = {}
                for colonna in colonne_da_scrivere:
                    #il valore associato alla colonna corrente nella riga corrente del file originale viene assegnato al dizionario "nuova_riga"
                    nuova_riga[colonna] = riga[colonna]

                csv_writer.writerow(nuova_riga)

#colonne da includere nel file di output
colonne_selezionate = ["custody_id", "participant_id", "gun_id", "geo_id", "date_fk", "crime_gravity", "incident_id"]
seleziona_colonne(file_input, file_output, colonne_selezionate)