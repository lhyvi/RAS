import requests
import random
import argparse
import os

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("user", help="The user to pick animes from", type=str)
    args = parser.parse_args()
    user = args.user

    params = {
        'status': 'plan_to_watch',
        'sort': 'list_updated_at',
        'limit': 1000,
    }

    client_id = os.environ.get('X-MAL-CLIENT-ID')
    if not client_id:
        print("Set X-MAL-CLIENT-ID to MAL API client ID in env")
        exit(1)

    headers = {
        'X-MAL-CLIENT-ID': client_id,
    }

    response = requests.get(f'https://api.myanimelist.net/v2/users/{user}/animelist', params=params, headers=headers)

    if response.status_code == 404:
        print('Error 404')
        print(f'User "{user}", not found')
        exit(1)

    if response.status_code != 200:
        print(response)
        print(response.json())
        exit(1)

    titles = [(x['node']['title'], x['node']['id']) for x in response.json()['data']]

    while True and titles:
        print(f"Titles left: {len(titles)}")
        i = random.randint(0, len(titles) - 1)
        title, id = titles[i]
        del titles[i]
        print(title)
        print(f'https://myanimelist.net/anime/{id}')


        if len(titles) <= 0:
            print("\n\n> No more titles")
            break
        if 'q' in input('press q to quit: '):
                break