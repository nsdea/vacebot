# =================================================
# >>> BOT-EINSTELLUNGEN <<<

prefix = '!'

support_erstellen = '➕ Ticket erstellen 📩'
support_kanal = '📨-support-<name>'
support_kanal_nameanfang = '📨-support-'

team_rolle = 'Teammitglied'
standard_rolle = 'Spieler'

verifizierungs_kanal = '╚-✅-》verifizieren'
rollen_kanal = '╠❕》rollen'
log_kanal = 'log'

member_zaehler = '💥 <online>/<alle> online'

spam_woerter = 'scheiße fick sex penis arschloch drecks huren'

rollen_auswahl = {
#   EMOJI    ROLLE
    '💙': 'TestBlau',
    '❤️': 'TestRot',
    # und so weiter
}

# ==================================================

spam_woerter = spam_woerter.split()

import os

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

dotenv.load_dotenv()

intents = discord.Intents.all()
intents.members = True
client = commands.Bot(command_prefix=commands.when_mentioned_or(prefix), intents=intents)

@client.event
async def on_ready():
    print(f'Bot online: {client.user}')
    await client.change_presence(activity=discord.Game(name='VaceMC bot!'))

async def tensecondloop():
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

client.loop.create_task(tensecondloop())


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
    embed = discord.Embed(title='Willkommen auf VaceMC!', color=discord.Color(0xFF0000), url='https://web.vacemc.de', description=f'Viel Spaß auf dem Server, {member.mention}!\nDu bist der {len(member.guild.members)}. Member.') # f-string
    embed.set_thumbnail(url=member.avatar_url)

    # ignoriere das: finde_kanal(member.guild, '╔💐》willkommen')
    await member.send(content=member.mention, embed=embed)
    # ignoriere das: await member.add_roles(finde_rolle(member.guild, 'Spieler'))
    if member.id in [657900196189044736, 857344312718524447]: # onlix und sein Zweitaccount (xilno)
        await member.add_roles(finde_rolle(member.guild, '*'))

@client.event
async def on_member_remove(member):
    embed = discord.Embed(title=f'{member.name}#{member.discriminator} hat den Server verlassen', color=discord.Color(0xFF0000), description=f'Der Nutzer wurde gekickt, gebannt oder hat den Server verlassen.')
    await finde_kanal(member.guild, log_kanal).send(content=finde_rolle(member.guild, 'Watchdog').mention, embed=embed)

@client.event
async def on_raw_reaction_add(data):
    if data.channel_id == finde_kanal(data.member.guild, verifizierungs_kanal).id:
        await data.member.add_roles(finde_rolle(data.member.guild, standard_rolle))

    elif data.channel_id == finde_kanal(data.member.guild, rollen_kanal).id:
        for rolle in rollen_auswahl.keys():
            if rolle == data.emoji.name:
                await data.member.add_roles(finde_rolle(data.member.guild, rollen_auswahl[rolle]))

@client.command(help='Entfernt eine Reaktions-Rolle.')
async def unreact(ctx, *rolle):
    rolle = ' '.join(rolle)
    if finde_rolle(ctx.guild, rolle) and rolle in rollen_auswahl.values():
        await ctx.author.remove_roles(finde_rolle(ctx.guild, rolle))
    await ctx.message.delete()

@client.command(help='Erstellt einen Member-Zähler')
async def countsetup(ctx):
    kanal = await ctx.guild.create_voice_channel(name=member_zaehler)
    await kanal.set_permissions(finde_rolle(ctx.guild, '*'), view_channel=True, connect=False)
    await kanal.set_permissions(finde_rolle(ctx.guild, '@everyone'), view_channel=True, connect=False)

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
    
    await kanal.send(content=finde_rolle(member.guild, team_rolle).mention, embed=discord.Embed(title='Support-Ticket', description='✅ Willkommen beim Support-Ticket! Hier kann dir der Support weiterhelfen.\n> Um den Kanal zu schließen, mach `!ticketclose`.', color=discord.Color(0x03ff70)))
    await finde_kanal(member.guild, log_kanal).send(embed=discord.Embed(title='Neues Support-Ticket', description=f'📩 **{member.name}#{member.discriminator}** hat ein Support-Ticket erstellt: {kanal.mention}', color=discord.Color(0x03ff70)))

@client.event
async def on_voice_state_update(member, before, after):
    if after.channel:
        if after.channel.name == support_erstellen:
            await create_support(after.channel, member)

@commands.has_permissions(manage_channels=True)
@client.command(help='Erstellt einen Ticket-Kanal')
async def ticketsetup(ctx):
    await ctx.guild.create_voice_channel(name=support_erstellen, category=ctx.channel.category)

@commands.has_permissions(manage_channels=True)
@client.command(help='Erstellt einen Ticket-Kanal')
async def ticketopen(ctx, user: discord.Member):
    await create_support(ctx.channel, user)

@client.command(help='Löscht einen Ticket-Kanal')
async def ticketclose(ctx):
    if ctx.channel.name.startswith(support_kanal_nameanfang):
        await ctx.channel.delete()
        await finde_kanal(ctx.guild, log_kanal).send(embed=discord.Embed(title='Support-Ticket beendet', description=f'🗑 **{ctx.channel.name}** wurde gelöscht von {ctx.author.mention}.', color=discord.Color(0xFF0000)))

@client.event
async def on_message(message):
    for spam_wort in spam_woerter:
        if spam_wort in message.content:
            await message.delete()
            embed = discord.Embed(title=f'{message.author.name}#{message.author.discriminator} hat gespammt', color=discord.Color(0xFF0000), description=f'Die Nachricht lautet:\n```\n{message.content}``` wobei das Wort *{spam_wort}* erkannt und die Nachricht gelöscht wurde.')
            await finde_kanal(message.author.guild, log_kanal).send(content=finde_rolle(message.author.guild, 'Watchdog').mention, embed=embed)

    if message.channel.name == rollen_kanal and not message.content.startswith(prefix + 'unreact '):
        await message.delete()

    await client.process_commands(message) # führe den Command aus, falls es ein Command ist

client.run(os.getenv('TOKEN'))