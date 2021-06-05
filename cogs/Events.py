import discord
from discord.ext import commands
from discord.ext.commands import BucketType, cooldown

def getconv(arg):
    final = "Unknown Argument"
    if arg == "str":
        final = "Text"
    if arg == "int":
        final = "a Number"
    return final

class Events(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.cd_mapping = commands.CooldownMapping.from_cooldown(1, 5, commands.BucketType.member)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        bucket = self.cd_mapping.get_bucket(ctx)
        retry_after = bucket.update_rate_limit()
        if retry_after:
            return
        if isinstance(error, commands.CommandNotFound):
            return 
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send('You dont have the required permission to use this command')
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f'Woah calm down there, this command has a cooldown! Retry in {round(error.retry_after)} seconds.')
        elif isinstance(error, commands.MemberNotFound):
            await ctx.send(f'I couldnt find this member')
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'That isnt the proper usage of `{ctx.command}`\nUsage: `{ctx.command} {ctx.command.signature}`')
        elif isinstance(error, commands.NotOwner):
            await ctx.send(f'Only the owner is allowed to use this command.')
        elif isinstance(error, commands.BadArgument):
            sep = '\"'
            await ctx.send(f"I couldnt convert `Argument: {str(error).split(sep)[3]}` in `Command: {ctx.command}` into `{getconv(str(error).split(sep)[1])}`")
    
    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        try:
            if ctx.author.id == 801010311552958464:
                ctx.command.reset_cooldown(ctx)
        except:
            pass

def setup(client):
    client.add_cog(Events(client))
