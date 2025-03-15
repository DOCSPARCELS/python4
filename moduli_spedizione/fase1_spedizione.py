import json
import os

# Percorso corretto del file zone.json
json_path = os.path.join(os.path.dirname(__file__), "..", "servizi_listini", "zone", "zone.json")

# Controllo se il file esiste
if not os.path.exists(json_path):
    print(f"❌ ERRORE: Il file '{json_path}' non esiste! Assicurati di averlo posizionato correttamente.")
    exit()

# Apertura del file JSON
with open(json_path, "r", encoding="utf-8") as file:
    paesi_disponibili = json.load(file)

# Funzione per selezionare un paese
def seleziona_paese(messaggio, paesi_disponibili):
    """Permette all'utente di selezionare il paese digitando il nome."""
    print(f"\n🌎 {messaggio}")

    paesi_lista = list(paesi_disponibili.keys())  # Converti le chiavi del dizionario in una lista
    #print("💡 Paesi disponibili:", ", ".join(paesi_lista[:10]), "... (e altri)")

    while True:
        paese_input = input("🔍 Paese: ").strip().title()
        
        if paese_input in paesi_lista:
            return paese_input
        
        suggerimenti = [p for p in paesi_lista if paese_input.lower() in p.lower()]
        
        if suggerimenti:
            print("❓ Forse cercavi uno di questi?")
            for s in suggerimenti:
                print(f" - {s}")
        else:
            print("❌ Paese non trovato. Riprova.")



# ✅ Selezione del paese di partenza e destinazione
partenza_paese = seleziona_paese("Partenza", paesi_disponibili)
partenza_citta = input("🏙️  Città: ").strip()
partenza_cap = input("📍 CAP: ").strip()

destinazione_paese = seleziona_paese("Destinazione", paesi_disponibili)
destinazione_citta = input("🏙️  Città: ").strip()
destinazione_cap = input("📍 CAP: ").strip()

# ✅ Selezione della tipologia di spedizione
tipologia = input("📦 Tipologia DOCS/PKG: ").strip().upper()

colli = []
peso_totale = 0

if tipologia == "PKG":
    while True:
        try:
            numero_colli = int(input("📦 Numero colli: "))
            if numero_colli < 1:
                print("❌ ERRORE: Deve essere almeno 1!")
            else:
                break
        except ValueError:
            print("❌ ERRORE: Inserisci un numero valido!")
    
    for i in range(1, numero_colli + 1):
        print(f"\n🔹 Collo: {i}")

        while True:
            try:
                peso = float(input("⚖️  Peso kg: "))
                if peso <= 0:
                    print("❌ ERRORE: Il peso deve essere positivo!")
                else:
                    break
            except ValueError:
                print("❌ ERRORE: Inserisci un numero valido!")

        while True:
            try:
                lunghezza = float(input("📏 Lunghezza cm: "))
                if lunghezza <= 0:
                    print("❌ ERRORE: Deve essere un valore positivo!")
                else:
                    break
            except ValueError:
                print("❌ ERRORE: Inserisci un numero valido!")

        while True:
            try:
                larghezza = float(input("📏 Larghezza cm: "))
                if larghezza <= 0:
                    print("❌ ERRORE: Deve essere un valore positivo!")
                else:
                    break
            except ValueError:
                print("❌ ERRORE: Inserisci un numero valido!")

        while True:
            try:
                altezza = float(input("📏 Altezza cm: "))
                if altezza <= 0:
                    print("❌ ERRORE: Deve essere un valore positivo!")
                else:
                    break
            except ValueError:
                print("❌ ERRORE: Inserisci un numero valido!")

        colli.append({
            "peso": peso,
            "lunghezza": lunghezza,
            "larghezza": larghezza,
            "altezza": altezza
        })
        peso_totale += peso

else:
    numero_colli = 1
    while True:
        try:
            peso = float(input("⚖️ Peso documento (kg): "))
            if peso <= 0:
                print("❌ ERRORE: Il peso deve essere positivo!")
            else:
                break
        except ValueError:
            print("❌ ERRORE: Inserisci un numero valido!")

    lunghezza, larghezza, altezza = 29, 21, 1  # Dimensioni standard per documenti
    colli.append({
        "peso": peso,
        "lunghezza": lunghezza,
        "larghezza": larghezza,
        "altezza": altezza
    })
    peso_totale = peso

if partenza_paese.lower() == "italia" and destinazione_paese.lower() == "italia":
    tipo_listino = "EXPORT"
    zona_da_usare = "destinazione"
elif partenza_paese.lower() == "italia" and destinazione_paese.lower() != "italia":
    tipo_listino = "EXPORT"
    zona_da_usare = "destinazione"
elif partenza_paese.lower() != "italia" and destinazione_paese.lower() == "italia":
    tipo_listino = "IMPORT"
    zona_da_usare = "partenza"
else:
    print("\n❌ ERRORE: Spedizione tra due paesi esteri. Contattare assistenza.")
    exit()

# ✅ Calcolo del peso volumetrico totale
#    peso_volumetrico_totale = sum(
#   (collo["lunghezza"] * collo["larghezza"] * collo["altezza"]) / 5000  # Valore 5000 come esempio
#   for collo in colli
#)

#print(f"\n✅ Peso reale: {peso_totale} kg")
#print(f"✅ Peso volume: {peso_volumetrico_totale} kg")
#print(f"✅ Peso tassato: {max(peso_totale, peso_volumetrico_totale):.2f} kg")
print(f"🌍 Tipo di Spedizione: {tipo_listino}")
print(f"📍 Zona di riferimento: {zona_da_usare.upper()}")

# print("🔍 DEBUG: Dati raccolti dalla Fase 1:", {
#   "pacchi": colli,
#   "peso_totale": peso_totale,
#   "partenza_paese": partenza_paese,
#   "partenza_citta": partenza_citta,
#   "partenza_cap": partenza_cap,
#   "destinazione_paese": destinazione_paese,
#   "destinazione_citta": destinazione_citta,
#   "destinazione_cap": destinazione_cap,
#   "tipologia": tipologia,
#   "tipo_listino": tipo_listino,
#   "zona_da_usare": zona_da_usare
#})

# Questa funzione raccoglie tutti i dati della spedizione e li restituisce
def raccogli_dati_spedizione():
    return {
        "pacchi": colli,
        "peso_totale": peso_totale,
        "partenza_paese": partenza_paese,
        "partenza_citta": partenza_citta,
        "partenza_cap": partenza_cap,
        "destinazione_paese": destinazione_paese,
        "destinazione_citta": destinazione_citta,
        "destinazione_cap": destinazione_cap,
        "tipologia": tipologia,
        "tipo_listino": tipo_listino,
        "zona_da_usare": zona_da_usare
    }

# Esegui la funzione se il file viene eseguito come script
if __name__ == "__main__":
    dati_spedizione = raccogli_dati_spedizione()
    print(dati_spedizione)
