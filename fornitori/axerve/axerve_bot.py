import requests
import json
import pandas as pd
from datetime import datetime
import os
from dotenv import load_dotenv

# Carica le variabili d'ambiente dal file .env
load_dotenv()

class AxerveBot:
    def __init__(self):
        self.api_key = os.getenv("AXERVE_API_KEY")
        self.api_url = os.getenv("AXERVE_API_URL")
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def test_connection(self):
        """Testa la connessione con le API di Axerve"""
        try:
            response = requests.get(f"{self.api_url}/status", headers=self.headers)
            response.raise_for_status()
            return {"success": True, "message": "Connessione riuscita", "data": response.json()}
        except requests.exceptions.RequestException as e:
            return {"success": False, "message": f"Errore di connessione: {str(e)}"}
    
    def create_payment_link(self, amount, description, customer_email=None, customer_name=None, expiry_days=7):
        """
        Crea un link di pagamento tramite API Axerve
        
        Parameters:
        amount (float): Importo da pagare
        description (str): Descrizione della transazione
        customer_email (str, optional): Email del cliente
        customer_name (str, optional): Nome del cliente
        expiry_days (int, optional): Giorni di validità del link
        
        Returns:
        dict: Risposta contenente il link di pagamento e i dettagli della richiesta
        """
        payload = {
            "amount": amount,
            "currency": "EUR",
            "description": description,
            "expiry_date": (datetime.now() + pd.Timedelta(days=expiry_days)).strftime("%Y-%m-%d"),
            "notify_url": os.getenv("NOTIFY_URL", ""),
            "redirect_url": os.getenv("REDIRECT_URL", "")
        }
        
        if customer_email:
            payload["customer_email"] = customer_email
        
        if customer_name:
            payload["customer_name"] = customer_name
        
        try:
            response = requests.post(f"{self.api_url}/payment-links", 
                                    headers=self.headers, 
                                    json=payload)
            response.raise_for_status()
            return {"success": True, "data": response.json()}
        except requests.exceptions.RequestException as e:
            return {"success": False, "message": f"Errore nella creazione del link di pagamento: {str(e)}"}

    def send_payment_link(self, payment_link_id, send_method="email", recipient=None):
        """
        Invia un link di pagamento già creato
        
        Parameters:
        payment_link_id (str): ID del link di pagamento
        send_method (str): Metodo di invio (email, sms, whatsapp)
        recipient (str): Indirizzo email o numero di telefono del destinatario
        
        Returns:
        dict: Risposta contenente lo stato dell'invio
        """
        payload = {
            "send_method": send_method,
            "recipient": recipient
        }
        
        try:
            response = requests.post(f"{self.api_url}/payment-links/{payment_link_id}/send", 
                                    headers=self.headers, 
                                    json=payload)
            response.raise_for_status()
            return {"success": True, "data": response.json()}
        except requests.exceptions.RequestException as e:
            return {"success": False, "message": f"Errore nell'invio del link di pagamento: {str(e)}"}
    
    def get_transactions(self, start_date=None, end_date=None, status=None, transaction_type=None, page=1, limit=100):
        """
        Recupera l'elenco delle transazioni
        
        Parameters:
        start_date (str, optional): Data di inizio (formato YYYY-MM-DD)
        end_date (str, optional): Data di fine (formato YYYY-MM-DD)
        status (str, optional): Stato delle transazioni (completed, failed, pending)
        transaction_type (str, optional): Tipo di transazione (pos, paybylink)
        page (int, optional): Numero di pagina
        limit (int, optional): Numero di risultati per pagina
        
        Returns:
        dict: Risposta contenente l'elenco delle transazioni
        """
        params = {
            "page": page,
            "limit": limit
        }
        
        if start_date:
            params["start_date"] = start_date
        
        if end_date:
            params["end_date"] = end_date
        
        if status:
            params["status"] = status
        
        if transaction_type:
            params["type"] = transaction_type
        
        try:
            response = requests.get(f"{self.api_url}/transactions", 
                                headers=self.headers, 
                                params=params)
            response.raise_for_status()
            return {"success": True, "data": response.json()}
        except requests.exceptions.RequestException as e:
            return {"success": False, "message": f"Errore nel recupero delle transazioni: {str(e)}"}

    def get_transaction_details(self, transaction_id):
        """
        Recupera i dettagli di una specifica transazione
        
        Parameters:
        transaction_id (str): ID della transazione
        
        Returns:
        dict: Risposta contenente i dettagli della transazione
        """
        try:
            response = requests.get(f"{self.api_url}/transactions/{transaction_id}", 
                                headers=self.headers)
            response.raise_for_status()
            return {"success": True, "data": response.json()}
        except requests.exceptions.RequestException as e:
            return {"success": False, "message": f"Errore nel recupero dei dettagli della transazione: {str(e)}"}

    def export_transactions_to_csv(self, transactions_data, filename="transactions.csv"):
        """
        Esporta le transazioni in un file CSV
        
        Parameters:
        transactions_data (dict): Dati delle transazioni
        filename (str, optional): Nome del file CSV da creare
        
        Returns:
        dict: Stato dell'esportazione
        """
        try:
            df = pd.DataFrame(transactions_data["data"]["transactions"])
            df.to_csv(filename, index=False)
            return {"success": True, "message": f"Transazioni esportate con successo in {filename}"}
        except Exception as e:
            return {"success": False, "message": f"Errore nell'esportazione delle transazioni: {str(e)}"}


