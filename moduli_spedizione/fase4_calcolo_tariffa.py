import json
import os

def calcolo_tariffa(dati_spedizione, file_listini, codice_listino):
    """
    Calcola la tariffa della spedizione in base al servizio selezionato, alla zona e al peso.
    Ora restituisce anche il codice_listino usato.
    """
    servizio = dati_spedizione["servizio"]
    zona_riferimento = dati_spedizione["zona_riferimento"]
    tipologia = dati_spedizione["tipologia"]  # DOCS o PKG
    # print("DEBUG - dati_spedizione ricevuti in fase 4:", dati_spedizione)
    peso_tassato = dati_spedizione["peso_tassato"]

    # Controllo se il file esiste
    if not os.path.exists(file_listini):
        print(f"❌ Il file listino {file_listini} non esiste.")
        return None

    # Carica il listino prezzi
    try:
        with open(file_listini, "r", encoding="utf-8") as f:
            listino_data = json.load(f)  # Carica tutto il JSON
    except Exception as e:
        print(f"❌ ERRORE: Il file listino {file_listini} non è leggibile! Errore: {e}")
        return None

    # Se il file ha "tariffe", usa la logica di espresso_cash.json
    if "tariffe" in listino_data:
        listino_tariffe = listino_data["tariffe"]
    else:
        print(f"❌ Struttura del listino {file_listini} non riconosciuta.")
        return None

    # Verifica se la zona esiste nel listino
    if zona_riferimento not in listino_tariffe:
        print(f"❌ Nessuna tariffa trovata per la zona {zona_riferimento} in {file_listini}")
        return None

    tariffe_zona = listino_tariffe[zona_riferimento]

    # Verifica se la tipologia (DOCS o PKG) esiste nel listino per quella zona
    if tipologia not in tariffe_zona:
        print(f"❌ Nessuna tariffa trovata per {tipologia} in zona {zona_riferimento}")
        return None

    tariffe_tipologia = tariffe_zona[tipologia]

    # Trova la tariffa più vicina per il peso tassato
    pesi_disponibili = sorted(map(float, tariffe_tipologia.keys()))
    peso_selezionato = None

    for p in pesi_disponibili:
        if peso_tassato <= p:
            peso_selezionato = str(p)
            break

    if not peso_selezionato:
        print(f"❌ Nessuna tariffa per {tipologia} con peso {peso_tassato} kg in zona {zona_riferimento}")
        return None

    tariffa_finale = tariffe_tipologia[peso_selezionato]["tariffa_finale"]

    # print(f"📦 Servizio {servizio} - Peso Tassato {peso_tassato} kg - 💰 Tariffa € {tariffa_finale:.2f} - ( Listino {codice_listino} )")

    return {
        "servizio": servizio,
        "tariffa": tariffa_finale,
        "codice_listino": codice_listino,
        "peso_tassato": peso_tassato  # ✅ Aggiunge il peso tassato
    }
