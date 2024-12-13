#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from datetime import datetime
import pandas as pd

class Modulbuchung:
    def __init__(self, buchungsnummer, buchungsdatum, status, pruefungsversuch, pruefungsdatum=None, note=None, bestanden=False, modul_code=None, student_code=None, db_handler=None):
        self.buchungsnummer = buchungsnummer
        self.buchungsdatum = buchungsdatum.to_pydatetime() if pd.notna(buchungsdatum) else None
        self.status = status
        self.pruefungsversuch = pruefungsversuch
        # Falls pruefungsdatum ein Timestamp ist, konvertiere ihn in einen String
        self.pruefungsdatum = datetime.strptime(pruefungsdatum.strftime('%Y-%m-%d'), '%Y-%m-%d') if pd.notna(pruefungsdatum) else None
        self.note = float(note) if note is not None else None
        self.bestanden = bool(bestanden)  # Sicherstellen, dass 'bestanden' als bool behandelt wird
        self.modul_code = modul_code
        self.student_code = student_code
        self.db_handler = db_handler

        # Modul- und Studenten-Objekte initialisieren
        self.modul = self.lade_modul() if db_handler else None
        self.student = self.lade_student() if db_handler else None

    def lade_modul(self):
        """Lädt das Modul-Objekt basierend auf modul_code."""
        if not self.db_handler:
            raise ValueError("Kein DB-Handler vorhanden. Modul kann nicht geladen werden.")
        
        # Abrufen der Modul-Daten
        modul_data = self.db_handler.get_modul(self.modul_code)
        
        if modul_data is not None:
            # Debugging-Ausgabe der geladenen Daten
            print(f"Geladene Modul-Daten: {modul_data}")
            
            # Überprüfen, ob die erwarteten Spalten vorhanden sind
            if "modul_code" in modul_data.columns:
                return Modul(
                    modul_data["modul_code"].iloc[0], 
                    modul_data["modul_name"].iloc[0], 
                    modul_data["credits"].iloc[0], 
                    modul_data["tutor"].iloc[0], 
                    modul_data["pruefungsform"].iloc[0]
                )
            else:
                print(f"Spalte 'modul_code' nicht gefunden. Vorhandene Spalten: {modul_data.columns}")
        else:
            print(f"Kein Modul mit Code {self.modul_code} gefunden.")
        
        return None

    def lade_student(self):
        """Lädt das Student-Objekt basierend auf student_code."""
        if not self.db_handler:
            raise ValueError("Kein DB-Handler vorhanden. Student kann nicht geladen werden.")
        
        # Abrufen der Student-Daten
        student_data = self.db_handler.get_student(self.student_code)
        
        if student_data is not None:
            # Debugging-Ausgabe der geladenen Daten
            print(f"Geladene Student-Daten: {student_data}")
            
            # Überprüfen, ob die erwarteten Spalten vorhanden sind
            if "student_code" in student_data.columns:
                return Student(
                    student_data["student_code"].iloc[0], 
                    student_data["student_name"].iloc[0], 
                    student_data["start_studium"].iloc[0], 
                    student_data["zielnote"].iloc[0]
                )
            else:
                print(f"Spalte 'student_code' nicht gefunden. Vorhandene Spalten: {student_data.columns}")
        else:
            print(f"Kein Student mit Code {self.student_code} gefunden.")
        
        return None


    def status_anzeigen(self):
        """Zeigt den Status der Modulbuchung an."""
        return {
            "Buchungsnummer": self.buchungsnummer,
            "Status": self.status,
            "Prüfungsversuch": self.pruefungsversuch,
            "Bestanden": self.bestanden,
        }

    def ist_pruefung_bestanden(self):
        """Überprüft, ob die Prüfung bestanden wurde."""
        return self.bestanden

    def pruefungsinfo_anzeigen(self):
        """Zeigt detaillierte Prüfungsinformationen."""
        return {
            "Buchungsnummer": self.buchungsnummer,
            "Prüfungsdatum": self.pruefungsdatum.strftime('%Y-%m-%d') if self.pruefungsdatum else "Kein Datum festgelegt",
            "Prüfungsversuch": self.pruefungsversuch,
            "Note": self.note,
            "Bestanden": self.bestanden,
        }

    def __str__(self):
        """String-Darstellung der Modulbuchung."""
        modul_info = f"Modul: {self.modul.modul_name} (Code: {self.modul_code})" if self.modul else "Kein Modul"
        student_info = f"Student: {self.student.student_name} (Code: {self.student_code})" if self.student else "Kein Student"
        return f"Buchungsnummer: {self.buchungsnummer} | {modul_info} - {student_info} | Status: {self.status} | Prüfung: {self.pruefungsversuch} - Bestanden: {self.bestanden}"

class Modul:
    def __init__(self, modul_code, modul_name, credits, tutor, pruefungsform):
        self.modul_code = modul_code
        self.modul_name = modul_name
        self.credits = credits
        self.tutor = tutor
        self.pruefungsform = pruefungsform


class Student:
    def __init__(self, student_code, student_name, start_studium, zielnote):
        self.student_code = student_code
        self.student_name = student_name
        self.start_studium = start_studium
        self.zielnote = zielnote

