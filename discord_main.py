import discord
from discord.ext import commands
from discord import app_commands
import os
import json
import requests
import asyncio
import json
import datetime
import time
from helpers.redisClient import redis_client
from dotenv import find_dotenv, load_dotenv

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)


# from controllers.queryBooks import query_books

TOKEN = os.environ.get("TOKEN")
GUILD = "bots test server"

intents = discord.Intents.all()

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

# queryResult = query_books(title="Moby-Dick")


# async def schedule_message(interaction, interval):
#     is_active = True

#     while is_active:
#         rawData = redis_client.get(str(interaction.user.name))
#         userData = json.loads(rawData)

#         is_active = userData["isActive"]

#         if userData["status"] == 0:
#             message = "The temp in inside the threshold."
#         elif userData["status"] == -1:
#             message = "The current temp is lower than the threshold."
#         elif userData["status"] == 1:
#             message = "The current temp is higher than the threshold."

#         if userData["prevStatus"] != userData["status"]:
#             embed = discord.Embed(description=message, color=discord.Color.green())
#             await interaction.followup.send(embed=embed, ephemeral=True)

#         await asyncio.sleep(interval)


@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(e)


def write_info(filename, query):
    try:
        ## write json
        data = {}
        data["isActive"] = True
        data["query"] = query
        data["isDone"] = False
        data["isReceived"] = False
        data["output"] = "Auuuuuuughhhh!!"
        with open(filename, "w") as outfile:
            json.dump(data, outfile)
    except Exception as e:
        print(e)


def make_doc(prompt, filename):
    """
    make/overwrite a doc in redis
    the doc is made so that it can be consumed by an agent
    doc can be made with 2 different filenames.
    customer_service or store
    """
    try:
        data = {
            "isActive": True,
            "status": 0,
            "prompt": prompt,
            "isReceived": False,
            "isDone": False,
            "output": "",
        }
        print("writing ", filename, " in redis")
        redis_client.set(filename, json.dumps(data))
    except Exception as e:
        print(e)


async def read_doc(interaction, filename):
    """
    read a doc from redis
    then it waits for the bool "isDone" to turn True
    indicating that the request has been processed
    then it replies with the llm's output
    """
    try:
        dataRaw = redis_client.get(filename)
        data = json.loads(dataRaw)
        await interaction.response.send_message(
            "Please wait for a moment...", ephemeral=True
        )
        print("listening for changes in ", filename)
        while data["isDone"] == False:
            dataRaw = redis_client.get(filename)
            data = json.loads(dataRaw)
        k = data["output"]
        print("replying with output from ", filename)
        await interaction.followup.send(k, ephemeral=True)
    except Exception as e:
        print(e)


# Book Store Command
@bot.tree.command(
    name="book_store", description="Call this to query our book store bot."
)
@app_commands.describe(
    prompt="Enter any prompt to communicate with the given agent.",
)
async def book_store_update(interaction: discord.Interaction, prompt: str):
    print(prompt)
    make_doc(prompt, "store")
    await read_doc(interaction, "store")


# Customer Service Command
@bot.tree.command(
    name="customer_service", description="Call this to query our customer service bot."
)
@app_commands.describe(
    prompt="What is wrong with you?",
)
async def customer_service_call(interaction: discord.Interaction, prompt: str):
    print(prompt)
    make_doc(prompt, "customer_service")
    await read_doc(interaction, "customer_service")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return


bot.run(TOKEN)
