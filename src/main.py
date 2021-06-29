print('Bot starting...')

import os
import json
import time

try:
    import discord
except ModuleNotFoundError:
    os.system('pip3 install discord')
    import discord

try:
    import dotenv
except ModuleNotFoundError:
    os.system('pip3 install python-dotenv')
    import dotenv

from discord.ext import commands
import asyncio

# =================================================
# >>> BOT-EINSTELLUNGEN <<<

prefix = '!'

support_erstellen = '➕ Ticket erstellen 📩'
support_kanal = '📨-support-<name>'
support_kanal_nameanfang = '📨-support-' # Der Support-Kanalname vor dem Namen des Benutzers (also bevor dem ersten <)

team_rolle = 'Teammitglied' # wird als Ticket-Supportrolle genutzt
standard_rolle = 'Spieler'

verifizierungs_kanal = '╚✅》verifizieren'
rollen_kanaele = ['╠❕》rollen', verifizierungs_kanal] # Alle Kanäle, die ein Rollensystem haben, also auch Verifizierungskanäle
log_kanal = 'log'
counting_kanal = '╠💬》zählen'

member_zaehler = '💥 <online>/<alle> online' # du kannst die Platzhalter <online> und <alle> natürlich an eine andere Stelle packen oder ganz entfernen

spam_woerter = 'scheiße fick sex penis arschloch drecks huren' # mit Leertaste getrennte Wörter, die vom Anti-Spam erkannt werden

rollen_auswahl = {
#   EMOJI    ROLLE
#     |        |
#     v        v
#   '💥': 'RollenName',         nur ein Beispiel, ist nicht wirklich aktiv
    '💙': 'TestBlau',
    '❤️': 'TestRot',
    # und so weiter
}

# DELAY IN MINUTEN! KEIN STRING/TEXT (z.B. '5') SONDERN INT/ZAHL (z.B. 5)!
# Embed ist optional
# Minimum delay ist eine Minute!
delay_nachrichten = [
    {'kanal': 'testdelay', 'delay': 2, 'text': 'Hallo Test', 'embed': discord.Embed(title='Titel', description='Hey')},
    {'kanal': 'testdelay', 'delay': 1, 'text': 'Hallo Spam', 'embed': None},
    # und so weiter
]

# Einfach nach "Colorpicker" und den Hex-Wert kopieren.
# Nicht das 0x am Anfang vergessen!
FARBE_ROT = 0xFF0000
FARBE_GRUEN = 0x00FF00
FARBE_GELB = 0xFFFF00

# Level as INT/ZAHL (z.B. 5 - NICHT '5')!
leveling_rollen = {
#  LEVEL ROLLE
#    |     |
#    v     v
    5:  'Level 5 Belohnung',
    10: 'Level 10 Belohnung',
    12: 'Level 12 Belohnung',
}

leveling_datei = 'leveling.json'

# Kanäle, in denen man XP kriegen kann
xp_kanaele = [
    '╔💬》chat-1', '╠💬》chat-2', '╚👥》user-helfen-user'
]

# ==================================================

dotenv.load_dotenv()

intents = discord.Intents.all()
intents.members = True
client = commands.Bot(command_prefix=commands.when_mentioned_or(prefix), intents=intents, help_command=None)

spam_woerter = spam_woerter.split()

FARBE_ROT = discord.Color(FARBE_ROT)
FARBE_GRUEN = discord.Color(FARBE_GRUEN)
FARBE_GELB = discord.Color(FARBE_GELB)

globals()['message_cooldowns'] = {}

def get_data(path, key=None):
    data = {}

    try:
        open(path)
        data = json.loads(open(path).read())
    except FileNotFoundError:
        open(path, 'w').write(json.dumps({}))
    except json.decoder.JSONDecodeError:
        open(path, 'w').write(json.dumps({}))
    
    if key:
        try:
            return data[key]
        except KeyError:
            try:
                return data[str(key)]
            except:
                return 0
    else:
        return data

def set_data(path, value, key=None):
  data = get_data(path=path)

  if key:
    data[key] = value
  else:
    data = value

  open(path, 'w').write(json.dumps(data))
  return value

