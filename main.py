#!/usr/bin/env python
# coding: utf-8
project/
│
├── models/
│   ├── __init__.ipynb
│   ├── student.ipynb
│   ├── studiengang.ipynb
│   ├── semester.ipynb
│   ├── modul.ipynb
│   ├── modulbuchung.ipynb
│   ├── dashboard.ipynb
│
├── database/
│   ├── __init__.ipynb
│   ├── dbzugriff.ipynb
│
├── gui/
│   ├── __init__.ipynb
│   ├── dashboard_gui.ipynb
│
├── main.ipynb
├── requirements.txt
└── README.md

# In[ ]:


# main.py
from dbzugriff import DBZugriff
from csvzugriff import CSVZugriff
from student import Student
import dashboard

def main():
    # Erstelle eine Instanz von CSVZugriff
    csv_zugriff = CSVZugriff()  # Hier CSVZugriff korrekt instanziieren

    # Erstelle eine Instanz von DBZugriff und übergebe die CSVZugriff-Instanz
    dbhandler = DBZugriff(csv_zugriff)

    # Benutzereingabe für den Studenten-Code
    student_code = input("Bitte gib den Studenten-Code ein: ")

    # Versuche, die Studentendaten zu holen
    student_data = dbhandler.get_student(student_code)

    if student_data is not None and not student_data.empty:
        print(f"Studenten-Daten für {student_code} gefunden. Starte Dashboard...")

        student_name = student_data['student_name'].values[0]
        start_studium = student_data.iloc[0]["start_studium"]
        zielnote = student_data.iloc[0]["zielnote"]

        # Student-Objekt erstellen
        student = Student(
            student_code=student_code,
            student_name=student_name,
            start_studium=start_studium,
            zielnote=zielnote,
            db_handler=dbhandler
        )

        # Hole die Module des Studenten
        booked_not_completed_modules = dbhandler.get_booked_but_not_completed_modules(student_code)
        not_booked_modules = dbhandler.get_modules_not_booked_yet(student_code)
        completed_modules = dbhandler.get_completed_modules(student_code)
        student_plot = student.plot_combined_credits_per_semester()

        # Starte das Dashboard und übergebe alle gesammelten Daten
        dashboard.run_dashboard(student, booked_not_completed_modules, not_booked_modules, completed_modules)


    else:
        print(f"Kein Student mit dem Code {student_code} gefunden.")

# Führe die Main-Funktion aus
if __name__ == "__main__":
    main()


# 
