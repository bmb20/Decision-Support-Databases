import csv
import pyodbc

#informazioni per la connessione
server = 'tcp:lds.di.unipi.it'
database = 'Group_ID_8_DB'
username = 'Group_ID_8'
password = 'ZV7YV8RP'
connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

#apertura della connessione con il database usando le info presenti nella connection_string
#viene usato il blocco with perché garantisce che la connessione venga chiusa correttamente alla fine del blocco
with pyodbc.connect(connection_string) as cnxn:
    cursor = cnxn.cursor()
    
    #dizionario con le associazioni tra i nomi delle tabelle e i percorsi dei file csv corrispondenti
    table_files = {
        "Date": "C:/Users/bianc/Desktop/LDS_Group8/Part_1/Date.csv",
        "Geography": "C:/Users/bianc/Desktop/LDS_Group8/Part_1/Geography.csv",
        "Gun": "C:/Users/bianc/Desktop/LDS_Group8/Part_1/Gun.csv",
        "Participant": "C:/Users/bianc/Desktop/LDS_Group8/Part_1/Participant.csv",
        "Custody": "C:/Users/bianc/Desktop/LDS_Group8/Part_1/Custody.csv"
    }

    #iterazione sulle tabelle e lettura dei file csv
    #per ogni tabella si apre il file csv corrispondente e si utilizza csv.reader per ottenere un oggetto che può essere iterato per leggere le righe del file
    for table_name, file_path in table_files.items():
        with open(file_path, "r") as csv_file:
            csv_lines = csv.reader(csv_file, delimiter=",")

            #lettura header
            headers = next(csv_lines)

            #seek serve per riportare il cursore all'inzio del file 
            csv_file.seek(0)

            #serve per saltare l'header durante il ciclo di lettura, in modo da partire direttamente dalla seconda riga che è quella contenente i dati
            next(csv_lines, None)

            #creazione di una stringa sql per l'inserimento dei dati nella tabella corrente  
            placeholders = ",".join(["?" for _ in headers])
            columns = ",".join(headers)
            sql = f"INSERT INTO {username}.{table_name}({columns}) VALUES({placeholders})"
            print(sql)

            #iterazione sulle righe del file e per ogni riga viene eseguita una query sql per l'inserimento dei dati in tabella
            for row in csv_lines:
                #print(row)
                #Controllo di quale sia la tabella corrente ed esecuzione del cast in base al tipo dei dati nelle varie colonne
                if table_name == "Date":
                    rows=cursor.execute(sql,(int(row[0]),int(row[1]),int(row[2]),int(row[3]),row[4],int(row[5]), row[6]))
                if table_name == "Geography":
                    rows=cursor.execute(sql,(int(row[0]),float(row[1]),float(row[2]),row[3],row[4],row[5]))
                if table_name == "Gun":
                    rows=cursor.execute(sql,(int(row[0]),row[1],row[2]))
                if table_name == "Participant":
                    rows=cursor.execute(sql,(int(row[0]), row[1], row[2], row[3], row[4]))
                if table_name == "Custody":
                    rows=cursor.execute(sql,(int(row[0]),int(row[1]),int(row[2]),int(row[3]),int(row[4]), int(row[5]), int(row[6])))
            #commit della transazione per applicare le modifiche al database 
            cnxn.commit()
            print(f"Done - {table_name}")
#chiusura del cursore
cursor.close()

