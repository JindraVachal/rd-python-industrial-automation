markdown
# ETL Proces: Načítání senzorických dat do MariaDB (Docker)

Tento projekt načítá data z 6ks senzorů PT100 z CSV souboru `Data1.csv` (formát CSV) a ukládá je do SQL databáze MariaDB. Řešení běží v izolovaných kontejnerech pomocí **Docker Compose**. Každá část projektu/kódu je okomentována v českém jazyce.

## 📋 Popis řešení
Projekt se skládá ze dvou hlavních částí (služeb):
1.  **MariaDB Server (`db_server`):** Databázové úložiště, které uchovává data trvale díky Docker Volumes. Obsahuje mechanismus `healthcheck`, který hlídá, zda je DB připravena k přijímání dat.
2.  **Python ETL Aplikace (`Load_csv_Data1.py`):** Vlastní skript, který:
    *   Načte data ze souboru `Data1.csv` (kódování UTF-16, oddělovač mezer).
    *   Provede transformaci (spojení data a času do formátu Timestamp).
    *   Očistí data (vynechání nefunkčních snímačů V5 a V6).
    *   Nahraje data do DB pomocí knihovny `SQLAlchemy`.

## 🛠️ Technologie
*   **Docker & Docker Compose** (kontejnerizace)
*   **Python 3.12-slim** (skriptovací jazyk)
*   **Pandas** (zpracování dat)
*   **MariaDB** (SQL databáze)

## 🚀 Jak spustit projekt
1. **Příprava:** Ujisti se, že máš nainstalovaný Docker a ve složce `src/` máš soubor `Data1.csv`.
2. **Spuštění:** V kořenové složce projektu zadej do terminálu:
   ```bash
   docker-compose up --build

