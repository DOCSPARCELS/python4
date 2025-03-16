# 📦 Gestione Spedizioni

## 📌 Descrizione
Questo progetto gestisce **spedizioni, listini, zone, servizi e contatti** tramite file JSON e HTML.

---

## 📂 Struttura delle Cartelle

├── .DS_Store
├── .gitignore
├── config.json
├── contatti
│   └── contatti.json
├── error.log
├── fastapi_server.py
├── fornitori
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-313.pyc
│   │   └── gestione_fornitori.cpython-313.pyc
│   ├── aruba
│   │   └── __init__.py
│   ├── axerve
│   │   ├── __int__.py
│   │   └── login.py
│   ├── brt
│   │   └── __init__.py
│   ├── dhl
│   │   └── __init__.py
│   ├── dhl_cargo
│   │   └── __init__.py
│   ├── endex
│   │   ├── __init__.py
│   │   └── login.py
│   ├── fedex
│   │   └── __init__.py
│   ├── fedex_tnt
│   │   └── __init__.py
│   ├── gestione_fornitori.py
│   ├── globalservice
│   │   ├── .env
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   │   ├── __init__.cpython-313.pyc
│   │   │   └── login.cpython-313.pyc
│   │   ├── bot.py
│   │   ├── login.py
│   │   ├── preventivo_globalservice.py
│   │   ├── preventivo_globalservice_precompilato.py
│   │   └── selenium_provincia.py
│   ├── gls
│   │   └── __init__.py
│   ├── inpost
│   │   └── __init__.py
│   ├── mondospedizioni
│   │   ├── .env
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   │   ├── __init__.cpython-313.pyc
│   │   │   ├── avvia_preventivo_mondospedizioni.cpython-313.pyc
│   │   │   ├── bot.cpython-313.pyc
│   │   │   ├── documenti.cpython-313.pyc
│   │   │   ├── login.cpython-313.pyc
│   │   │   ├── pacchi.cpython-313.pyc
│   │   │   └── preventivo_mondospedizioni.cpython-313.pyc
│   │   ├── bot.py
│   │   ├── documenti.py
│   │   ├── login.py
│   │   ├── pacchi.py
│   │   ├── preventivo_mondospedizioni.py
│   │   └── test_mondospedizioni.py
│   ├── mypos
│   │   └── __init__.py
│   ├── packlink
│   │   ├── __init__.py
│   │   └── login.py
│   ├── poste
│   │   └── __init__.py
│   └── ups
│       └── __init__.py
├── google
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-313.pyc
│   │   └── geocoding.cpython-313.pyc
│   ├── geocoding.py
│   └── test_provincia.py
├── moduli_spedizione
│   ├── __pycache__
│   │   ├── fase1_spedizione.cpython-313.pyc
│   │   ├── fase2_determinazione_zona.cpython-313.pyc
│   │   ├── fase3_calcolo_peso.cpython-313.pyc
│   │   └── fase4_calcolo_tariffa.cpython-313.pyc
│   ├── calcolo_preventivo copy.py
│   ├── calcolo_preventivo.py
│   ├── fase1_spedizione.py
│   ├── fase2_determinazione_zona.py
│   ├── fase3_calcolo_peso.py
│   └── fase4_calcolo_tariffa.py
├── server.log
├── servizi_listini
│   ├── .DS_Store
│   ├── listini
│   │   ├── espresso_cash.json
│   │   ├── espresso_icc.json
│   │   ├── espresso_import_cash.json
│   │   ├── ore12_cash.json
│   │   ├── ore12_import_cash.json
│   │   ├── saver_cash.json
│   │   ├── standard_cash.json
│   │   └── standard_import_cash.json
│   ├── monitor_servizi_zone.py
│   ├── paesi
│   │   └── paesi.json
│   ├── province_italia.json
│   ├── servizi.html
│   ├── servizi.json
│   ├── servizi_zone.csv
│   ├── servizi_zone.json
│   └── zone
│       ├── province_italia.json
│       ├── zone.html
│       ├── zone.json
│       └── zone_cap_italia.json
└── update_readme.py



---

## ⚙️ **File Principali**
- **`config.json`** → Contiene le impostazioni generali del progetto.
- **`contatti.json`** → Elenco di clienti e fornitori con dettagli.
- **`servizi.json`** → Definizione dei servizi di spedizione.
- **`zone.json`** → Associazione paesi e zone di spedizione.
- **`listini/*.json`** → Listini tariffari per servizi standard e personalizzati.
- **`preventivo.py`** → (Da sviluppare) Script per calcolare i costi di spedizione.

---

## 🔧 **Futuri sviluppi**
✅ Strutturare meglio la cartella `spedizioni`.  
✅ Implementare script Python per elaborare dati JSON.  
✅ Collegare la gestione dei file con un database.  

---

## 📞 Contatti
Per qualsiasi informazione o aggiornamento sul progetto, contattami! 🚀
