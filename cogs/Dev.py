import discord
from discord.ext import commands
from contextlib import redirect_stdout
from PIL import Image
import traceback
import textwrap
import asyncio
import io
import random
import colorsys
import inspect
import datetime
from pyfiglet import figlet_format
import sys
import os
import sqlite3

def start(id):
    database.insert_one({"id": id, "wallet": 0, "bank": 0, "job": None, "inv": ["gift"], "prestige": 0, "multi": 1, "level": 1, "xp": 0, "last_daily":datetime.datetime.strptime("2021-3-3 10:11:12", "%Y-%m-%d %H:%M:%S"), "blacklisted":False, "max_bank": 50000, "powerups":[]})

class Dev(commands.Cog):
    def __init__(self, client):
        self.client = client
        self._last_result = None
        self.text_flip = {}
        self.char_list = "!#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}"
        self.alt_char_list = "{|}zʎxʍʌnʇsɹbdouɯlʞɾᴉɥƃɟǝpɔqɐ,‾^[\]Z⅄XMΛ∩┴SɹQԀONW˥ʞſIHפℲƎpƆq∀@¿<=>;:68ㄥ9ϛㄣƐᄅƖ0/˙-'+*(),⅋%$#¡"[
            ::-1
        ]

    @commands.command(pass_context=True, hidden=True, name="eval", description='Evaluates code')
    @commands.is_owner()
    async def _eval(self, ctx, *, body: str):
        """Evaluates python code"""
        env = {
            "client": self.client,
            "ctx": ctx,
            "channel": ctx.channel,
            "author": ctx.author,
            "guild": ctx.guild,
            "message": ctx.message,
            "_": self._last_result,
            "source": inspect.getsource,
            "s": ctx.send,
            "g": ctx.guild,
            "c": ctx,
        }
        env.update(globals())
        body = self.cleanup_code(body)
        stdout = io.StringIO()
        err = out = None
        to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'
        try:
            exec(to_compile, env)
        except Exception as e:
            err = await ctx.send(f"```py\n{e.__class__.__name__}: {e}\n```")
            return await err.add_reaction("❌")
        func = env["func"]
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            err = await ctx.send(f"```py\n{value}{traceback.format_exc()}\n```")
        else:
            value = stdout.getvalue()
            if ret is None:
                if value:
                    try:
                        out = await ctx.send(f"```py\n{value}\n```")
                    except:
                        paginated_text = ctx.paginate(value)
                        for page in paginated_text:
                            if page == paginated_text[-1]:
                                out = await ctx.send(f"```py\n{page}\n```")
                                break
                            await ctx.send(f"```py\n{page}\n```")
            else:
                self._last_result = ret
                try:
                    out = await ctx.send(f"```py\n{value}{ret}\n```")
                except:
                    paginated_text = ctx.paginate(f"{value}{ret}")
                    for page in paginated_text:
                        if page == paginated_text[-1]:
                            out = await ctx.send(f"```py\n{page}\n```")
                            break
                        await ctx.send(f"```py\n{page}\n```")
        if out:
            await out.add_reaction("✔")
        if err:
            await err.add_reaction("❌")

    def cleanup_code(self, content):
        """Automatically removes code blocks from the code."""
        if content.startswith("```") and content.endswith("```"):
            return "\n".join(content.split("\n")[1:-1])
        return content.strip("` \n")

    def get_syntax_error(self, e):
        if e.text is None:
            return f"```py\n{e.__class__.__name__}: {e}\n```"
        return f'```py\n{e.text}{"^":>{e.offset}}\n{e.__class__.__name__}: {e}```'

    def getColor(self, colorHex):
        colorHex = str(colorHex)
        return discord.Colour(int(f"0x{colorHex[1:]}", 16))

    def randomcolor(self):
        values = [int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1)]
        color = discord.Color.from_rgb(*values)
        return self.getColor(color)

    @commands.command(hidden=True, description='Refreshes the bot')
    @commands.is_owner()
    async def restart(self, ctx):
        await ctx.reply("Restarting...")
        python = sys.executable
        os.execl(python, python, *sys.argv)

def setup(client):
    client.add_cog(Dev(client))