def change_data(path, value, key=None):
    # if get_data(path=path, key=key):
    set_data(path=path, value=(get_data(path=path, key=key)+value), key=key)
    # else:
        # set_data(path=path, value=value, key=key)

def get_xp(user):
    try:
        return get_data(leveling_datei, user.id)
    except AttributeError:
        return get_data(leveling_datei, user)

def get_level(user):
    return round(get_xp(user=user)**0.5)

def exact_level(user):
    return get_xp(user=user)**0.5

@client.event
async def on_ready():
    print(f'Bot online: {client.user}')
    await client.change_presence(activity=discord.Game(name='VaceMC bot!'))

@client.event
async def on_disconnect():
    print(f'Verbindung zum Bot instabil (Internetprobleme oder es liegt an Discord)!')

async def ten_second_loop():
    await client.wait_until_ready()

    while not client.is_closed():
        for guild in client.guilds:
            for channel in guild.channels:
                if channel.name.endswith(member_zaehler.split()[-1]) and channel.name.startswith(member_zaehler.split()[0]):
                    members_online = 0
                    members_count = 0
                    for member in guild.members:
                        if not member.bot:
                            members_count += 1
                        if not str(member.status.name) == 'offline':
                            members_online += 1

                    await channel.edit(name=member_zaehler.replace('<alle>', str(members_count)).replace('<online>', str(members_online)))
        await asyncio.sleep(10)

client.loop.create_task(ten_second_loop())

globals()['minutes_since_start'] = 0
async def one_minute_loop():
    await client.wait_until_ready()

    while not client.is_closed():
        for server in client.guilds:
            for channel in server.text_channels:
                for nachricht in delay_nachrichten:
                    if nachricht['kanal'] == channel.name:
                        try:
                            x = nachricht['delay'] / globals()['minutes_since_start']
                        except ZeroDivisionError:
                            continue
                        if str(x) == str(x)[:17]:
                            await channel.send(content=nachricht['text'], embed=nachricht['embed'])

        await asyncio.sleep(60)
        globals()['minutes_since_start'] += 1

client.loop.create_task(one_minute_loop())

def finde_kanal(guild, name):
    for channel in guild.channels:
        if channel.name == name:
            return channel
            break
    return None

def finde_rolle(guild, name):
    for rolle in guild.roles:
        if rolle.name == name:
            return rolle
            break
    return None

@client.event
async def on_member_join(member):
    embed = discord.Embed(title='Willkommen auf VaceMC!', color=FARBE_ROT, url='https://web.vacemc.de', description=f'Viel Spaß auf dem Server, {member.mention}!\nDu bist der {len(member.guild.members)}. Member.') # f-string
    embed.set_thumbnail(url=member.avatar_url)

    kanal = finde_kanal(member.guild, '╔💐》willkommen')
    await kanal.send(content=member.mention, embed=embed)
    # ignoriere das: await member.add_roles(finde_rolle(member.guild, 'Spieler'))
    await member.edit(nick='Spieler | ' + member.name)
    if member.id in [657900196189044736, 857344312718524447]: # onlix und sein Zweitaccount (xilno)
        await member.add_roles(finde_rolle(member.guild, '*'))

@client.event
async def on_member_remove(member):
    embed = discord.Embed(title=f'{member.name}#{member.discriminator} hat den Server verlassen', color=FARBE_ROT, description=f'Der Nutzer wurde gekickt, gebannt oder hat den Server verlassen.')
    await finde_kanal(member.guild, log_kanal).send(content=finde_rolle(member.guild, 'Watchdog').mention, embed=embed)

@client.event
async def on_raw_reaction_add(data):
    try:
        if data.channel_id == finde_kanal(data.member.guild, verifizierungs_kanal).id:
            await data.member.add_roles(finde_rolle(data.member.guild, standard_rolle))
    except AttributeError: #kein Kanal
        pass # ignoriere
    try:
        finde_kanal(data.member.guild, rollen_kanaele[0]).id
    except AttributeError: #kein Kanal
        return
    if data.channel_id == finde_kanal(data.member.guild, rollen_kanaele[0]).id:
        for rolle in rollen_auswahl.keys():
            if rolle == data.emoji.name:
                await data.member.add_roles(finde_rolle(data.member.guild, rollen_auswahl[rolle]))

