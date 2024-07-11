import json
from bech32 import bech32_decode, bech32_encode, convertbits

def process_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        tokens_owner = json.load(f)
    
    final_output = []

    for type in tokens_owner:
        hrp, data = bech32_decode(type['owner'])
        if hrp is None or data is None:
            continue  # Skip invalid bech32 addresses

        converted_data = convertbits(data, 5, 8, False)
        if converted_data is None:
            continue  # Skip addresses that cannot be converted

        neutaro_addr = bech32_encode('neutaro', convertbits(converted_data, 8, 5, True))
        star_addr = bech32_encode('star', convertbits(converted_data, 8, 5, True))

        final_output.append({
            "bitcanna": type['owner'],
            "startgaze": star_addr,
            "neutaro": neutaro_addr
        })

    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(final_output, f, indent=2)
        print(f'Data successfully saved to {output_file}')
    except Exception as error:
        print(f'An error has occurred while saving to {output_file}: {error}')

# Process the first file
process_file('./temporal_stakers_list.json', './final_stakers_list_2.json')

# Process the second file
process_file('./temporal_nostakers_list.json', './final_nostakers_list_2.json')
