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
async def on_raw_reaction_add(event):
    print("test0")
    mId = event.message_id
    if mId not in settings.subscriptions:
        return
    print("test1")
    subscription = settings.subscriptions[mId]
    for sub in subscription:
        print("test2")
        if event.emoji.id == sub.id:
            print("test3")
            guild = client.TextChannel(id=event.channel_id).guild
            role = guild.get_role(sub.rid)
            print("test4")
            await client.add_roles(user, role, reason="User requested via reaction")
            break



@client.event
async def on_raw_reaction_add(event):
    mId = event.message_id
    if mId not in settings.subscriptions:
        return

    subscription = settings.subscriptions[mId]
    for sub in subscription:
        if event.emoji.id == sub.id:
            guild = client.TextChannel(id=event.channel_id).guild
            role = guild.get_role(sub.rid)

            await client.remove_roles(user, role, reason="User requested via reaction")
            break

client.run(settings.discord['token'])
