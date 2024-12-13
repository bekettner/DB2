#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import tkinter as tk
from tkinter import ttk
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd

def run_dashboard(student, booked_not_completed_modules, not_booked_modules, completed_modules):
    root = tk.Tk()
    root.title("Student Dashboard")

    # Fenstergröße anpassen
    root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")

    # Überschrift
    label = tk.Label(root, text="Studenteninformationen", font=("Arial", 16))
    label.pack(pady=10)

    # Informationen des Studenten
    info_frame = tk.Frame(root)
    info_frame.pack(pady=10, padx=10)

    student_name = student.student_name if student.student_name else "Nicht verfügbar"
    student_code = student.student_code if student.student_code else "Nicht verfügbar"
    studiengang_name = student.studiengang.studiengang_name if student.studiengang else "Nicht verfügbar"
    aktuelles_datum = datetime.now().strftime('%d.%m.%Y')

    # Die Labels und Werte nebeneinander anordnen
    data_labels = ["Name:", "Code:", "Studiengang:", "Datum:"]
    data_values = [student_name, student_code, studiengang_name, aktuelles_datum]
    
    for i, (label_text, value) in enumerate(zip(data_labels, data_values)):
        tk.Label(info_frame, text=label_text, font=("Arial", 12, "bold")).grid(row=0, column=i*2, sticky="w", padx=5)
        tk.Label(info_frame, text=value, font=("Arial", 12)).grid(row=0, column=i*2+1, sticky="w", padx=5)

    # Tabellenbereich
    table_frame = tk.Frame(root)
    table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Erstelle ein Frame für alle Tabellen nebeneinander
    tables_frame = tk.Frame(table_frame)
    tables_frame.pack(fill=tk.BOTH, expand=True)

    # Tabelle: Gebuchte, aber nicht abgeschlossene Module
    if booked_not_completed_modules is not None and not booked_not_completed_modules.empty:
        tk.Label(tables_frame, text="Gebuchte, aber nicht abgeschlossene Module:", font=("Arial", 14)).grid(row=0, column=0, padx=10)

        booked_tree = ttk.Treeview(tables_frame, columns=["Modul-Code", "Modul-Name", "Credits", "Tutor", "Prüfungsform"], show="headings", height=10)
        booked_tree.grid(row=1, column=0, padx=10, pady=10)

        # Spaltenüberschriften hinzufügen
        for col in ["Modul-Code", "Modul-Name", "Credits", "Tutor", "Prüfungsform"]:
            booked_tree.heading(col, text=col)
            booked_tree.column(col, width=70)

        # Daten einfügen und "Credits" formatieren
        for _, row in booked_not_completed_modules.iterrows():
            booked_tree.insert("", "end", values=(
                row["modul_code"],
                row["modul_name"],
                row["credits"],
                row["tutor"],
                row["pruefungsform"]
            ))
    else:
        tk.Label(tables_frame, text="Keine gebuchten, aber nicht abgeschlossenen Module vorhanden.", font=("Arial", 14)).grid(row=1, column=0, padx=10)

    # Tabelle: Offene Module
    if not_booked_modules is not None and not not_booked_modules.empty:
        tk.Label(tables_frame, text="Offene Module:", font=("Arial", 14)).grid(row=0, column=1, padx=10)

        open_tree = ttk.Treeview(tables_frame, columns=["Modul-Code", "Modul-Name", "Credits", "Tutor", "Prüfungsform"], show="headings", height=10)
        open_tree.grid(row=1, column=1, padx=10, pady=10)

        for col in ["Modul-Code", "Modul-Name", "Credits", "Tutor", "Prüfungsform"]:
            open_tree.heading(col, text=col)
            open_tree.column(col, width=70)

        for _, row in not_booked_modules.iterrows():
            open_tree.insert("", "end", values=(
                row["modul_code"],
                row["modul_name"],
                row["credits"],
                row["tutor"],
                row["pruefungsform"]
            ))
    else:
        tk.Label(tables_frame, text="Keine offenen Module vorhanden.", font=("Arial", 14)).grid(row=1, column=1, padx=10)

    # Tabelle: Abgeschlossene Module
    if completed_modules is not None and not completed_modules.empty:
        tk.Label(tables_frame, text="Abgeschlossene Module:", font=("Arial", 14)).grid(row=0, column=2, padx=10)

        completed_tree = ttk.Treeview(tables_frame, columns=["Modul-Code", "Modul-Name", "Credits", "Tutor", "Prüfungsform", "Note"], show="headings", height=10)
        completed_tree.grid(row=1, column=2, padx=10, pady=10)

        for col in ["Modul-Code", "Modul-Name", "Credits", "Tutor", "Prüfungsform", "Note"]:
            completed_tree.heading(col, text=col)
            completed_tree.column(col, width=70)

        for _, row in completed_modules.iterrows():
            completed_tree.insert("", "end", values=(
                row["modul_code"],
                row["modul_name"],
                row["credits"],
                row["tutor"],
                row["pruefungsform"],
                row["note"]
            ))
    else:
        tk.Label(tables_frame, text="Keine abgeschlossenen Module vorhanden.", font=("Arial", 14)).grid(row=1, column=2, padx=10)

    # Kreisdiagramm für Prüfungsformen und Semesterplot nebeneinander anzeigen
    if completed_modules is not None and not completed_modules.empty:
        pruefungsform_counts = completed_modules["pruefungsform"].value_counts()

        # Kreisdiagramm erstellen (kleiner)
        fig_pie, ax_pie = plt.subplots(figsize=(3, 3))  # Größeren Wert für größere Diagramme verwenden
        ax_pie.pie(pruefungsform_counts, labels=pruefungsform_counts.index, autopct='%1.1f%%', startangle=90)
        ax_pie.axis('equal')

        # Frame für Diagramme (Kreisdiagramm und Semesterplot)
        diagrams_frame = tk.Frame(root)
        diagrams_frame.pack(pady=10, padx=10)

        # Kreisdiagramm im Tkinter-Fenster anzeigen
        pie_canvas = FigureCanvasTkAgg(fig_pie, master=diagrams_frame)
        pie_canvas.draw()
        pie_canvas.get_tk_widget().pack(side="left", padx=10)  # Links positionieren

        semester_plot = student.plot_combined_credits_per_semester()
        if semester_plot:
            semester_canvas = FigureCanvasTkAgg(semester_plot, master=diagrams_frame)
            semester_canvas.draw()
            semester_canvas.get_tk_widget().pack(side="left", padx=10)  # Rechts vom Kreisdiagramm positionierensemester_plot = student.plot_combined_credits_per_semester()  # Für das Diagramm übergeben
        

        # Berechnungen für die neue Tabelle
        total_credits = completed_modules["credits"].sum()
        average_grade = round(completed_modules["note"].mean(), 2)
        target_grade = student.zielnote  # Zielnote aus dem Student-Objekt holen

        result_frame = tk.Frame(diagrams_frame)
        result_frame.pack(side="left", padx=10)

        result_data = [("Zielnote:", target_grade), 
                       ("Aktueller Notendurchschnitt:", average_grade), 
                       ("Erreichte ECTS-Credits:", total_credits)]

        for i, (label_text, value) in enumerate(result_data):
            tk.Label(result_frame, text=label_text, font=("Arial", 12, "bold")).grid(row=i, column=0, sticky="w", pady=2)
            tk.Label(result_frame, text=value, font=("Arial", 12)).grid(row=i, column=1, sticky="w", pady=2)

    root.mainloop()

