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
        embed = discord.Embed(
            title = "my links",
            description = "[Invite Link](https://discord.com/oauth2/authorize?client_id=845503955038896128&permissions=0&scope=bot)\n[Website](https://KhanBot.justbeveb.repl.co)"
        )
        await ctx.send(embed=embed)

    @commands.command(description='Shows the bots latency/response time\nUsage: ping\nAliases: None')
    @commands.cooldown(1, 3, BucketType.user)
    async def ping(self, ctx):
        channel = ctx.message.channel
        t1 = time.perf_counter()
        await channel.trigger_typing()
        t2 = time.perf_counter()
        embed=discord.Embed(title=None, description='Ping: {} MS'.format(round((t2-t1)*1000)))
        await channel.send(embed=embed)

    @commands.command()
    async def info(self, ctx):
        embed = discord.Embed(
            title = "Starky Bot",
            description = f"```Guilds: {len(client.guilds)}\nUnique Users: {len(client.users)}\nOwner: Drained#5313\n[Website](https://KhanBot.justbeveb.repl.co)```"
        )

def setup(client):
    client.add_cog(General(client))
