#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from datetime import datetime

class Dashboard:
    def __init__(self, student):
        """
        Initialisiert das Dashboard mit einem Student-Objekt.
        :param student: Instanz der Klasse Student
        """
        self.student = student

    def anzeigen(self):
        """
        Zeigt das Dashboard an.
        """
        aktuelles_datum = datetime.now().strftime('%d.%m.%Y')
        print("=" * 80)
        print(f"Dashboard für {self.student.student_name} (Matrikelnummer: {self.student.student_code})")
        print(f"Studiengang: {self.student.studiengang.studiengang_name if self.student.studiengang else 'Unbekannt'}")
        print(f"Datum: {aktuelles_datum}")
        print("=" * 80)

