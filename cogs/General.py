import discord
from discord.ext import commands
from discord.ext.commands import BucketType, cooldown
import os

class General(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.cd_mapping = commands.CooldownMapping.from_cooldown(1, 45, commands.BucketType.member)

    @commands.command()
    async def invite(self, ctx):
        await ctx.send("https://discord.com/oauth2/authorize?client_id=845503955038896128&permissions=0&scope=bot\nWebsite: https://KhanBot.justbeveb.repl.co")

def setup(client):
    client.add_cog(General(client))
