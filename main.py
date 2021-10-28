import os
import discord
from discord.ext import commands
import music
from keep_alive import keep_alive

cogs = [music]

client = commands.Bot(command_prefix='?', intents = discord.Intents.all())
print("Started")

for i in range(len(cogs)):
  cogs[i].setup(client)

my_secret = os.environ['token']

keep_alive()
client.run(my_secret)