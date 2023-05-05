import os
import hashlib
import sqlite3

# Die unterstützten Dateiformate
SUPPORTED_FORMATS = ['.jpg', '.jpeg', '.png', '.gif']

# Der Pfad zum Ordner, den du durchsuchen möchtest
DIRECTORY_TO_SEARCH = r'D:\#BACKUP\BILDER\4.Bilder_Neu_N900'

# Der Pfad zur Datenbank
DATABASE_PATH = 'picture.sqlite'


# Eine Funktion, die die Tabelle images erstellt
def create_table():
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE images (
            file_path TEXT NOT NULL,
            directory_path TEXT NOT NULL,
            hash_value TEXT NOT NULL
        )''')
        conn.commit()


# Eine Funktion, die den Hashwert eines Bildes berechnet
def calculate_hash(file_path):
    with open(file_path, 'rb') as f:
        file_bytes = f.read()
        return hashlib.sha256(file_bytes).hexdigest()


# Eine Funktion, die ein Bild in die Datenbank einfügt
def insert_into_database(file_path, hash_value):
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO images VALUES (?, ?, ?)', (file_path, os.path.dirname(file_path), hash_value))
        conn.commit()


# Eine Funktion, die alle Bilder im Verzeichnis durchsucht und die gefundenen Bilder in die Datenbank einfügt
def search_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.splitext(file_path)[1].lower() in SUPPORTED_FORMATS:
                hash_value = calculate_hash(file_path)
                insert_into_database(file_path, hash_value)


def find_duplicates():
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            'SELECT hash_value, GROUP_CONCAT(file_path, ", ") AS file_paths, directory_path FROM images GROUP BY hash_value HAVING COUNT(*) > 1')
        duplicates = cursor.fetchall()
        for hash_value, file_paths, directory_path in duplicates:
            print(
                f'Der Hashwert {hash_value} wurde in den folgenden Dateien gefunden: {file_paths} im Ordner {directory_path}')


if __name__ == '__main__':
    create_table()
    search_directory(DIRECTORY_TO_SEARCH)
    find_duplicates()
