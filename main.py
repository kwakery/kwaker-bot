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
async def on_voice_state_update(user, before, after):
    # print(discord.utils.get(user.guild.roles, name="Music").id)
    if user.guild.id != 522607015336476683:
        return

    role = user.guild.get_role(526952431297232906) # Get "Music" role object

    if after.channel != None and after.channel.id == 526968501903163413:
        await user.add_roles(role)
    else:
        if role in user.roles:
            await user.remove_roles(role)

@client.event
async def on_raw_reaction_add(event):
    mId = event.message_id
    if mId not in settings.subscriptions:
        return

    subscription = settings.subscriptions[mId]

    for sub in subscription:
        if event.emoji.id == sub.id:
            guild = client.get_guild(event.guild_id)
            user = guild.get_member(event.user_id)
            role = guild.get_role(sub.rid)

            await user.add_roles(role, reason="User requested via reaction")
            break

@client.event
async def on_raw_reaction_remove(event):
    mId = event.message_id
    if mId not in settings.subscriptions:
        return

    subscription = settings.subscriptions[mId]

    for sub in subscription:
        if event.emoji.id == sub.id:
            guild = client.get_guild(event.guild_id)
            user = guild.get_member(event.user_id)
            role = guild.get_role(sub.rid)

            await user.remove_roles(role, reason="User requested via reaction")
            break


client.run(settings.discord['token'])
