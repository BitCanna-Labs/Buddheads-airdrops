#python3
# Get the list of STAR > BCNA > NEUTARO and iterate on BCNA address searching for delegations.
import json
import requests
from collections import defaultdict

# Cargar el fichero JSON
with open('converted-address.json', 'r') as file:
    data = json.load(file)

# Eliminar duplicados basándonos en el campo "bitcanna"
unique_data = {entry['bitcanna']: entry for entry in data}.values()

# Listas para almacenar los resultados
total_zero_list = []
total_non_zero_list = []

# Función para obtener el total de delegaciones
def obtener_total_delegaciones(bitcanna_address):
    url = f"https://lcd.bitcanna.io/cosmos/staking/v1beta1/delegations/{bitcanna_address}"
    response = requests.get(url)
    print(f"Checking {bitcanna_address}")
    if response.status_code == 200:
        json_response = response.json()
        total = int(json_response['pagination']['total'])
        return total
    else:
        print(f"Error al obtener datos para {bitcanna_address}: {response.status_code}")
        return None

# Iterar sobre los datos únicos y obtener el total de delegaciones
for entry in unique_data:
    bitcanna_address = entry['bitcanna']
    total = obtener_total_delegaciones(bitcanna_address)
    if total is not None:
        if total == 0:
            total_zero_list.append(bitcanna_address)
        else:
            total_non_zero_list.append(bitcanna_address)

# Imprimir los resultados
print("Total = 0:")
print(total_zero_list)
print("\nTotal > 0:")
print(total_non_zero_list)

# Guardar los resultados en ficheros JSON
with open('total_zero_list.json', 'w') as file:
    json.dump(total_zero_list, file)

with open('total_non_zero_list.json', 'w') as file:
    json.dump(total_non_zero_list, file)
