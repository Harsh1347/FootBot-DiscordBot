import discord
from discord.ext import commands
from fpl import get_fixture

client = discord.Client()


@client.event
async def on_ready():
    print(f"We logged in as {client.user}")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello from the BOT!')

    if message.content.startswith('$match'):
        await message.channel.send("Today's matches are : MUN vs LEI")

    if message.content.startswith('$eplfixture'):

        await message.channel.send(f"```{get_fixture()}```")

client.run('ODIyNzIyOTE5Nzc1MzM4NDk2.YFWabQ.d4i5UdYqsr4xjvXUduywGtrYOwo')
