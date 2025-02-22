import pandas as pd
import json

def main():
    # Leer el archivo JSON
    with open('data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Crear el archivo Excel con varias hojas
    with pd.ExcelWriter('output.xlsx', engine='openpyxl') as writer:
        for key in data:
             # Convertir cada clave del JSON a DataFrame y guardarlo en una hoja separada
            df = pd.DataFrame(data[key])
            df.to_excel(writer, sheet_name=key.capitalize(), index=False)

    print("Archivo Excel 'output.xlsx' generado exitosamente.")

if __name__ == '__main__':
    main()
