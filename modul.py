#!/usr/bin/env python
# coding: utf-8

# In[2]:


from dbzugriff import DBZugriff

class Modul:
    def __init__(self, modul_code: str, modul_name: str, credits: int, tutor: str, preufungsform: str, db_handler: DBZugriff):
        self.modul_code = modul_code
        self.modul_name = modul_name
        self.credits = credits
        self.tutor = tutor
        self.pruefungsform = pruefungsform
        self.db_handler = db_handler
        
        # Lade die Moduldaten sofort beim Erstellen des Moduls
        self.lade_daten()

    def lade_daten(self):
        """
        Lädt die Moduldaten aus der DBZugriff-Klasse.
        """
        try:
            # Hole die Daten des Moduls basierend auf modul_code
            modul_data = self.db_handler.get_modul(self.modul_code)
            
            # Überprüfen, ob Daten gefunden wurden
            if modul_data is not None:
                self.modul_name = modul_data["modul_name"]  # Name des Moduls
                self.credits = modul_data["credits"]       # Credits des Moduls
                self.tutor = modul_data["tutor"]           # Tutor des Moduls
                self.pruefungsform = modul_data["pruefungsform"]  # Prüfungsform
            else:
                raise ValueError(f"Modul {self.modul_code} konnte nicht gefunden werden.")
        except KeyError as e:
            print(f"Fehler beim Zugriff auf die Moduldaten: {e}")
        except Exception as e:
            print(f"Unerwarteter Fehler beim Laden der Moduldaten: {e}")

    def __str__(self):
        """
        Gibt eine textuelle Darstellung des Moduls zurück.
        """
        if self.modul_name is None:
            return f"Modul mit Code {self.modul_code} wurde noch nicht geladen."
        return (f"Modul: {self.modul_name} (Code: {self.modul_code}), "
                f"Credits: {self.credits}, Tutor: {self.tutor}, Prüfungsform: {self.pruefungsform}")


# In[ ]:




