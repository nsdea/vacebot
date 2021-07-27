import os
import requests
import webbrowser

from difflib import SequenceMatcher

print()
print('*****************************')
print('Willkommen zum Update-Helfer!')
print('*****************************')
print('Falls ein Fehler auftritt, kontaktiere bitte die Entwickler.\n')
print('Abbruch des ganzen Programms - wie immer - mit STRG (also CTRL) + C\n')
print()
print('Bitte immer alles aufmerksam durchlesen!')

input('\n--> Enter drücken\n')

online = requests.get('https://raw.githubusercontent.com/nsde/vacebot/main/src/main.py').text
lokal = open('src/main.py', encoding='utf-8').read()
unterschied = SequenceMatcher(None, online, lokal).ratio() * 100

print(f'Der geupdatete, neue main.py-Code online stimmt zu {round(unterschied, 1)}% mit deinem Code überein.')
print('Beachte allerdings, dass der Unterschied der Einstellungen auch mitgezählt wird, das heißt, es kann zu wenigen Prozent Unterschied kommen!')
print()

online_updater = requests.get('https://raw.githubusercontent.com/nsde/vacebot/main/update.py').text
lokal_updater = open('update.py', encoding='utf-8').read()
unterschied_updater = SequenceMatcher(None, online_updater, lokal_updater).ratio() * 100

print(f'Der Updater ist zu {round(unterschied_updater, 1)}% geupdatet. (lol, ja, auch der Updater muss geupdatet werden :D)')
print('Den Updater musst du leider manuell updaten, weil ich mich nicht selbst ändern kann, das geht einfach nicht.')
print()

if 'y' in input('Hauptdatei (main.py) updaten? "y" (empfohlen) oder "n": ').lower():
    print('GANZ WICHTIG!!!')
    print('Die Einstellungen werden in der main.py-Datei gespeichert.')
    print('Das heißt: !!! nach den Update werden deine Einstellungen zurückgesetzt!!!')
    print('Damit du deine Einstellungen nicht aus Versehen verlierst, werden wir dir ein Backup (main.backup.py) erstellen.')
    print('!!! WICHTIG: Du musst die Einstellungen der main.py also später ändern !!!\n')

    input('--> Enter drücken, um fortzufahren')

    print('\nBackup wird erstellt...')
    open('src/main.backup.py', 'w', encoding='utf-8').write(open('src/main.py', encoding='utf-8').read())
    print('Backup erfolgreich erstellt.')

    print('\nCode wird automatisch geupdatet...')
    open('src/main.py', 'w', encoding='utf-8').write(online)
    print('Code wurde erfolgreich geupdatet!')

else:
    print('Update übersprungen.')

if 'y' in input('\nPackages updaten? "y" (empfohlen) oder "n": ').lower():
    print('Lehn\' dich zurück. Das kann etwas dauern.')
    print('Wir sagen bescheid, wenn es fertig ist (nicht davor schließen!).')
    input('\n--> Enter drücken, um loszulegen.\n\n\n')

    os.system('pip3 install -r requirements.txt')
    
    print('\n\n\n' + ('#'*50))
    print('+++ Fertig! +++')

else:
    print('Package Installation übersprungen.')

if 'y' in input('\nMöglicherweise musst du die ".env" ändern, weil neue Einstellungen nötig sind.\n"y" (empfohlen) oder "n": ').lower():
    print('Leider musst du das manuell tun. Vergleiche die online-Template (Vorlage) mit deiner lokalen ".env".')
    print('Falls du dir unsicher ist, was in die Template einzutragen ist, ließ in der README.md nach oder frage einen Entwickler.')
    print('!!! Es wird bei Entertastendruck ein Backup der .env erstellt.')
    print()
    print('Fortfahren, um das Backup zu erstellen, und um die online-Template der .env zu öffnen.')

    input('\n--> Enter drücken')

    open('src/.env_backup', 'w', encoding='utf-8').write(open('src/.env', encoding='utf-8').read())
    webbrowser.open('https://raw.githubusercontent.com/nsde/vacebot/main/src/dot_env_template.txt')

else:
    print('.env-Prüfung übersprungen.')

print('\n=== Ende des Updaters ===')