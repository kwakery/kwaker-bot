import discord
from config import *

client = discord.Client()

@client.event
async def on_ready():
    print("Kwaker Bot v0.1")
    await client.change_presence(game=discord.Game(name="kwakery"))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    # if message.content == "Hello":
    #     await client.send_message(message.channel, "World")

@client.event
async def on_voice_state_update(before, after):
    if after.server.id != "522607015336476683":
        return

    role = discord.utils.get(after.server.roles, name="Music") # Get "Music" role object

    if after.voice_channel != None and after.voice_channel.id == "526968501903163413":
        await client.add_roles(after, role)
    else:
        if role in after.roles:
            await client.remove_roles(after, role)


client.run(settings.discord['token'])
