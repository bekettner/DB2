#!/usr/bin/env python
# coding: utf-8

# In[4]:


# csvzugriff.py
import pandas as pd

class CSVZugriff:
    def __init__(self):
        # Hier werden die Pfade zu den CSV-Dateien festgelegt
        self.file_paths = [
            r"D:\studium\2. semester\Objektorientierte Programmierung\Basislisten\modul.csv",
            r"D:\studium\2. semester\Objektorientierte Programmierung\Basislisten\modulbuchung.csv",
            r"D:\studium\2. semester\Objektorientierte Programmierung\Basislisten\semester.csv",
            r"D:\studium\2. semester\Objektorientierte Programmierung\Basislisten\semester_modul.csv",
            r"D:\studium\2. semester\Objektorientierte Programmierung\Basislisten\student.csv",
            r"D:\studium\2. semester\Objektorientierte Programmierung\Basislisten\student_studiengang.csv",
            r"D:\studium\2. semester\Objektorientierte Programmierung\Basislisten\studiengang.csv",
            r"D:\studium\2. semester\Objektorientierte Programmierung\Basislisten\studiengang_semester.csv"
        ]
        
        # Definiere ein Mapping, welche Spalten als Strings behandelt werden sollen
        self.column_types = {
            "student.csv": {"student_code": str, "zielnote": float},
            "student_studiengang.csv": {"student_code": str, "studiengang_code": str},
            "modul.csv": {"modul_code": str, "credits": int},
            "modulbuchung.csv": {"student_code": str, "modul_code": str, "bestanden": bool},
            "semester.csv": {"semester_code": str},
            "semester_modul.csv": {"semester_code": str, "modul_code": str},
            "studiengang.csv": {"studiengang_code": str, "credits": int, "semester": int},
            "studiengang_semester.csv": {"studiengang_code": str, "semester_code": str}
        }

          # Definiere, welche Spalten als Datum geparst werden sollen
        self.date_columns = {
            "student.csv": ["start_studium"],  
            "modulbuchung.csv": ["buchungsdatum", "pruefungsdatum"],  
        }
        
    def read_data(self):
        """
        Liest alle CSV-Dateien in der Liste ein und gibt ein Dictionary zurück.
        Der Schlüssel ist der Dateiname, der Wert ist der eingelesene DataFrame.
        :return: Dictionary mit Dateinamen als Schlüssel und DataFrames als Werte
        """
        data_dict = {}
        for file_path in self.file_paths:
            try:
                # Extrahiere den Dateinamen (z. B. "student.csv")
                file_name = file_path.split("\\")[-1]
                
                # Überprüfe, ob für diese Datei spezielle Spaltentypen definiert sind
                dtype = self.column_types.get(file_name, None)
                parse_dates = self.date_columns.get(file_name, None)
                
                # Lade die Datei mit definierten Datentypen und Datumsspalten
                data = pd.read_csv(file_path, dtype=dtype, parse_dates=parse_dates)
                
                # Speichere den DataFrame in das Dictionary
                data_dict[file_name] = data
                print(f"Datei {file_name} erfolgreich geladen.")  # Debugging: Bestätigung
            except FileNotFoundError:
                print(f"Datei nicht gefunden: {file_path}")
            except Exception as e:
                print(f"Fehler beim Lesen der Datei {file_path}: {e}")
        return data_dict

# Kurzer Test, um sicherzustellen, dass die CSV-Dateien geladen werden können
if __name__ == "__main__":
    csv_zugriff = CSVZugriff()
    csv_zugriff.read_data()  # Teste das Einlesen der CSV-Dateien


# In[ ]:




