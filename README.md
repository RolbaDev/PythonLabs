# ✅ Task Manager CLI

Prosta i funkcjonalna aplikacja do zarządzania zadaniami w terminalu. Każda lista zadań zapisywana jest jako osobny plik `.json`, dzięki czemu możesz tworzyć, przełączać i usuwać różne zestawy zadań.

## ✨ Funkcjonalności

- Tworzenie wielu list zadań
- Dodawanie zadań z opisem
- Oznaczanie statusu zadania: `Started`, `Paused`, `Completed`
- Przeglądanie aktywnych i przeterminowanych zadań (TTL = 7 dni)
- Usuwanie zadań oraz całych list
- Kolorowe oznaczenia dla lepszej czytelności w terminalu

---

## ⚙️ Użycie

Każdą komendę wywołuje się za pomocą:

```bash
python Manager.py <komenda> [opcje]
```

---

## 🧾 Dostępne komendy

### 📌 Dodawanie zadania

```bash
python Manager.py add_task "Nazwa zadania" "Opis zadania" --list "moja_lista"
```

Dodaje nowe zadanie do podanej listy. Jeśli lista nie istnieje, zadanie nie zostanie dodane.

---

### 📋 Wyświetlanie zadań

```bash
python Manager.py list_tasks --list "moja_lista"
```

Dodatkowy filtr po statusie:

```bash
python Manager.py list_tasks --status 1 --list "moja_lista"
```

- `1` – Started
- `2` – Paused
- `3` – Completed

Zadania przeterminowane (starsze niż 7 dni) są wyświetlane osobno.

---

### 🛠️ Aktualizacja statusu zadania

```bash
python Manager.py update_status <task_id> <status_id> --list "moja_lista"
```

Przykład:

```bash
python Manager.py update_status 2 3 --list "moja_lista"
```

---

### 🗑️ Usuwanie zadania

```bash
python Manager.py remove_task <task_id> --list "moja_lista"
```

Usuwa zadanie z podanej listy.

---

### 🧼 Usuwanie całej listy

```bash
python Manager.py delete_list "nazwa_listy"
```

---

### 🆕 Tworzenie nowej listy

```bash
python Manager.py add_list "nazwa_listy"
```

---

### 📂 Lista wszystkich dostępnych list

```bash
python Manager.py lists
```

---

## 🎨 Kolory statusów

- 🟡 **Started** – żółty
- 🔴 **Paused** – czerwony
- 🟢 **Completed** – zielony
- ⏳ **Outdated** – żółty + informacja o ile dni spóźnione

---

## 📁 .gitignore (przykład)

Aby nie dodawać plików `__pycache__` oraz `.json` do repozytorium:

```
__pycache__/
*.json
```

---

## 📦 Wymagania

- Python 3.6+
- `termcolor`  
Zainstaluj komendą:

```bash
pip install termcolor
```

---

## 📣 Autor

Dominik Rolbiecki
