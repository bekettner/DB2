#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import os
from csvzugriff import CSVZugriff

class DBZugriff:
    def __init__(self, db_handler: CSVZugriff):
        """
        Initialisiert die DBZugriff-Klasse mit einer Instanz von CSVZugriff.
        :param db_handler: Eine Instanz von CSVZugriff, die die CSV-Dateien verwaltet.
        """
        self.db_handler = db_handler

    def read_data(self):
        """
        Ruft die read_data-Methode von CSVZugriff auf.
        :return: Dictionary mit den geladenen CSV-Daten.
        """
        return self.db_handler.read_data()
    
    def get_student(self, student_code: str):
        """
        Gibt die Daten eines Studenten basierend auf dem student_code zurück.
        :param student_code: Code des Studenten
        :return: Pandas DataFrame mit den Daten des Studenten
        """
        student_data = self.db_handler.read_data().get("student.csv")
        if student_data is not None:
            # Da student_code bereits als str eingelesen wird, ist keine Konvertierung nötig
            return student_data[student_data["student_code"] == student_code]
        else:
            print("Studenten-Daten konnten nicht geladen werden.")
            return None

    
    def get_studiengang(self, student_code: str):
        """
        Gibt die Daten aller Studiengänge zurück.
        :return: Pandas DataFrame mit den Studiengangdaten
        """
        studiengang_data = self.db_handler.read_data().get("studiengang.csv")
        if studiengang_data is not None:
            return studiengang_data
        else:
            print("Studiengang-Daten konnten nicht geladen werden.")
            return None
    
                
    def get_modul(self, modul_code: str):
        """
        Gibt die Daten eines Moduls basierend auf dem modul_code zurück.
        :param modul_code: Der Code des Moduls.
        :return: Ein Pandas DataFrame mit den Moduldaten oder ein leeres DataFrame, wenn das Modul nicht gefunden wird.
        """
        try:
            modul_data = self.read_data().get("modul.csv")
            if modul_data is not None and not modul_data.empty:
                modul_row = modul_data[modul_data["modul_code"] == modul_code]
                if not modul_row.empty:
                    return modul_row  # Rückgabe als DataFrame
                else:
                    print(f"Kein Modul mit modul_code={modul_code} gefunden.")
                    return pd.DataFrame()  # Leeres DataFrame zurückgeben
            else:
                print("Keine Daten für modul.csv gefunden.")
                return pd.DataFrame()  # Leeres DataFrame zurückgeben
        except Exception as e:
            print(f"Fehler beim Laden von modul.csv: {e}")
            return pd.DataFrame()  # Leeres DataFrame bei Fehler


    def get_modulbuchung(self, student_code: str):
        """
        Gibt die Modulbuchungen eines Studenten basierend auf dem student_code zurück.
        :param student_code: Code des Studenten
        :return: Pandas DataFrame mit den Modulbuchungen
        """
        modulbuchung_data = self.db_handler.read_data().get("modulbuchung.csv")
        if modulbuchung_data is not None:
            return modulbuchung_data[modulbuchung_data["student_code"] == student_code]
        else:
            print("Studenten-Daten konnten nicht geladen werden.")
            return None

    def get_semester(self, semester_code=None):
        """
        Gibt die Daten aller Semester zurück oder filtert nach einem bestimmten Semester-Code.
        :param semester_code: Optionaler Semester-Code, um ein bestimmtes Semester zu filtern.
        :return: Pandas DataFrame mit den Semesterdaten oder einem leeren DataFrame, wenn kein Ergebnis gefunden wird.
        """
        semester_data = self.db_handler.read_data().get("semester.csv")
        
        if semester_data is None:
            print("Semester-Daten konnten nicht geladen werden.")
            return pd.DataFrame()  # Gib einen leeren DataFrame zurück, falls keine Daten geladen werden konnten.
        
        # Wenn kein semester_code angegeben ist, alle Daten zurückgeben
        if semester_code is None:
            return semester_data
        
        # Nach semester_code filtern
        filtered_data = semester_data[semester_data["semester_code"] == semester_code]
        
        if filtered_data.empty:
            print(f"Kein Semester mit dem Code {semester_code} gefunden.")
        return filtered_data

    def get_semester_modul(self, semester_code: str):
        """
        Gibt die Modulzuordnungen eines Semesters basierend auf dem semester_code zurück.
        :param semester_code: Der Code des Semesters.
        :return: Pandas DataFrame mit den Modulzuordnungen oder ein leeres DataFrame, falls keine Daten vorhanden sind.
        """
        try:
            semester_modul_data = self.db_handler.read_data().get("semester_modul.csv")
            if semester_modul_data is not None and not semester_modul_data.empty:
                return semester_modul_data[semester_modul_data["semester_code"] == semester_code]
            else:
                print("Keine Daten für semester_modul.csv gefunden.")
                return pd.DataFrame()  # Leeres DataFrame zurückgeben
        except Exception as e:
            print(f"Fehler beim Laden von semester_modul.csv: {e}")
            return pd.DataFrame()  # Leeres DataFrame bei Fehler

    def get_student_studiengang(self, student_code: str):
        """
        Gibt die Studiengänge eines Studenten basierend auf dem student_code zurück.
        :param student_code: Code des Studenten
        :return: Pandas DataFrame mit den Studiengängen
        """
        student_studiengang_data = self.db_handler.read_data().get("student_studiengang.csv")
        if student_studiengang_data is not None:
            return student_studiengang_data[student_studiengang_data["student_code"] == student_code]
        else:
            print("Studiumsdaten-Daten konnten nicht geladen werden.")
            return None
            

    def get_studiengang_semester(self, studiengang_code: str):
        """
        Gibt die Semester eines Studiengangs basierend auf dem studiengang_code zurück.
        :param studiengang_code: Code des Studiengangs
        :return: Pandas DataFrame mit den Studiengängen
        """
        studiengang_semester_data = self.db_handler.read_data().get("studiengang_semester.csv")
        if studiengang_semester_data is not None:
            return studiengang_semester_data[studiengang_semester_data["studiengang_code"] == studiengang_code]
        else:
            print("Studiumsdaten_Semester-Daten konnten nicht geladen werden.")
            return None

    def get_completed_modules(self, student_code: str):
        """
        Gibt eine Liste der abgeschlossenen Module eines Studenten zurück, inklusive der Note.
        :param student_code: Der Code des Studenten.
        :return: Liste von abgeschlossenen Modulen.
        """
        # CSV-Daten laden
        data = self.db_handler.read_data()
        
        # Notwendige DataFrames extrahieren
        modul_data = data.get("modul.csv")
        modulbuchung_data = data.get("modulbuchung.csv")
        student_data = data.get("student.csv")
        
        if modul_data is not None and modulbuchung_data is not None and student_data is not None:
            # Filtere die Modulbuchungen nach dem student_code und beständig = True
            completed_modules = modulbuchung_data[(modulbuchung_data["student_code"] == student_code) &
                                                  (modulbuchung_data["bestanden"] == True)]
            
            # Verknüpfe die abgeschlossenen Module mit den Modul-Details
            completed_modules_details = completed_modules.merge(modul_data, on="modul_code", how="left")
            
            # Rückgabe der Liste der abgeschlossenen Module einschließlich der Note
            return completed_modules_details[["modul_code", "modul_name", "credits", "tutor", "pruefungsform", "note"]]
        else:
            print("Fehler beim Laden der Daten.")
            return None

    def get_booked_but_not_completed_modules(self, student_code: str):
        """
        Gibt eine Liste der gebuchten, aber nicht abgeschlossenen Module eines Studenten zurück.
        :param student_code: Der Code des Studenten.
        :return: Liste von gebuchten, aber nicht abgeschlossenen Modulen.
        """
        # CSV-Daten laden
        data = self.db_handler.read_data()
        
        # Notwendige DataFrames extrahieren
        modul_data = data.get("modul.csv")
        modulbuchung_data = data.get("modulbuchung.csv")
        
        if modul_data is not None and modulbuchung_data is not None:
            # Filtere die Modulbuchungen nach dem student_code und nicht bestanden (bestanden == False)
            # Hier nehmen wir an, dass "bestanden" entweder True oder False ist
            booked_not_completed_modules = modulbuchung_data[(modulbuchung_data["student_code"] == student_code) &
                                                              (modulbuchung_data["bestanden"] == False)]
            
            # Verknüpfe die gebuchten, nicht abgeschlossenen Module mit den Modul-Details
            booked_not_completed_modules_details = booked_not_completed_modules.merge(modul_data, on="modul_code", how="left")
            
            # Rückgabe der Liste der gebuchten, aber nicht abgeschlossenen Module
            return booked_not_completed_modules_details[["modul_code", "modul_name", "credits", "tutor", "pruefungsform"]]
        else:
            print("Fehler beim Laden der Daten.")
            return None

    def get_modules_not_booked_yet(self, student_code: str):
        """
        Gibt eine Liste der Module eines Studiengangs zurück, die der Student noch nicht gebucht hat.
        :param student_code: Der Code des Studenten.
        :return: Liste der Module, die der Student noch nicht gebucht hat.
        """
        # CSV-Daten laden
        data = self.db_handler.read_data()
        
        # Notwendige DataFrames extrahieren
        modul_data = data.get("modul.csv")
        modulbuchung_data = data.get("modulbuchung.csv")
        student_studiengang_data = data.get("student_studiengang.csv")
        studiengang_semester_data = data.get("studiengang_semester.csv")
        semester_modul_data = data.get("semester_modul.csv")
        
        if modul_data is not None and modulbuchung_data is not None and student_studiengang_data is not None and studiengang_semester_data is not None and semester_modul_data is not None:
            # Schritt 1: Finde den Studiengang des Studenten
            studiengang_code = student_studiengang_data[student_studiengang_data["student_code"] == student_code]["studiengang_code"]
            
            if studiengang_code.empty:
                print(f"Kein Studiengang für Student {student_code} gefunden.")
                return None
            
            # Der Student ist genau einem Studiengang zugeordnet
            studiengang_code = studiengang_code.iloc[0]
            
            # Schritt 2: Alle Semester des Studiengangs ermitteln
            semester_codes = studiengang_semester_data[studiengang_semester_data["studiengang_code"] == studiengang_code]["semester_code"]
            
            if semester_codes.empty:
                print(f"Keine Semester für Studiengang {studiengang_code} gefunden.")
                return None
            
            # Schritt 3: Alle Module der Semester ermitteln
            all_modules_in_study_program = semester_modul_data[semester_modul_data["semester_code"].isin(semester_codes)]["modul_code"].unique()
            
            # Schritt 4: Alle bereits gebuchten Module des Studenten finden
            booked_modules = modulbuchung_data[modulbuchung_data["student_code"] == student_code]["modul_code"].unique()
            
            # Schritt 5: Filtere die Module des Studiengangs, die der Student noch nicht gebucht hat
            not_booked_modules = [modul_code for modul_code in all_modules_in_study_program if modul_code not in booked_modules]
            
            # Schritt 6: Holt die Details der noch nicht gebuchten Module
            not_booked_modules_details = modul_data[modul_data["modul_code"].isin(not_booked_modules)]
            
            # Rückgabe der Liste der Module, die der Student noch nicht gebucht hat
            return not_booked_modules_details[["modul_code", "modul_name", "credits", "tutor", "pruefungsform"]]
        else:
            print("Fehler beim Laden der Daten.")
            return None


