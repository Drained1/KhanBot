import discord
from discord.ext import commands
import os
import app

bot = commands.Bot(command_prefix=['ka ', 'KA', 'Ka', 'kA'], case_insensitive=True, help_command=None)

@bot.event
async def on_ready():
    print('Online')

for filename in os.listdir('./cogs'):
	if filename.endswith('.py'):
		bot.load_extension(f'cogs.{filename[:-3]}')

@bot.command(hidden=True)
@commands.is_owner()
async def load(ctx, extension):
	bot.load_extension(f'cogs.{extension}')
	await ctx.send(f'Loaded {extension}')


@bot.command(hidden=True)
@commands.is_owner()
async def unload(ctx, extension):
	bot.unload_extension(f'cogs.{extension}')
	await ctx.send(f'Unloaded {extension}')


@bot.command(hidden=True)
@commands.is_owner()
async def reload(ctx, extension):
	bot.unload_extension(f'cogs.{extension}')
	bot.load_extension(f'cogs.{extension}')
	await ctx.send(f'Reloaded {extension}')

app.start()
bot.run(os.environ.get('TOKEN'))