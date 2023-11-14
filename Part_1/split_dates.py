import csv
import xml

"""XML to CSV"""

import xml.etree.ElementTree as ET

#Funzione per estrarre i dati dal file XML e convertili nel file CSV
def conversion(xml_file, csv_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    with open(csv_file, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)

        #heading del csv
        headers = []
        for item in root[0]:
            headers.append(item.tag)
        csvwriter.writerow(headers)

        #scrittura dati nel file CSV
        for element in root:
            row = []
            for item in element:
                row.append(item.text)
            csvwriter.writerow(row)

#path dei file xml e csv
xml_file = 'C:/Users/bianc/Desktop/LDS_Group8/Part_1/dates.xml'
csv_file = 'C:/Users/bianc/Desktop/LDS_Group8/Part_1/coverted_dates.csv'

conversion(xml_file, csv_file)

"""Division of the date present in the Dates file into: month, day and year"""

#path del file csv
csv_file = 'C:/Users/bianc/Desktop/LDS_Group8/Part_1/coverted_dates.csv'

#apertura file csv nella modalità lettura
with open(csv_file, 'r', newline='') as csvfile:
    csvreader = csv.reader(csvfile)

    #creazione di una nuova lista per le righe con i dati suddivisi
    rows_with_split_data = []

    for row in csvreader:
        #divisione del contenuto della prima colonna e aggiunta delle parti divise come nuove colonne
        split_data = row[0].split('-')
        part1 = split_data[0] if len(split_data) > 0 else ""
        part2 = split_data[1] if len(split_data) > 1 else ""
        part3 = split_data[2] if len(split_data) > 2 else ""
        part3_1 = part3.split(" ")

        #questo "if" è per il nome/intestazione delle colonne
        if part1 == 'date':
          part1 = 'year'
          part2 = 'month'
          part3_1[0] = 'day'
        #Creazione di una nuova riga con i dati suddivisi + i dati delle altre colonne già presenti nel file
        new_row = [part1, part2, part3_1[0]] + row[1:]

        #Aggiunta della nuova riga alla lista delle righe con i dati suddivisi
        rows_with_split_data.append(new_row)

#path del nuovo file csv con i file suddivisi
csv_file = 'C:/Users/bianc/Desktop/LDS_Group8/Part_1/split_dates.csv'

#Scrittura dei dati della lista in un file CSV
with open(csv_file, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)

    for row in rows_with_split_data:
        csvwriter.writerow(row)

"""Deduction of the day of the week and the quarter of the year from the csv file obtained with the split data"""

from datetime import datetime, date

#apertura file csv in modalità lettura
with open('C:/Users/bianc/Desktop/LDS_Group8/Part_1/split_dates.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)

    header = next(csv_reader)

    #aggiunta dei nomi/intestazioni delle due nuove colonne all'header
    header.append('day_of_the_week')
    header.append('quarter')
    header.append('date')
    
    #apertura del nuovo file finale in modalità scrittura
    with open('C:/Users/bianc/Desktop/LDS_Group8/Part_1/Date.csv', 'w', newline='') as new_csv_file:
        csv_writer = csv.writer(new_csv_file)

        #scrittura heading del nuovo file
        csv_writer.writerow(header)

        #per ogni riga nel file csv originale:
        for row in csv_reader:
            #estraggo giorno, mese e anno dalle colonne
            year = int(row[0])
            month = int(row[1])
            day = int(row[2])

            #Creazione di una data completa con datatime
            complete_date = datetime(year, month, day)
            complete_date = complete_date.date()

            #per ottenere il giorno della settimana come una stringa
            day_of_the_week = complete_date.strftime('%A')

            #per ottenere il quarto dell'anno
            quarter = (complete_date.month - 1) // 3 + 1

            #aggiunta del giorno della settimana e del quarto alla riga
            row.append(day_of_the_week)
            row.append(quarter)
            row.append(complete_date)

            #scrittura della riga aggiornata nel nuovo file csv
            csv_writer.writerow(row)