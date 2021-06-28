import requests

from difflib import SequenceMatcher

online = requests.get('https://raw.githubusercontent.com/nsde/vacebot/main/src/main.py').text
lokal = open('src/main.py', encoding='utf-8').read()

unterschied = SequenceMatcher(None, online, lokal).ratio() * 100

print(f'Der geupdatete Code online stimmt zu {round(unterschied, 1)}% mit deinem Code überein.')

if 'update' in input('Schreibe "update", um den Bot zu updaten: ').lower():
    print('Code wird automatisch geupdatet...')
    open('src/main.py', 'w', encoding='utf-8').write(online)
    print('Code wurde erfolgreich geupdatet!')
else:
    print('Update übersprungen.')