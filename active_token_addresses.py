import requests
import json

def fetch_graphql(query, variables):
    url = 'https://graphql.mainnet.stargaze-apis.com/graphql'
    headers = {
        'Content-Type': 'application/json',
    }
    response = requests.post(url, json={'query': query, 'variables': variables}, headers=headers)
    response.raise_for_status()
    return response.json()

def fetch_all_owners():
    all_owners = set()
    all_tokens = []
    has_more = True
    offset = 0
    limit = 100

    query = """
    query GetTokensByCollection($offset: Int) {
      tokens(collectionAddr: "stars1w4dff5myjyzymk8tkpjrzj6gnv352hcdpt2dszweqnff927a9xmqc7e0gv", limit: 100, offset: $offset) {
        tokens {
          tokenId
          owner {
            address
          }
        }
      }
    }
    """

    while has_more:
        variables = {'offset': offset}
        response = fetch_graphql(query, variables)
        tokens = response['data']['tokens']['tokens']

        if len(tokens) < limit:
            has_more = False

        for token in tokens:
            token_id = token['tokenId']
            owner_address = token['owner']['address']
            all_owners.add(owner_address)
            all_tokens.append({
                'tokenId': token_id,
                'owner': owner_address
            })

        offset += limit
        print("Let's go for more: " + str(offset))

    return all_owners, all_tokens

if __name__ == '__main__':
    owners, tokens = fetch_all_owners()
    print(f"Total number of unique owners: {len(owners)}")
    print(f"Total number of tokens with owners: {len(tokens)}")

    # Guardar el listado en un archivo JSON
    with open('tokens_with_owners.json', 'w') as json_file:
        json.dump(tokens, json_file, indent=4)

    print("Results saved at 'tokens_with_owners.json'")