# Il backend in python flask

## Setup
> Attenzione! Python ha disattivato l'installazione globale dei pacchetti.

Per poter funzionare dovete:

### 1. Creare un ambiente virtuale
Eseguire il comando nella cartella di root del progetto

```
python3 -m venv rizik0
```

e poi per attivare l'ambiente virtuale

```
source rizik0/bin/activate
```

### 2. Installare i pacchetti

```
python3 -m pip install -r requirements.txt
```

---

![flow chart](https://github.com/rizik0/rizik0-backend/assets/112891194/576e6457-89b6-4a5e-aa4d-d453ebb33212)

Account su SQL
## Creare il database sqlite da file sql:
```
cat database.sql | sqlite3 database.db
```
## Leggere il database da terminale
```
sqlite3 database.db

sqlite> select * from players;
```

## Connettersi al database da python:
```
sqliteConnection = sqlite3.connect('database.db')
cursor = sqliteConnection.cursor()
```