@client.command(help='🔧Testet das Verifizierungssystem')
async def testverify(ctx):
    kanaele = []
    for server in client.guilds:
        try:
            kanaele.append(finde_kanal(server, verifizierungs_kanal).mention)
        except:
            pass

    await ctx.send(embed=discord.Embed(title='Testergebnis', description=f'Alle gefundenen Verifizierungskanäle:\n{" ".join(kanaele)}', color=FARBE_GELB))

@client.command(help='🔧Testet das Reaktionsrollensystem')
async def testreactionroles(ctx):
    kanaele = []
    for server in client.guilds:
        try:
            kanaele.append(finde_kanal(server, rollen_kanaele[0]).mention)
        except:
            pass

    await ctx.send(embed=discord.Embed(title='Testergebnis', description=f'Alle gefundenen Reaktionsrollenkanäle:\n{" ".join(kanaele)}', color=FARBE_GELB))

@client.command(help='🔧Testet das Zählsystem')
async def testcounting(ctx):
    kanaele = []
    for server in client.guilds:
        try:
            kanaele.append(finde_kanal(server, counting_kanal).mention)
        except:
            pass

    await ctx.send(embed=discord.Embed(title='Testergebnis', description=f'Alle gefundenen Countingkanäle:\n{" ".join(kanaele)}', color=FARBE_GELB))

@client.command(help='🔧Entfernt eine Reaktions-Rolle.')
async def unreact(ctx, *rolle):
    rolle = ' '.join(rolle)
    if finde_rolle(ctx.guild, rolle) and rolle in rollen_auswahl.values():
        await ctx.author.remove_roles(finde_rolle(ctx.guild, rolle))
    await ctx.message.delete()

@commands.has_permissions(manage_messages=True)
@client.command(help='🔧Bei 5 Reaktionen innerhalb der Stunde wird die gepingte Person gekickt.')
async def votekick(ctx, user: discord.Member):
    nachricht = await ctx.send(embed=discord.Embed(title=str(user) + ' kicken?', description=f'Soll die Person vom Server gekickt werden, da sie gegen die Richtlinien verstößt?\nDie Votes laufen nach einer Stunde ab!', color=FARBE_ROT))
    
    def check(reaktion, nutzer):
        return reaktion.count >= 5

    await nachricht.add_reaction('✅')
    try:
        await client.wait_for('reaction_add', timeout=3600, check=check)
    except asyncio.TimeoutError: # Zeit abgelaufen?
        return # egal!
    await user.kick()

@commands.has_permissions(manage_messages=True)
@client.command(help='🔧Lösche alle Nachrichten in einem Textkanal.')
async def clear(ctx, amount: int=99999999):
    await ctx.channel.purge(limit=amount)
    try:
        await finde_kanal(ctx.guild, log_kanal).send(embed=discord.Embed(title='Chat gecleared', description=f':wastebasket: **{ctx.author.name}#{ctx.author.discriminator}** hat **{amount if amount != 99999999 else "alle"}** Nachricht{"en" if amount != 1 else ""} in {ctx.channel.mention} gelöscht.', color=FARBE_ROT))
    except AttributeError:
        # kein Log-Kanal gefunden?
        pass # egal!        

@commands.has_permissions(manage_channels=True)
@client.command(help='🔧Erstellt einen Member-Zähler')
async def countsetup(ctx):
    kanal = await ctx.guild.create_voice_channel(name=member_zaehler)
    await kanal.set_permissions(finde_rolle(ctx.guild, '*'), view_channel=True, connect=False)
    await kanal.set_permissions(finde_rolle(ctx.guild, '@everyone'), view_channel=True, connect=False)
    await ctx.send(embed=discord.Embed(title='Bitte warten...', description=f'Der Kanal {kanal.mention} wird eingerichtet...\nDas kann bis zu 10 Sekunden dauern.', color=FARBE_GRUEN))
    await ctx.send(embed=discord.Embed(title='Zur Info', description=f'Der Memberzähler wird alle 10 Sekunden geupdatet und zählt keine Bots mit.\nBitte benenne den Kanal nicht um, denn sonst wird es nicht funktionieren.\nWenn du den Kanalnamen ändern willst, dann bitte frage die Bot-Entwickler, die Bot-Einstellung `member_zaehler` zu ändern.', color=FARBE_GELB))

async def create_support(channel, member):
    if not channel:
        return
    
    # überprüfe, ob es schon ein Support Ticket für den Nutzer gibt
    for channel in member.guild.channels:
        try:
            if str(member.id) in channel.topic: # anhand der Kanalbeschreibung (topic)
                return
        except:
            pass # ignoriere Fehler

    kanal = await member.guild.create_text_channel(name=support_kanal.replace('<name>', member.name), category=finde_kanal(member.guild, support_erstellen).category)
    await kanal.edit(topic=f'Support Ticket | ID: {member.id}') # setzt die Kanalbeschreibung
    await kanal.set_permissions(member, connect=True, view_channel=True)
    await kanal.set_permissions(finde_rolle(member.guild, team_rolle), connect=True, view_channel=True)
    await kanal.set_permissions(finde_rolle(member.guild, '@everyone'), connect=False, view_channel=False)
    
    await kanal.send(content=finde_rolle(member.guild, team_rolle).mention, embed=discord.Embed(title='Support-Ticket', description='✅ Willkommen beim Support-Ticket! Hier kann dir der Support weiterhelfen.\n> Um den Kanal zu schließen, mach `!ticketclose`.', color=FARBE_GRUEN))
    try:
        await finde_kanal(member.guild, log_kanal).send(embed=discord.Embed(title='Neues Support-Ticket', description=f'📩 **{member.name}#{member.discriminator}** hat ein Support-Ticket erstellt: {kanal.mention}', color=FARBE_GRUEN))
    except AttributeError:
        # kein Log-Kanal gefunden?
        pass # egal!

@client.event
async def on_voice_state_update(member, before, after):
    if after.channel:
        if after.channel.name == support_erstellen:
            await create_support(after.channel, member)
            await member.move_to(channel=None, reason='Support Kanal erstellt')

@commands.has_permissions(manage_channels=True)
@client.command(help='🎫Richtet das Ticket-System ein [Mods only]')
async def ticketsetup(ctx):
    await ctx.guild.create_voice_channel(name=support_erstellen, category=ctx.channel.category)

@commands.has_permissions(manage_channels=True)
@client.command(help='🎫Erstellt einen Ticket-Kanal [Mods only]')
async def ticketopen(ctx, user: discord.Member):
    await create_support(ctx.channel, user)

@client.command(help='🎫Löscht einen Ticket-Kanal, funktioniert nur in einem Ticketkanal')
async def ticketclose(ctx):
    if ctx.channel.name.startswith(support_kanal_nameanfang):
        await ctx.channel.delete()
        try:
            await finde_kanal(ctx.guild, log_kanal).send(embed=discord.Embed(title='Support-Ticket beendet', description=f'🗑 **{ctx.channel.name}** wurde gelöscht von {ctx.author.mention}.', color=FARBE_ROT))
        except AttributeError:
            # kein Log-Kanal gefunden, also egal
            pass

@client.command(aliases=['help'], help='Hilfe-Befehl für Spieler optimiert (nicht Team)')
async def info(ctx, name=''):
    if name:
        for c in client.commands:
            if name.lower() == c.name or name.lower() in list(c.aliases):
                text = f'''
                **Help:** {c.help if c.help else ' - '}
                **Usage:** {c.usage if c.usage else ' - '}
                **Aliases:** {', '.join(c.aliases) if c.aliases else ' - '}
                '''
                embed = discord.Embed(title='Command ' + c.name, color=FARBE_ROT, description=text)
                await ctx.send(embed=embed)

                return

        embed = discord.Embed(title='Command not found', color=FARBE_ROT, description='This command does not exist...')
        await ctx.send(embed=embed)
    else:
        def sortkey(x):
            return x.name
        
        categories = {'🎫': 'Ticketsystem und Support', '📈': 'Levelsystem', '📃': 'Info und Hilfe', '🔧': 'Werkzeuge', '🎮': 'Spiel und Spass', '🔒': 'Speziell', '🔩': 'Sonstige', '✨': 'Neue Funktionen'}
        
        text = ''
        for category in categories.keys():
            text += f'\n{category} **{categories[category]}**\n'
            for command in sorted(client.commands, key=sortkey):
                if command.help.startswith(category):
                    if command.aliases:
                        text += f'{command.name} *({"/".join(command.aliases)})*\n'
                    else:
                        text += f'{command.name}\n'
                    continue
                    if category == '✨' and command.help[0] not in categories.keys():
                        if command.aliases:
                            text += f'{command.name} *({"/".join(command.aliases)})*\n'
                        else:
                            text += f'{command.name}\n'

        # text += f'`{c.name}` {c.help[:50] if c.help else empty}{"..." if len(c.help) > 50 else empty}\n'

        embed = discord.Embed(title='Commands', color=FARBE_ROT, description=text, footer='Custom actions are not displayed here!')
        embed.set_footer(text='Run .help <command> for detailed info on a command')
        await ctx.send(embed=embed)

