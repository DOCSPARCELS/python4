# from fornitori.mondospedizioni.bot import ottieni_tariffe_mondospedizioni
# Aggiungi qui altri fornitori quando disponibili
# from fornitori.fedex.api import ottieni_tariffe_fedex
# from fornitori.dhl.api import ottieni_tariffe_dhl

def recupera_tariffe(dati_spedizione):
   """Chiama tutti i fornitori e restituisce un elenco di tariffe con formato uniforme"""
tariffe = []

    # ✅ Mondospedizioni
    # offerte_mondo = ottieni_tariffe_mondospedizioni(dati_spedizione)
    # for offerta in offerte_mondo:
    #   tariffe.append({
    #       "prezzo": offerta["prezzo"],
    #       "tempi": offerta["tempi"],
    #       "servizio": offerta.get("servizio", "N/D"),  # Se non presente, default "N/D"
    #       "corriere": offerta.get("corriere", "Mondospedizioni"),
    #       "fornitore": "Mondospedizioni"
    #   })

    # ✅ Esempio di un'API FedEx
    # offerte_fedex = ottieni_tariffe_fedex(dati_spedizione)
    # for offerta in offerte_fedex:
    #     tariffe.append({
    #         "prezzo": offerta["prezzo"],
    #         "tempi": offerta["tempi"],
    #         "servizio": offerta["servizio"],
    #         "corriere": "FedEx",  # Le API lo sanno già, quindi fisso
    #         "fornitore": "FedEx"
    #     })

#   return tariffe


