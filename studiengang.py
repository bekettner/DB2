#!/usr/bin/env python
# coding: utf-8

# In[6]:


from dbzugriff import DBZugriff
from semester import Semester

class Studiengang:
    def __init__(self, studiengang_code: str, studiengang_name: str, erforderliche_credits: int, mindeststudienzeit: int):
        self.studiengang_code = studiengang_code
        self.studiengang_name = studiengang_name
        self.erforderliche_credits = erforderliche_credits
        self.mindeststudienzeit = mindeststudienzeit

    def get_semester(self, dbzugriff: DBZugriff):
        """
        Gibt alle Semester des Studiengangs zurück, basierend auf den CSV-Daten, die über DBZugriff abgerufen werden.
        :param dbzugriff: Instanz von DBZugriff zum Laden der Daten.
        :return: Liste von Semester-Objekten.
        """
        semester_list = []
        
        # Hole die Semester-Daten für den Studiengang über DBZugriff
        studiengang_semester_daten = dbzugriff.get_studiengang_semester(self.studiengang_code)
        
        if studiengang_semester_daten is not None:
            for index, semester_info in studiengang_semester_daten.iterrows():
                semester_code = semester_info["semester_code"]
                semester_name = semester_info["semester_name"]
                semester = Semester(semester_code, semester_name)
                
                # Lade die Module für dieses Semester
                semester.lade_module(dbzugriff)  # Methode zum Laden der Module für das Semester
                
                # Füge das Semester zur Liste hinzu
                semester_list.append(semester)
        
        return semester_list

    def __str__(self):
        return (
            f"Studiengang: {self.studiengang_name} (Code: {self.studiengang_code})\n"
            f"Erforderliche Credits: {self.erforderliche_credits}\n"
            f"Mindeststudienzeit: {self.mindeststudienzeit} Semester"
        )


# In[ ]:




