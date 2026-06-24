# System Wyceny Nieruchomości (ML w Architekturze Mikroserwisów)

## Opis Projektu
Celem projektu jest stworzenie modularnej aplikacji opartej o silnik Machine Learning (Regresja Liniowa), która przewiduje ceny nieruchomości na podstawie parametrów takich jak metraż, liczba sypialni, stan umeblowania czy obecność klimatyzacji. Projekt wykorzystuje rzeczywisty zbiór danych rynkowych (Kaggle Housing Dataset), który został przetworzony, urealniony do warunków krajowych i zmigrowany do relacyjnej bazy danych SQLite.

Aplikacja została zaprojektowana w architekturze mikroserwisowej, rozdzielającej backend (silnik predykcyjny API) od warstwy prezentacji (interfejs użytkownika). Całość została w pełni skonteneryzowana za pomocą Dockera, dzięki czemu system uruchamia się w dowolnym środowisku.

## Struktura Projektu
Zgodnie z wymogami, logika działania została sztywno rozdzielona na niezależne warstwy (`data` | `model` | `app`):

```text
SUML-PROJEKT/
│
├── data/                   # [WARSTWA DATA]
│   └── data_processor.py   # Pobieranie danych z SQLite i podział na zbiory train/test
│
├── model/                  # [WARSTWA MODEL]
│   ├── trainer.py          # Skrypt trenujący model Regresji Liniowej
│   └── predictor.py        # Klasa odpowiedzialna za ładowanie i inferencję modelu
│
├── app/                    # [WARSTWA APP]
│   ├── api.py              # Serwer Backend API (FastAPI + Pydantic)
│   └── main.py             # Interfejs graficzny użytkownika Frontend (Streamlit)
│
├── datasets/               # Zasoby danych
│   ├── Housing.csv         # Surowe dane
│   └── housing.db          # Przetworzona baza danych SQLite
│
├── notebooks/              # Prace analityczne
│   └── data_preparation.ipynb # Notatnik Jupyter (Proces EDA, czyszczenie i transformacja)
│
├── saved_models/           # Przechowywanie wytrenowanych modeli
│   └── housing_model.joblib
│
├── Dockerfile              # Definicja obrazu bazowego systemu
├── docker-compose.yml      # Orkiestracja mikroserwisów (API + Frontend)
├── requirements.txt        # Lista zależności
└── README.md               # Dokumentacja projektu
```

## Architektura i Przepływ Danych

### Przygotowanie Danych
Surowy plik CSV z Kaggle został poddany czyszczeniu w notatniku Jupyter (folder notebooks/). Wartości tekstowe (yes/no) zmapowano na binarne 1/0, stan umeblowania zakodowano liczbowo, a ceny i metraż zostały urealnione. Gotowy zbiór wyeksportowano jako tabelę w bazie datasets/housing.db.

### Inicjalizacja i Trening
Podczas uruchamiania środowiska wywoływany jest moduł model.trainer. Pobiera on dane zapytaniem SQL z bazy SQLite za pośrednictwem klasy DataProcessor, trenuje algorytm LinearRegression i serializuje go do wydajnego formatu .joblib.

### Backend API (FastAPI)
Kontener backendowy uruchamia serwer Uvicorn i wystawia bezpieczny punkt końcowy (endpoint) /predict. Dane wejściowe przesyłane w formacie JSON są automatycznie walidowane przez bibliotekę Pydantic, co zapewnia stabilność działania silnika.

### Frontend (Streamlit)
Drugi, niezależny kontener serwuje aplikację webową dla użytkownika. Streamlit zbiera dane z formularzy i checkboxów, buduje obiekt JSON i wysyła zapytanie HTTP POST do kontenera API, prezentując użytkownikowi wynik wyceny w PLN.

---

## Instrukcja Uruchomienia

Aplikacja została w pełni skonteneryzowana. Uruchomienie nie wymaga wstępnej konfiguracji w systemie operacyjnym gospodarza, instalacji interpretera Python czy bibliotek lokalnych.

### Wymagania techniczne:
- Zainstalowane narzędzie Docker oraz wtyczka Docker Compose.

### Uruchomienie projektu:
Wpisz w terminalu (w głównym katalogu projektu) poniższą komendę:

```bash
docker-compose up --build
```
### Dostęp do usług:
-Interfejs użytkownika (Frontend): http://localhost:8501
-Dokumentacja techniczna (Backend API): http://localhost:8000/docs

### Zatrzymanie środowiska:
Aby wyłączyć aplikację i całkowicie wyczyścić zasoby kontenerów, użyj:
```bash
docker-compose down -v
```