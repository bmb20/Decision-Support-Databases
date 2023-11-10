"""Codice efficiente (6 minuti di esecuzione) per la geolocalizzazione degli incidenti."""

from geopy.distance import geodesic
import csv

#Funzione per calcolare la distanza tra due punti in base alle coordinate
def calcola_distanza(coord1, coord2):
    return geodesic(coord1, coord2).kilometers

#lettura del dataset geografico utilizzato, il cui output è un dizionario con le informazioni sulle città
city_info = {}
with open('/content/new_uscities.csv', mode='r', encoding='utf-8') as uscities_file:
    uscities_reader = csv.DictReader(uscities_file)
    for row in uscities_reader:
        lat = float(row['lat'])
        lon = float(row['lng'])
        #lat_group e lon_group rappresentano la parte "intera" dei valori della longitudine e latitudine associati alle città
        #questi valori sono usati poi per determinare il gruppo di coordinate a cui appartiene l'incidente
        lat_group = int(lat)
        lon_group = int(lon)
        #vede se il gruppo di coordinate è già presente nel dizionario city_info
        if (lat_group, lon_group) not in city_info:
          #se non è presente allora lo aggiunge con le relative informazioni sulla città
          #ogni gruppo di coordinate è associato alla prima città trovata nel file che condivide le stesse coordinate
            city_info[(lat_group, lon_group)] = {
                'city': row['city'],
                'state_name': row['state_name'],
                'continent': row['timezone'],
                'latitude': lat,
                'longitude': lon
            }

#Lettura del file "Police_final.csv"  e apertura del file "police_with_geoinfo" per la scrittura dei risultati
with open('/content/Police_final.csv', mode='r', encoding='utf-8') as police_file:
    with open('/content/police_with_geoinfo.csv', mode='w', newline='', encoding='utf-8') as result_file:
        police_reader = csv.DictReader(police_file)
        #con fieldnames prendo i nomi degli attributi presenti nel file Police_final e ci aggiungo le tre colonne
        #quindi fieldnames è la lista che contiene i nomi delle colonne del file
        fieldnames = police_reader.fieldnames + ['city', 'state', 'continent']
        result_writer = csv.DictWriter(result_file, fieldnames=fieldnames)
        result_writer.writeheader()

        #per ogni riga nel file police_final
        for row in police_reader:
            #prendo i valori delle coordinate
            latitudine = float(row['latitude'])
            longitudine = float(row['longitude'])

            #prendo la parte intera che serve per trovare il gruppo di coordinate dell'incidente
            lat_group_pol = int(latitudine)
            lon_group_pol = int(longitudine)

            #Cerca la città più vicina all'interno del gruppo
            #closest_city è None inizialmente (prima della ricerca)
            closest_city = None
            #limite della distanza max entro cui una città è considerata come "vicina" e quindi candidata come città da considerare
            max_distance = 100.0
            #ciclo for per scorrere il dizionario che contiene le info sulla città più vicina all'interno di quel gruppo
            #quindi per ogni gruppo di coordinate presente nel dizionario city_info
            for (group_lat, group_lon), info in city_info.items():
              #vede se il gruppo di coordinate corrente (di city_info) è abbastanza vicino al gruppo di coordinate dell'incidente
              #il minore uguale a 1 serve per impostare la differenza pari ad 1 grado sia per latitudine sia per longitudine
              #questo per ridurre la ricerca ai gruppi di coordinate che sono abbastanza vicini all'incidente
                if abs(group_lat - lat_group_pol) <= 1 and abs(group_lon - lon_group_pol) <= 1:
                  #mi calcola la distanza richiamando la funzione che utilizza la libreria geodesic
                    distance = calcola_distanza((info['latitude'], info['longitude']), (latitudine, longitudine))
                    #se la distanza è minore della massima allora associo a closest_city le informazioni della città presenti in "info"
                    #aggiorno anche la distanza massima
                    if distance < max_distance:
                        closest_city = info
                        max_distance = distance

            #se è stata trovata una città più vicina all'incidente che soddisfa i criteri impostati, associo i valori alla riga corrente
            if closest_city:
                row['city'] = closest_city['city']
                row['state'] = closest_city['state_name']
                row['continent'] = closest_city['continent']

            result_writer.writerow(row)