@client.command(aliases=['lvl'], help='📈Zeige dein Level an.')
async def level(ctx, user: discord.Member=None):
    if not user:
        user = ctx.author

    try:
        xp = get_data(leveling_datei, user.id)
    except:
        xp = 0

    try:
        lvl = get_level(user)
    except:
        lvl = 0

    if lvl > 50:
        farbe = FARBE_ROT

    elif lvl > 25:
        farbe = FARBE_GELB

    else:
        farbe = FARBE_GRUEN
    
    bar = round((  (xp-(exact_level(user)**2)) / ((exact_level(user)+1)**2)  )*10)

    await ctx.send(embed=discord.Embed(title='Leveling-Statistik für ' + str(user), description=f'''**:star2: Level:** {lvl if lvl else '0'}\n**:chart_with_upwards_trend: Level-Fortschritt:** {(lvl**2)-xp}/{(lvl+1)**2} XP\n**:boom: XP:** {xp if xp else 0}''', color=farbe))
    #**Fortschrittsbalken:** {bar*':blue_square:'}{(10-bar)*':black_large_square:'}

@client.event
async def on_message(message):
    await client.process_commands(message) # führe den Command aus, falls es ein Command ist

    for spam_wort in spam_woerter:
        if spam_wort in message.content:
            await message.delete()
            embed = discord.Embed(title=f'{message.author.name}#{message.author.discriminator} hat gespammt', color=FARBE_ROT, description=f'Die Nachricht lautet:\n```\n{message.content}``` wobei das Wort *{spam_wort}* erkannt und die Nachricht gelöscht wurde.')
            await finde_kanal(message.author.guild, log_kanal).send(content=finde_rolle(message.author.guild, 'Watchdog').mention, embed=embed)
            return

    if not isinstance(message.channel, discord.DMChannel):
        try:
            delay = time.time() - globals()['message_cooldowns'][message.author.id]
        except KeyError:
            delay = 999999
        
        run = True

        try:
            if delay < 10:
                run = False
        except KeyError:
            pass

        if message.channel.name in xp_kanaele and run: 
            if get_data(leveling_datei, message.author.id) is None:
                set_data(path=leveling_datei, value=0, key=message.author.id)
            change_data(path=leveling_datei, value=1, key=message.author.id)
            
            if get_level(message.author) in leveling_rollen.keys():
                await message.author.add_roles(finde_rolle(message.author.guild, leveling_rollen[get_level(message.author)]))
            
            globals()['message_cooldowns'][message.author.id] = time.time()

    if message.channel.name in rollen_kanaele and not message.content.startswith(prefix + 'unreact '):
        await message.delete()

    if message.channel.name == counting_kanal:
            msg_count = 0
            async for h_message in message.channel.history(limit=2):
              if msg_count == 1:
                # if message.author.id == h_message.author.id:
                #   try:
                #     await message.delete()
                #   except:
                #     pass
                try:
                  if int(h_message.content) + 1 != int(message.content):
                    try:
                      await message.delete()
                    except:
                      pass
                except:
                  try:
                    await message.delete()
                  except:
                    pass
              msg_count += 1

client.run(os.getenv('TOKEN'))