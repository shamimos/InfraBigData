import pandas as pd
import os

class EnrichedData:
    def __init__(self, csv_path='src/static/xlsx/cleaned_data_nobel_prizes.csv', csv='src/static/xlsx/cleaned_data_laureates.csv', log='enrichment_report.txt'):
        self.csv_path = csv_path
        self.csv = csv
        self.log = log
        self.audit_dir = 'src/static/auditoria'
        self.conn = None
        self.cursor = None
    
    def load_csv_data(self, path):
        """Cargar datos desde un archivo CSV especificado por la ruta."""
        try:
            df = pd.read_csv(path)
            print(f"Datos cargados correctamente desde {path}")
            return df
        except FileNotFoundError:
            print(f"Error: El archivo no fue encontrado en {path}")
        except Exception as e:
            print(f"Error al cargar el archivo CSV: {e}")
    
    def merge_dataframes(self, df1, df2, left_on='laureate_id', right_on='id'):
        """Unir dos DataFrames en base a una columna en común."""
        try:
            merged_df = pd.merge(df1, df2, left_on=left_on, right_on=right_on, how='inner')
            print("DataFrames unidos correctamente.")
            return merged_df
        except Exception as e:
            print(f"Error al unir DataFrames: {e}")
    
    def save_to_csv(self, df, output_path):
        """Guardar DataFrame en un archivo CSV."""
        try:
            df.to_csv(output_path, index=False)
            print(f"DataFrame guardado en {output_path}")
        except Exception as e:
            print(f"Error al guardar el archivo CSV: {e}")
    
    def create_log (self, path_laureates, path_nobel_prizes):   
        df_laureates = pd.read_csv(path_laureates)
        total_filas_laureates = df_laureates.shape[0]

        df_nobel_prizes = pd.read_csv(path_nobel_prizes)
        total_filas_nobel_prizes = df_nobel_prizes.shape[0]

        df_merge = self.merge_dataframes(df_laureates, df_nobel_prizes, left_on='laureate_id', right_on='id')
        total_filas_merge = df_merge.shape[0] 

        resultado_outer = pd.merge(df_laureates, df_nobel_prizes, left_on="laureate_id", right_on="id", how="outer", indicator=True)
        total_diferentes_merge = resultado_outer[resultado_outer['_merge'] != 'both'].shape[0]

        audit_file = f"{self.audit_dir}/{self.log}"

        with open(audit_file, 'w') as f:
            f.write(f'Total registros en nobel_prizes: {total_filas_nobel_prizes}\n')
            f.write(f'Total registros en laureates: {total_filas_laureates}\n')
            f.write(f'Total registros coincidentes: {total_filas_merge}\n')
            f.write(f'Total registros diferentes: {total_diferentes_merge}\n')
            f.write('Auditoría completada.\n')
            print('Auditoría completada.')

# Ejemplo de uso:
data_manager = EnrichedData()

# Cargar DataFrames
df1 = data_manager.load_csv_data(data_manager.csv_path)
df2 = data_manager.load_csv_data(data_manager.csv)

# Merge DataFrames
if df1 is not None and df2 is not None:
    merged_df = data_manager.merge_dataframes(df1, df2, left_on='laureate_id', right_on='id')  # Reemplazar 'common_column_name' con el nombre real de la columna

    # Guardar el DataFrame resultante
    if merged_df is not None:
        data_manager.save_to_csv(merged_df, 'src/static/xlsx/enriched_data.csv')
        data_manager.create_log(data_manager.csv_path, data_manager.csv)
