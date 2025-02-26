import pandas as pd
import json

def main():
    # Leer el archivo JSON
    with open('nobel_laureates.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Preparar un DataFrame vacío para concatenar todos los datos
    all_data = pd.DataFrame()

    # Recorrer cada clave en el JSON y agregar los datos al DataFrame si son adecuados
    for key, value in data.items():
        # Asegurarse de que los datos pueden ser un DataFrame
        if isinstance(value, list) and value and isinstance(value[0], dict):
            df = pd.DataFrame(value)
            df['category'] = key.capitalize()  # Añadir columna de categoría
            all_data = pd.concat([all_data, df], ignore_index=True)
        elif isinstance(value, dict):  # Si es un diccionario, convertir en DataFrame con un solo registro
            df = pd.DataFrame([value])
            df['category'] = key.capitalize()  # Añadir columna de categoría
            all_data = pd.concat([all_data, df], ignore_index=True)
        else:
            print(f"Los datos bajo la clave '{key}' no son adecuados para conversión a DataFrame y han sido omitidos.")

    # Guardar el DataFrame combinado en un archivo Excel
    if not all_data.empty:
        with pd.ExcelWriter('nobel_laureates.xlsx', engine='openpyxl') as writer:
            all_data.to_excel(writer, sheet_name='All Data', index=False)
        print("Archivo Excel 'nobel_laureates.xlsx' generado exitosamente en una sola hoja.")
    else:
        print("No se generó el archivo Excel porque no se encontraron datos adecuados.")

if __name__ == '__main__':
    main()
