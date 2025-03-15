import sys
sys.path.append(".")  # Assicura che il path principale sia incluso
from google.geocoding import trova_provincia_google

GOOGLE_API_KEY = "AIzaSyBvihtyzRMyjD8AGYQ1_DSUEkDrNwcqHjs"

citta_test = ["Roma", "Milano", "Venezia", "Ischia", "Cortina d'Ampezzo", "San Marino"]

for citta in citta_test:
    provincia = trova_provincia_google(citta, GOOGLE_API_KEY)
    print(f"La provincia di {citta} è: {provincia}")
