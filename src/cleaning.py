import pandas as pd
import sqlite3
import os

class Cleaning:
    def __init__(self, db_path='src/static/db/nobel_laureates.db'):
        self.database_path = db_path
        self.conn = None
        self.cursor = None
        self.connect_db()

    def connect_db(self):
        """Establecer conexión a la base de datos."""
        try:
            self.conn = sqlite3.connect(self.database_path)
            self.cursor = self.conn.cursor()
            print("Conexión a la base de datos establecida correctamente.")
        except sqlite3.Error as e:
            print(f"Error al conectar a la base de datos: {e}")

    def load_data(self, table_name):
        """Cargar datos desde una tabla especificada."""
        try:
            if self.conn is None:
                self.connect_db()
            query = f"SELECT * FROM {table_name}"
            df = pd.read_sql_query(query, self.conn)
            print(df.head())
            print(f"Dimensiones del DataFrame: {df.shape}")
            print(f"Columnas del DataFrame: {df.columns}")
            print(f"Tipos de datos de las columnas:\n{df.dtypes}")
            print(f"Resumen estadístico para columnas numéricas: {df.describe()}")
            print("Columnas con valores nulos:", df.isnull().sum())
            print("Número de registros duplicados:", df.duplicated().sum())
            return df
        except sqlite3.Error as e:
            print(f"Error al realizar consulta SQL: {e}")
        finally:
            if self.conn:
                self.cursor.close()
                self.conn.close()
                print("Conexión a la base de datos cerrada.")

    def validate_datetime_types(self, df, date_columns):
        """Validar y convertir tipos de datos de fechas."""
        try:
            # date_columns = ['birthdate', 'deathdate']  # Asumiendo que quieres validar fechas
            for col in date_columns:
                if col in df.columns:
                    df[col] = pd.to_datetime(df[col], format='%Y-%m-%d', errors='coerce')   # Convertir a tipo fecha
                else:
                    print(f"Advertencia: La columna {col} no se encontró en el DataFrame.")
            return df
        except Exception as e:
            print(f"Error al validar tipos de datos: {e}")

    def delete_null_values(self, df):
        """Eliminar filas con valores nulos en columnas específicas."""
        for col in df.columns:
            if df[col].isnull().sum() > 0:
                df = df.dropna(subset=[col])
                print(f"Valores nulos eliminados de la columna {col}.")
        return df
                
    def save_to_csv(self, df, filename):
        """Guardar el DataFrame limpio en un archivo CSV en una ubicación específica."""
        directory = 'src/static/xlsx'
        os.makedirs(directory, exist_ok=True)  # Crea el directorio si no existe
        filepath = os.path.join(directory, filename)
        df.to_csv(filepath, index=False, encoding='utf-8')
        print(f"DataFrame guardado correctamente en {filepath}.")
    
    def report_cleaning(self, df, filename):

        directory = 'src/static/auditoria'
        os.makedirs(directory, exist_ok=True) # Crea el directorio si no existe
        filepath = os.path.join(directory, filename)

        with open(filepath, 'a') as file:  # Cambia 'w' a 'a' para añadir al archivo existente
            # Estado inicial del DataFrame
            file.write("Estado inicial del DataFrame:\n")
            file.write(f"Dimensiones iniciales: {df.shape}\n")
            file.write(f"Valores nulos iniciales por columna:\n{df.isnull().sum().to_string()}\n")
            file.write(f"Registros duplicados iniciales: {df.duplicated().sum()}\n\n")
            
            # Limpieza de datos
            inicial_nulos = df.isnull().sum()
            inicial_duplicados = df.duplicated().sum()
            # Asigna tus métodos de limpieza aquí, por ejemplo:
            df.drop_duplicates(inplace=True)
            df.dropna(inplace=True)
            
            # Estado después de la limpieza
            file.write("Estado después de la limpieza:\n")
            file.write(f"Dimensiones finales: {df.shape}\n")
            file.write(f"Valores nulos finales por columna:\n{df.isnull().sum().to_string()}\n")
            file.write(f"Registros duplicados finales: {df.duplicated().sum()}\n\n")
            
            # Impacto de la limpieza
            file.write("Impacto de las operaciones de limpieza:\n")
            file.write(f"Filas eliminadas: {inicial_nulos.sum() - df.isnull().sum().sum()} por nulos, {inicial_duplicados - df.duplicated().sum()} por duplicados\n")

    def close_db(self):
        """Cerrar la conexión a la base de datos si está abierta."""
        if self.conn:
            self.cursor.close()
            self.conn.close()
            print("Conexión a la base de datos cerrada correctamente.")

# Uso de la clase
cleaning_laureates = Cleaning()
df_laureates = cleaning_laureates.load_data('laureates')
df_laureates_validated = cleaning_laureates.validate_datetime_types(df_laureates, ['birthdate', 'deathdate'])
df_laureates_clean = cleaning_laureates.delete_null_values(df_laureates_validated)
cleaning_laureates.save_to_csv(df_laureates_clean, 'cleaned_data_laureates.csv')
cleaning_laureates.report_cleaning(df_laureates, 'auditoria_laureates.txt')

cleaning_nobel_prizes = Cleaning()
df_nobelPrizes = cleaning_nobel_prizes.load_data('nobel_prizes')
df_nobelPrizes_clean = cleaning_nobel_prizes.delete_null_values(df_nobelPrizes)
cleaning_nobel_prizes.save_to_csv(df_nobelPrizes_clean, 'cleaned_data_nobel_prizes.csv')
cleaning_nobel_prizes.report_cleaning(df_nobelPrizes, 'auditoria_nobel_prizes.txt')
