import discord
import os
import random
import datetime
from pymongo import MongoClient
import yfinance as yf
import matplotlib.pyplot as plt

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
        answer = ["Da, coaie, așa este.", "Posibil.",
                  "Nu, frate, greșești.", "Da' de unde știi tu, mă?"]
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

    # Stock share price.
    if message.content.startswith(".stock"):
        choices = message.content.split()
        del choices[0]
        stock = yf.Ticker(choices[0])
        todays_data = stock.history(period='1d')
        # await message.channel.send(f"> {stock.info['symbol']} ({stock.info['longName']}) | Open: ${stock.info['open']} | High: ${stock.info['dayHigh']} | {stock.info['regularMarketVolume']}")
        await message.channel.send(f"> {stock.info['symbol']} ({stock.info['longName']}) | Price: ${todays_data['Close'][0]} | Volume: {stock.info['regularMarketVolume']}")

    # Stock share price. Chart.
    if message.content.startswith(".chart"):
        choices = message.content.split()
        del choices[0] # Deleting the first element, which is the command itself.
        stock = yf.Ticker(choices[0]) # Stock name.
        hist = stock.history(period="1mo") # Period.
        hist['Close'].plot(figsize=(9, 5)) # Building the chart.
        plt.title(f"({stock.info['symbol']}) ON ONE MONTH PERIOD") # Title.
        plt.savefig(fname='plot') # Saving the generated chart so we can send it over in a message.
        await message.channel.send(file=discord.File('plot.png')) # Providing the chart.
        os.remove('plot.png') # Removing the chart so we won't occupy memory.
        plt.clf() # Clear the current figure. Otherwise the cache memory will conflict.

    # I have nothing to say.
    if message.content == ".look":
        look = "Look, if I am going to be honest with you - in my own humble opinion, without being sentimental, of course, without offending anyone who thinks differently, from my own point of view, but also by looking into this matter in a distinctive perspective - I would like to say I have nothing to say."
        await message.channel.send(f"> {look}")

    # Return all possible commands that can be used.
    if message.content == ".ba":
        embed = discord.Embed(title="Vlad the Impaler here to serve you!", description="Poți să folosești următoarele comenzi pe mine.")
        embed.add_field(name=".tepes", value="Citat motivațional de la Vlad Țepeș.")
        embed.add_field(name=".vasile", value="Vrăjeală ieftină.")
        embed.add_field(name=".membri", value="Numărul de membri de pe server.")
        embed.add_field(name=".dacubanu", value="Cap și pajură.")
        embed.add_field(name=".glumita", value="Lawyer jokes.")
        embed.add_field(name=".alege", value="Voia mea este poruncă!")
        embed.add_field(name=".stock", value="Stock price.")
        embed.add_field(name=".chart", value="La fel ca .stock, doar că cu diagramă.")
        embed.add_field(name=".look", value="I have nothing to say.")
        await message.channel.send(content=None, embed=embed)


@client.event
async def on_raw_message_delete(payload):  # Logging deleted messages.
    # Channel where the logs are being sent to.
    channel = client.get_channel(798663330516172830)
    # Getting cached message. The proper way to delete a message is with message_id, don't rely on this all the time.
    message = payload.cached_message
    await channel.send(f"[{datetime.datetime.now()}] {message.author} a șters în #{message.channel} [{message.content}]")


@client.event
async def on_member_join(member):
    for channel in member.guild.channels:
        # We check to make sure we are sending the message in the general channel
        if str(channel) == "general":
            await channel.send_message(f"""Welcome to the server, {member.mention}!""")

client.run(os.getenv('TOKEN'))
