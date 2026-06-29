# System Wyceny Nieruchomości (ML w Architekturze Mikroserwisów)

## Opis Projektu
Celem projektu jest stworzenie modularnej aplikacji opartej o silnik Machine Learning (Regresja Liniowa), która przewiduje ceny nieruchomości na podstawie parametrów takich jak metraż, liczba sypialni, stan umeblowania czy obecność klimatyzacji. Projekt wykorzystuje rzeczywisty zbiór danych rynkowych (Kaggle Housing Dataset), który został przetworzony, urealniony do warunków krajowych i zmigrowany do relacyjnej bazy danych SQLite.

Aplikacja została zaprojektowana w architekturze mikroserwisowej, rozdzielającej backend (silnik predykcyjny API) od warstwy prezentacji (interfejs użytkownika). Całość została w pełni skonteneryzowana za pomocą Dockera, dzięki czemu system uruchamia się w dowolnym środowisku.

---

## Wymagania Systemowe

### Wymagania sprzętowe:
- Procesor: Wspierający wirtualizację (x86_64 lub ARM64, np. Apple Silicon).
- Pamięć RAM: Minimum 4 GB wolnej pamięci operacyjnej.
- Przestrzeń dyskowa: Około 2 GB na obrazy Docker oraz warstwy cache.

### Wymagania programowe (Zależności globalne):
- Docker Engine: Wersja 20.10.0 lub nowsza.
- Docker Compose: Wersja 2.0.0 lub nowsza.
- Python (tylko do rozwoju lokalnego poza Dockerem): Wersja 3.10.x.

---


## Struktura Projektu
Zgodnie z wymogami, logika działania została sztywno rozdzielona na niezależne warstwy (`data` | `model` | `app`):

```text
SUML-PROJEKT/
│
├── .github/                # Konfiguracja potoków automatyzacji
│   └── workflows/
│       └── pylint.yml      # Potok GitHub Actions (CI) dla testów statycznych
│  
├── data/                   # [WARSTWA DATA]
│   └── data_processor.py   # Pobieranie danych z SQLite i podział na zbiory train test
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

## Charakterystyka Zbioru Danych (Słownik Pojęć)

Model predykcyjny wykorzystuje 12 cech wejściowych (zmiennych niezależnych) do prognozowania ceny końcowej nieruchomości rynkowej.

### Zmienna docelowa (Target)

* **price** (`float`): Cena końcowa nieruchomości wyrażona w Polskich Złotych (PLN).

### Cechy wejściowe (Features)

| Nazwa zmiennej | Typ danych | Opis i dopuszczalny zakres wartości |
| :--- | :---: | :--- |
| **area** | `float` | Powierzchnia użytkowa nieruchomości przeliczona na metry kwadratowe ($m^2$). |
| **bedrooms** | `int` | Całkowita liczba sypialni w nieruchomości. |
| **bathrooms** | `int` | Całkowita liczba łazienek w nieruchomości. |
| **stories** | `int` | Liczba kondygnacji (pięter) budynku. |
| **mainroad** | `int` | Położenie nieruchomości bezpośrednio przy głównej drodze (1 = Tak, 0 = Nie). |
| **guestroom** | `int` | Obecność wydzielonego pokoju gościnnego (1 = Tak, 0 = Nie). |
| **basement** | `int` | Obecność użytkowej piwnicy (1 = Tak, 0 = Nie). |
| **hotwaterheating** | `int` | Obecność instalacji centralnego podgrzewania wody (1 = Tak, 0 = Nie). |
| **airconditioning** | `int` | Obecność dedykowanego systemu klimatyzacji (1 = Tak, 0 = Nie). |
| **parking** | `int` | Liczba dostępnych miejsc parkingowych na terenie posiadłości (zakres 0-3). |
| **prefarea** | `int` | Lokalizacja nieruchomości w dzielnicy powszechnie uznawanej za preferowaną (1 = Tak, 0 = Nie). |
| **furnishingstatus** | `int` | Standard umeblowania lokalu (0 = Brak wykończenia, 1 = Częściowe, 2 = Pełne umeblowanie). |


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
* **Interfejs użytkownika (Frontend):** Pod adresem `http://localhost:8501`
* **Dokumentacja techniczna (Backend API):** Pod adresem `http://localhost:8000/docs`

### Zatrzymanie środowiska:
Aby wyłączyć aplikację i całkowicie wyczyścić zasoby kontenerów, użyj:
```bash
docker-compose down -v
```

## Instrukcja Rozwoju Lokalnego (Poza Dockerem)

W celu edycji kodu, debugowania lub ponownego uruchomienia procesu analizy danych (EDA) w notatniku, należy przygotować lokalne środowisko wirtualne.

### 0. Tworzenie i aktywacja środowiska wirtualnego

Najpierw utwórz środowisko deweloperskie w głównym katalogu projektu:

```bash
python -m venv venv
# Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# Linux / macOS:
source venv/bin/activate
```
### 1. Instalacja zależności projektowych:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```
### 2. Uruchomienie notatnika Jupyter:
```bash
jupyter notebook notebooks/data_preparation.ipynb
```

## Jakość Kodu i Integracja Ciągła (CI)
* Projekt posiada zaimplementowany potok automatyzacji GitHub Actions, który przy każdym wypchnięciu kodu (git push) weryfikuje poprawność składniową oraz zgodność ze standardami PEP8.
* Narzędzie weryfikujące: Pylint
* Konfiguracja potoku: .github/workflows/pylint.yml
* Aktualny status statycznej analizy kodu: 10.00/10 (lub powyżej progu akceptowalności --fail-under=8.0)