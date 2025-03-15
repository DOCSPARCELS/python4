import requests

# 🔹 Mappatura per abbreviare i nomi delle province (tutto in minuscolo)
conversione_province = {
    "città metropolitana di roma capitale": "Roma",
    "città metropolitana di milano": "Milano",
    "città metropolitana di napoli": "Napoli",
    "città metropolitana di torino": "Torino",
    "città metropolitana di genova": "Genova",
    "città metropolitana di bologna": "Bologna",
    "città metropolitana di cagliari": "Cagliari",
    "città metropolitana di venezia": "Venezia",
    "provincia di firenze": "Firenze",
    "provincia di venezia": "Venezia",
    "provincia di bari": "Bari",
    "provincia di palermo": "Palermo",
    "provincia di messina": "Messina",
    "provincia di verona": "Verona",
    "provincia di padova": "Padova",
    "provincia di belluno": "Belluno",
}

# 🔹 Funzione per ottenere la provincia dalla città con Google API
def trova_provincia_google(citta, api_key):
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={citta},Italy&key={api_key}&language=it"
    response = requests.get(url)

    if response.status_code == 200:
        dati = response.json()
        if dati["status"] == "OK":
            for componente in dati["results"][0]["address_components"]:
                if "administrative_area_level_2" in componente["types"]:  # Provincia
                    provincia = componente["long_name"].lower()  # Converti in minuscolo
                    return conversione_province.get(provincia, componente["long_name"].title())  # Usa titolo se non mappata

    return "Provincia non trovata"  # Se Google non restituisce nulla
