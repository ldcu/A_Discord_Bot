import discord
import os
import random
import datetime
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

# Getting quotes for Vasile.
vasile = []
for vorbele_lu_vasile in collection_v.find():
  vasile.append(vorbele_lu_vasile["quote"])

# Getting lawyer jokes.
lawyer_jokes = []
for joke in collection_lj.find():
  lawyer_jokes.append(joke["joke"])

@client.event
async def on_message(message):

  id = client.get_guild(792574419066159105)

  # Send Vlad the Impaler messages.
  if message.content == ".tepes":
    await message.channel.send(f"> {random.choice(vlad_the_impaler)}")

  # Send Vasile messages.
  if message.content == ".vasile":
    await message.channel.send(f"> {random.choice(vasile)}")

  # Send lawyer jokes.
  if message.content == ".glumita":
    await message.channel.send(f"> {random.choice(lawyer_jokes)}")

  # Display current number of members.
  if message.content == ".membri":
    await message.channel.send(f"""> Sunt în total {id.member_count} membri pe server.""")
  
  # Make the bot to agree with you on everything.
  if message.content.endswith(", nu?"):
    answer = ["Da, coaie, așa este.", "Posibil.", "Nu, frate, greșești.", "Da' de unde știi tu, mă?"]
    await message.channel.send(f"> {random.choice(answer)}")

  # Flip a coin.
  if message.content == ".dacubanu":
    answer = ["Cap.", "Pajură."]
    await message.channel.send(f"> {random.choice(answer)}")

  # Choice maker.
  if message.content.startswith(".alege"):
    choices = message.content.split()
    del choices[0]
    await message.channel.send(f"> {random.choice(choices)}")

  # Return all possible commands that can be used.
  if message.content == ".ba":
    embed = discord.Embed(title="Vlad the Impaler here to serve you!", description="Poți să folosești următoarele comenzi pe mine.")
    embed.add_field(name=".tepes", value="Citat motivațional de la Vlad Țepeș.")
    embed.add_field(name=".vasile", value="Vrăjeală ieftină.")
    embed.add_field(name=".membri", value="Numărul de membri de pe server.")
    embed.add_field(name=".dacubanu", value="Cap și pajură.")
    embed.add_field(name=".glumita", value="Lawyer jokes.")
    embed.add_field(name=".alege", value="Eu decid pentru tine!")
    await message.channel.send(content=None, embed=embed)

@client.event
async def on_raw_message_delete(payload): # Logging deleted messages.
    channel = client.get_channel(798663330516172830) # Channel where the logs are being sent to.
    message = payload.cached_message # Getting cached message. The proper way to delete a message is with message_id, don't rely on this all the time.
    await channel.send(f"[{datetime.datetime.now()}] {message.author} a șters în #{message.channel} [{message.content}]")

@client.event
async def on_member_join(member):
    for channel in member.guild.channels:
        if str(channel) == "general": # We check to make sure we are sending the message in the general channel
            await channel.send_message(f"""Welcome to the server, {member.mention}!""")

client.run(os.getenv('TOKEN'))