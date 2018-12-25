import discord
from config import *

client = discord.Client()

@client.event
async def on_ready():
    print("Kwaker Bot v0.1")
    game = discord.Game("kwakery")
    stream = discord.Streaming(name="kwaker-bot v0.1", url="https://twitch.tv/kwakery", twitch_name="kwakery")
    await client.change_presence(activity=stream)

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

@client.event
async def on_reaction_add(reaction, user):
    mId = reaction.message.id
    if mId not in settings.subscriptions:
        return

    subscription = settings.subscriptions[mId]
    for sub in subscription:
        if reaction.emoji.id == sub.id:
            role = discord.utils.get(user.server.roles, id=sub.rid)
            await client.add_roles(user, role)
            break



@client.event
async def on_reaction_remove(reaction, user):
    print("test")
    for subscription in settings.subscriptions:
        if user.server.id != subscription.sid:
            continue

        role = discord.utils.get(user.server.roles, id=subscription.rid)
        await client.add_roles(user, role)

client.run(settings.discord['token'])