def main():
    """Funzione principale per l'interfaccia CLI"""
    load_dotenv()
    bot = AxerveBot()
    
    print("=== Bot Axerve ===")
    print("1. Crea un link di pagamento")
    print("2. Visualizza le transazioni")
    print("3. Esporta transazioni in CSV")
    print("4. Esci")
    
    choice = input("Seleziona un'opzione: ")
    
    if choice == "1":
        amount = float(input("Importo: "))
        description = input("Descrizione: ")
        customer_email = input("Email cliente (opzionale): ") or None
        customer_name = input("Nome cliente (opzionale): ") or None
        
        result = bot.create_payment_link(amount, description, customer_email, customer_name)
        if result["success"]:
            print(f"Link di pagamento creato: {result['data']['payment_url']}")
            
            send = input("Vuoi inviare il link via email? (s/n): ")
            if send.lower() == "s":
                email = input("Email destinatario: ")
                send_result = bot.send_payment_link(result["data"]["payment_link_id"], "email", email)
                if send_result["success"]:
                    print("Link inviato con successo!")
                else:
                    print(send_result["message"])
        else:
            print(result["message"])
            
    elif choice == "2":
        start_date = input("Data inizio (YYYY-MM-DD, opzionale): ") or None
        end_date = input("Data fine (YYYY-MM-DD, opzionale): ") or None
        status = input("Stato (completed, failed, pending, opzionale): ") or None
        transaction_type = input("Tipo (pos, paybylink, opzionale): ") or None
        
        result = bot.get_transactions(start_date, end_date, status, transaction_type)
        if result["success"]:
            transactions = result["data"]["transactions"]
            print(f"\nTrovate {len(transactions)} transazioni:\n")
            for i, tx in enumerate(transactions):
                print(f"{i+1}. {tx['date']} - {tx['amount']} EUR - {tx['status']} - {tx['type']}")
        else:
            print(result["message"])
            
    elif choice == "3":
        start_date = input("Data inizio (YYYY-MM-DD, opzionale): ") or None
        end_date = input("Data fine (YYYY-MM-DD, opzionale): ") or None
        filename = input("Nome file (default: transactions.csv): ") or "transactions.csv"
        
        result = bot.get_transactions(start_date, end_date)
        if result["success"]:
            export_result = bot.export_transactions_to_csv(result, filename)
            print(export_result["message"])
        else:
            print(result["message"])
            
    elif choice == "4":
        print("Arrivederci!")
        return
    else:
        print("Opzione non valida")
    
    # Richiama la funzione principale per continuare
    main()

if __name__ == "__main__":
    main()