import os

def generate_readme():
    """Genera automaticamente il README.md con la struttura delle cartelle e dei file."""
    project_name = "📦 Gestione Spedizioni"
    description = "Questo progetto gestisce **spedizioni, listini, zone, servizi e contatti** tramite file JSON e HTML."

    # Funzione per generare la struttura delle cartelle
    def generate_tree(directory, prefix=""):
        tree = ""
        items = sorted([i for i in os.listdir(directory) if i != ".git"])
        for index, item in enumerate(items):
            path = os.path.join(directory, item)
            connector = "├── " if index < len(items) - 1 else "└── "
            tree += f"{prefix}{connector}{item}\n"
            if os.path.isdir(path):
                tree += generate_tree(path, prefix + "│   " if index < len(items) - 1 else prefix + "    ")
        return tree

    # Genera la struttura delle cartelle partendo dalla directory corrente
    project_structure = generate_tree(os.getcwd())

    readme_content = f"""# {project_name}

## 📌 Descrizione
{description}

---

## 📂 Struttura delle Cartelle

{project_structure}


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
"""

    # Scrive il contenuto nel README.md
    with open("README.md", "w", encoding="utf-8") as readme_file:
        readme_file.write(readme_content)

    print("✅ README.md aggiornato con successo!")

# Esegue lo script
if __name__ == "__main__":
    generate_readme()
