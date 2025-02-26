import requests
import json

# URL de la API de ejemplo
api_url = "https://api.nobelprize.org/2.1/laureates"
response = requests.get(api_url)

if response.status_code == 200:
    formatted_json = json.dumps(response.json(), indent=4)
    print('Solicitud exitosa:', formatted_json)
    with open('nobel_laureates.json', 'w', encoding='utf-8') as f:
        f.write(formatted_json)
        print('Archivo guardado correctamente.')
else:
    print('Error en la solicitud, detalles:', response.text)
