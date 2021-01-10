import discord
import os
import random
from pymongo import MongoClient

client = discord.Client()

cluster = MongoClient(os.getenv('MONGODB_URI'), 27017)
db = cluster["discord"]
collection_vt = db["vlad_the_impaler"]
collection_v = db["vasile"]
collection_lj = db["lawyer_jokes"]

@client.event
async def on_ready():
  print(f"We have logged in as {client.user}.")

# Getting quotes for Vlad the Impaler.
vlad_the_impaler = []
for vorbele_lu_tepes in collection_vt.find():
  vlad_the_impaler.append(vorbele_lu_tepes["quote"])
tepes = vlad_the_impaler.copy()

# Getting quotes for Vasile.
vasile = []
for vorbele_lu_vasile in collection_v.find():
  vasile.append(vorbele_lu_vasile["quote"])
vasilica = vasile.copy()

# Getting lawyer jokes.
lawyer_jokes = []
for joke in collection_lj.find():
  lawyer_jokes.append(joke["joke"])
jokes = lawyer_jokes.copy()

@client.event
async def on_message(message):

  id = client.get_guild(792574419066159105)

  # Send Vlad the Impaler messages.
  if message.content == ".tepes":
    mesaj = random.choice(tepes)
    await message.channel.send(mesaj)

  # Send Vasile messages.
  if message.content == ".vasile":
    mesaj = random.choice(vasilica)
    await message.channel.send(mesaj)

  # Send lawyer jokes.
  if message.content == ".glumita":
    mesaj = random.choice(jokes)
    await message.channel.send(mesaj)

  # Display current number of members.
  if message.content == ".membri":
    await message.channel.send(f"""Sunt în total {id.member_count} membri pe server.""")
  
  # Make the bot to agree with you on everything.
  if message.content.endswith(", nu?"):
    await message.channel.send("Da, coaie, așa este.")

  # Return all possible commands that can be used.
  if message.content == ".ba":
    embed = discord.Embed(title="Vlad the Impaler here to serve you!", description="Poți să folosești următoarele comenzi pe mine.")
    embed.add_field(name=".tepes", value="Citat motivațional de la Vlad Țepeș.")
    embed.add_field(name=".vasile", value="Vrăjeală ieftină.")
    embed.add_field(name=".membri", value="Numărul de membri de pe server.")
    embed.add_field(name=".dacubanu", value="Cap și pajură.")
    await message.channel.send(content=None, embed=embed)

  # Flip a coin.
  if message.content == ".dacubanu":
    variable = ["Cap.", "Pajură."]
    await message.channel.send("{}".format(random.choice(variable)))

async def on_member_join(member):
    for channel in member.guild.channels:
        if str(channel) == "general": # We check to make sure we are sending the message in the general channel
            await channel.send_message(f"""Welcome to the server, {member.mention}!""")

client.run(os.getenv('TOKEN'))