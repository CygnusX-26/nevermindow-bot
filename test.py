import requests
from pprint import pprint
name = 'Wyvern'
tag = '11208'
puuid = 'a756a896-b856-5cd2-8695-235816d4324b'
c = requests.get(f'https://api.henrikdev.xyz/valorant/v3/matches/na/{name}/{tag}').json()
players = c['data'][0]['players']['all_players']
for player in players:
    if player['puuid'] == puuid:
        pprint(player)