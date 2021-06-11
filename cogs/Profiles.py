import discord
from discord.ext import commands
import os
from urllib.request import urlopen
import json
import requests
import time
import random
import asyncio
import motor
import motor.motor_asyncio
from pymongo import MongoClient

user = os.environ.get("user")
passw = os.environ.get("pass")

cluster = motor.motor_asyncio.AsyncIOMotorClient(f"mongodb+srv://{user}:{passw}@starky.octkb.mongodb.net/Starky?retryWrites=true&w=majority")
database = cluster["ka"]["profiles"]

#db drainedboost

def get_data(url):
    response = urlopen(url)
    data = response.read().decode("utf-8")
    return json.loads(data)

class Profiles(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def setprofile(self, ctx, type=None, id=None):
        info = await database.find_one({"id":ctx.author.id})
        if info:
            return await ctx.send('You already have a set profile')

        if type.lower() not in ["kaid", "user"]:
            return await ctx.send("This command should be used like\n```k!verify kaid kaid_................``` or\n```k!verify username kacc```\nThe kaid or username should be yours")

        if not id:
            return await ctx.send("This command should be used like\n```k!verify kaid kaid_................``` or\n```k!verify username kacc```\nThe kaid or username should be yours")

        msg = await ctx.send('Checking if the account exists...\nMake sure it isnt a link!')
        phrase = f"Verification #{random.randint(100, 999)}"

        if type.lower() == "kaid":
            data = get_data(f"https://www.khanacademy.org/api/internal/user/profile?kaid={id}&format=pretty")

            if data == None:
                return await msg.edit(content="Invalid kaid... Did you include `kaid_` at the beginning? Please try again")
        
        if type.lower() == "user":
            data = get_data(f"https://www.khanacademy.org/api/internal/user/profile?username={id}&format=pretty")

            if data == None:
                return await msg.edit(content="Invalid username... Please try again")

        await msg.edit(content=f"Account exists! Now please change the bio in your account to `{phrase}`. Once finished send `confirm`, you have 5 minutes.")

        confirmation = await self.client.wait_for("message", check=lambda m: m.author is not self.client.user and m.author is ctx.author, timeout = 300)
        try:
            if confirmation.content.lower() == "confirm":
                #check data
                bio = ""
                if type.lower() == "kaid":
                    data = get_data(f"https://www.khanacademy.org/api/internal/user/profile?kaid={id}&format=pretty")
                    bio = data["bio"]
                if type.lower() == "user":
                    data = get_data(f"https://www.khanacademy.org/api/internal/user/profile?username={id}&format=pretty")
                    bio = data["bio"]
                if bio.lower() == phrase.lower():
                    await database.insert_one({"id":ctx.author.id, "kaid":data["kaid"]})
                    return await ctx.send('Verified!')
                else:
                    return await ctx.send(f'Verification failed.\n```Your bio: {bio}\nWhat it should be: {phrase}```')

            else:
                return await ctx.send('Process cancelled')

        except:
            return await ctx.send('You took too long')

    @commands.command()
    async def profile(self, ctx):
        info = await database.find_one({"id":ctx.author.id})
        if not info:
            return await ctx.send('Set your profile with `k!setprofile`')

        data = get_data(f"https://www.khanacademy.org/api/internal/user/profile?kaid={info['kaid']}&format=pretty")

        await ctx.send(embed=discord.Embed(title="Your Khan Academy Account Info", description=f"```Bio: {data['bio']}\nEnergy Points: {data['points']}```").set_author(name=data["nickname"]))

def setup(client):
    client.add_cog(Profiles(client))
