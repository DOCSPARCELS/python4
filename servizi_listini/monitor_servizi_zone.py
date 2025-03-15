import os
import json
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import pandas as pd

# Cartella principale
BASE_FOLDER = os.path.join(os.getcwd(), "servizi_listini")

# Percorsi corretti
SERVIZI_FILE = os.path.join(BASE_FOLDER, "servizi.json")
ZONE_FILE = os.path.join(BASE_FOLDER, "zone", "zone.json")
DATA_FOLDER = os.path.join(BASE_FOLDER, "listini")  # Dove si trovano i listini

# Percorso di output per `servizi_zone.json`
OUTPUT_FILE = os.path.join(BASE_FOLDER, "servizi_zone.json")

# Funzione per aggiornare la mappa servizi - listini - zone
def aggiorna_servizi_zone():
    file_paths = {f: os.path.join(DATA_FOLDER, f) for f in os.listdir(DATA_FOLDER) if f.endswith(".json") and f != "servizi.json"}
    
    # Caricare i servizi
    with open(SERVIZI_FILE, "r", encoding="utf-8") as f:
        servizi_data = json.load(f)
    
    servizi = {s["codice_servizio"]: s["nome_servizio"] for s in servizi_data["servizi"]}
    
    servizio_listino_zone_map = {}
    
    for file_path in file_paths.values():
        with open(file_path, "r", encoding="utf-8") as f:
            listino_data = json.load(f)
        
        codice_servizio = listino_data["codice_servizio"]
        codice_listino = listino_data["codice_listino"]
        
        if codice_servizio not in servizio_listino_zone_map:
            servizio_listino_zone_map[codice_servizio] = {}
        
        if codice_listino not in servizio_listino_zone_map[codice_servizio]:
            servizio_listino_zone_map[codice_servizio][codice_listino] = set()
        
        for zona in listino_data["tariffe"].keys():
            servizio_listino_zone_map[codice_servizio][codice_listino].add(zona)
    
    # Convertire in lista ordinata con campi corretti
    servizio_listino_zone = [
        {"codice_servizio": servizio, "nome_servizio": servizi.get(servizio, "Unknown"), "codice_listino": codice_listino, "Zone": sorted(list(zone), key=lambda x: (not x.startswith("ZIT"), x))}
        for servizio, listini in servizio_listino_zone_map.items()
        for codice_listino, zone in listini.items()
    ]
    
    # Salvare su file JSON
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(servizio_listino_zone, f, ensure_ascii=False, indent=4)
    
    print("[INFO] File servizi_zone.json aggiornato con successo!")

# Classe per il monitoraggio dei file
class FileMonitorHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith(".json") and "servizi_zone.json" not in event.src_path:
            print(f"[INFO] Rilevata modifica: {event.src_path}")
            aggiorna_servizi_zone()
    
    def on_created(self, event):
        if event.src_path.endswith(".json"):
            print(f"[INFO] Rilevata aggiunta file: {event.src_path}")
            aggiorna_servizi_zone()
    
    def on_deleted(self, event):
        if event.src_path.endswith(".json"):
            print(f"[INFO] Rilevata eliminazione file: {event.src_path}")
            aggiorna_servizi_zone()

# Avvio del monitoraggio dei file
def start_monitoring():
    event_handler = FileMonitorHandler()
    observer = Observer()
    observer.schedule(event_handler, DATA_FOLDER, recursive=False)
    observer.start()
    print("[INFO] Monitoraggio avviato...")
    
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

# Eseguire il monitoraggio
if __name__ == "__main__":
    aggiorna_servizi_zone()
    start_monitoring()