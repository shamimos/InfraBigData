import requests
import json
import sqlite3
import pandas as pd
import os

class Ingesta:
    def __init__(self):
        self.api_url = "https://api.nobelprize.org/2.1/laureates"
        database_dir = 'src/static/db'
        database_path = f"{database_dir}/nobel_laureates.db"

        # Crear el directorio si no existe
        if not os.path.exists(database_dir):
            os.makedirs(database_dir)

        # Conectar a la base de datos
        self.conn = sqlite3.connect(database_path)
        self.cursor = self.conn.cursor()
        self.setup_tables()

    def setup_tables(self):
        try:
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS laureates (
                id INTEGER PRIMARY KEY,
                fullName TEXT, 
                gender TEXT,
                birthdate TEXT,
                birthplace TEXT,
                deathdate TEXT,
                deathplace TEXT)       
            ''')
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS nobel_prizes (
                prize_id INTEGER PRIMARY KEY AUTOINCREMENT,
                laureate_id INTEGER,
                awardYear INTEGER,
                category TEXT,
                motivation TEXT,
                prizeAmount INTEGER,
                prizeAmountAdjusted INTEGER,
                FOREIGN KEY (laureate_id) REFERENCES laureates (id))
            ''')
            self.conn.commit()
            print("Tables created successfully.")
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")


    def get_data(self):
        response = requests.get(self.api_url)
        if response.status_code == 200:
            data = response.json()
            with open('nobel_laureates.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
                print('Archivo guardado correctamente.')
        else:
            print('Error en la solicitud, detalles:', response.text)
            data = None
        return data

    def load_data(self, filename):
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)

    def insert_data(self, data):
        for laureate in data.get('laureates', []):
            laureate_id = laureate['id']
            fullName = laureate['fullName']['en']
            gender = laureate.get('gender')
            birthdate = laureate.get('birth', {}).get('date')
            birthplace = laureate.get('birth', {}).get('place', {}).get('city', {}).get('en')
            deathdate = laureate.get('death', {}).get('date')
            deathplace = laureate.get('death', {}).get('place', {}).get('city', {}).get('en')

            self.cursor.execute('''
                INSERT INTO laureates (id, fullName, gender, birthdate, birthplace, deathdate, deathplace)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (laureate_id, fullName, gender, birthdate, birthplace, deathdate, deathplace))

            for prize in laureate.get('nobelPrizes', []):
                awardYear = prize.get('awardYear')
                category = prize.get('category', {}).get('en', 'Unknown')
                motivation = prize.get('motivation', {}).get('en', '')
                prizeAmount = prize.get('prizeAmount', 0)
                prizeAmountAdjusted = prize.get('prizeAmountAdjusted', 0)
                self.cursor.execute('''
                INSERT INTO nobel_prizes (laureate_id, awardYear, category, motivation, prizeAmount, prizeAmountAdjusted)
                VALUES (?, ?, ?, ?, ?, ?)
                ''', (laureate_id, awardYear, category, motivation, prizeAmount, prizeAmountAdjusted))
        self.conn.commit()
        print('Datos insertados correctamente.')

    def perform_audit(self):
        audit_dir = 'src/static/auditoria'
        audit_file = f"{audit_dir}/auditoria.txt"

        # Crear el directorio si no existe
        if not os.path.exists(audit_dir):
           os.makedirs(audit_dir)

        df_db = pd.read_sql_query("SELECT * FROM laureates", self.conn)
    
        # Cargar datos desde el archivo JSON
        data_json = self.load_data('nobel_laureates.json')
        df_json = pd.json_normalize(data_json['laureates'])  # Aplanar el JSON en un DataFrame
        
        # Asegurarse de que los ID son enteros para una comparación precisa
        df_db['id'] = df_db['id'].astype(int)
        df_json['id'] = df_json['id'].astype(int)
        
        # Comparar los registros en la base de datos con los obtenidos de la API
        db_ids = set(df_db['id'])
        json_ids = set(df_json['id'])
        
        # Identificar diferencias
        missing_in_db = json_ids - db_ids
        extra_in_db = db_ids - json_ids
    
        # Crear un informe de auditoría
        with open(audit_file, 'w') as file:
            file.write('Reporte de Auditoría\n')
            file.write(f'Total registros en DB: {len(df_db)}\n')
            file.write(f'Total registros en JSON: {len(df_json)}\n')
            file.write(f'Registros en JSON no en DB: {missing_in_db}\n')
            file.write(f'Registros en DB no en JSON: {extra_in_db}\n')

        print('Auditoría completada. Revisa el archivo de auditoría para más detalles.')

    def close_connection(self):
        self.conn.close()
        print('Conexión cerrada correctamente.')


if __name__ == '__main__':
    ingesta = Ingesta()
    data = ingesta.get_data()
    if data:
        laureate_data = ingesta.load_data('nobel_laureates.json')
        ingesta.insert_data(laureate_data)
        ingesta.perform_audit()
    ingesta.close_connection()