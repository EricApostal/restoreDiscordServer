import subprocess
import sys
from os import replace
import json

try:
    print("[STARTUP] Attempting to load package 'nextcord'")
    import nextcord
    from nextcord.ext import commands
    print('[STARTUP] nextcord succesfully imported')
except:
    print('[STARTUP] nextcord not found, attempting install')
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'nextcord'])
    import nextcord
    print('Succefully installed and imported nextcord!')





intents = nextcord.Intents.default()
intents.members = True
client = nextcord.Client(intents=intents)
whitelisted_channels = []

f = open('config.json')
config = json.load(f)
token = config['token']

@client.event
async def on_message(message):
    if message.content.startswith('!unpurge'):

        f = open("whitelistedchannels.txt", "r")
        for line in f.readlines():
            try:
                whitelisted_channels.append(int(line.replace('\n', '')))
            except:
                continue 

        for channel in message.guild.channels:
            if channel.id not in whitelisted_channels:
                await channel.delete()
                print(f'[LOG] Deleted {channel}!')
            else:
                print(f'[LOG] Found {channel} but skipping due to whitelist')

    elif message.content.startswith('!test'):       
        for i in range(100):                          
            await message.guild.create_text_channel(f'throwaway-channel-{i}')

@client.event
async def on_ready():
    print('[LOG] Auth successful, bot is in standby mode. Some tips before we begin: \n\n[TIP] Make sure the Bot has the highest role in your server\n[TIP] You can set whitelisted channels in the first line of the main.py file')
    print('[WARN] If you would like to test bot functionality, use !test. WARNING!: Running !test WILL make 100 random channels!')
    print("[LOG] Type '!unpurge' to remove all discord channels not excluded in whitelist.txt!")

client.run(token)
