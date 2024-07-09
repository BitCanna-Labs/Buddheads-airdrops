#python3
# Get the list of STAR > BCNA > NEUTARO and iterate on BCNA address searching for delegations.
import json
import requests
from collections import defaultdict

# Load the JSON file
with open('converted-address.json', 'r') as file:
    data = json.load(file)

# Delete duplicates based on field "bitcanna"
unique_data = {entry['bitcanna']: entry for entry in data}.values()

# List where to store the results
total_zero_list = []
total_non_zero_list = []

# Get the total of delegations by address
def get_total_delegations(bitcanna_address):
    url = f"https://lcd.bitcanna.io/cosmos/staking/v1beta1/delegations/{bitcanna_address}"
    response = requests.get(url)
    print(f"Checking {bitcanna_address}")
    if response.status_code == 200:
        json_response = response.json()
        total = int(json_response['pagination']['total'])
        return total
    else:
        print(f"Error getting data for address {bitcanna_address}: {response.status_code}")
        return None

# Iterate over the curated list to get the total of delegations
for entry in unique_data:
    bitcanna_address = entry['bitcanna']
    total = get_total_delegations(bitcanna_address)
    if total is not None:
        if total == 0:
            total_zero_list.append(bitcanna_address)
        else:
            total_non_zero_list.append(bitcanna_address)

# Print results
print(f"Total = 0: {len(total_zero_list)} addresses")
print(total_zero_list)
print(f"\nTotal > 0: {len(total_non_zero_list)} addresses")
print(total_non_zero_list)

# Store results in a JSON file
with open('total_zero_list.json', 'w') as file:
    json.dump(total_zero_list, file)

with open('total_non_zero_list.json', 'w') as file:
    json.dump(total_non_zero_list, file)
