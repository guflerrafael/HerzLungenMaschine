# Import external packages
from multiprocessing.connection import wait
from pickletools import read_bytes1
import pandas as pd
from datetime import datetime
import numpy as np
import re


# Klasse Subject
class Subject():
    
    # Konstruktor mit file_name als Parameter (aus welchen Daten für Subject gelesen werden)
    def __init__(self, file_name):

        ### Aufgabe 1: Interpolation ###

        # Lesen der Daten aus csv Datei
        __f = open(file_name)
        self.subject_data = pd.read_csv(__f)

        # Nachdem Lücken nur klein sind und Daten kein gekrümmtes Verhalten aufweißen,
        # ist hier linear oder nearest am sinnvollsten.
        self.subject_data = self.subject_data.interpolate(method="nearest", axis=0) 
        
        # Variablen der Klasse anlegen
        __splited_id = re.findall(r'\d+',file_name)      
        self.subject_id = ''.join(__splited_id)
        self.names = self.subject_data.columns.values.tolist()
        self.time = self.subject_data["Time (s)"]        
        self.spO2 = self.subject_data["SpO2 (%)"]
        self.temp = self.subject_data["Temp (C)"]
        self.blood_flow = self.subject_data["Blood Flow (ml/s)"]
        print('Subject ' + self.subject_id + ' initialized')
        

### Aufgabe 2: Datenverarbeitung ###
# Dataframe Funktionen zum Berechnen des SMA und CMA

def calculate_CMA(df,n):
    return df.expanding(n).mean()

def calculate_SMA(df,n):
    return df.rolling(n).mean()

#Aufgabe 4.1:

# Der Simple Moving Averge wird zum Glätten von Daten verwendet, dabei wird immer der Durchschnitt über eine gewisse Periode(Zeit) berechnet.
# Die alten Daten werden vernachlässigt um einen gewissen Trend erkennen zu können. Kurze Daten-Ausreißer werden sehr gut geglättet.
# Diese Art von Moving Averge wird daher oft zum Traden an der Börse verwendet.
# Ein Nachteil jedoch ist dass er etwas langsam auf Veränderungen der Daten reagiert,
# er ist daher für die Datenverarbeitungen die in kurzen Zeiträumen stattfinden schlecht geeignet.

#Aufgabe 4.2:
#Desto größer n wird desto mehr werden die "Daten-Ausreißer" geglättet.