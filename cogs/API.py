import discord
from discord.ext import commands, menus
import os
from urllib.request import urlopen
import json
import requests
import time
import random
import asyncio
from discord.ext.commands import BucketType, cooldown

linkstoload = ["https://www.khanacademy.org/api/internal/scratchpads/top?casing=camel&sort=3&page=0&limit=30&subject=all&topic_id=xffde7c31&lang=en","https://www.khanacademy.org/api/internal/scratchpads/top?casing=camel&sort=2&page=0&limit=30&subject=all&topic_id=xffde7c31&lang=en","https://www.khanacademy.org/api/internal/scratchpads/top?casing=camel&sort=5&page=0&limit=30&subject=all&topic_id=xffde7c31&lang=en"]

def get_data(url):
    response = urlopen(url)
    data = response.read().decode("utf-8")
    return json.loads(data)

class PaginatorSource(menus.ListPageSource):
    def __init__(self, ctx, entries, *, per_page=10):
        self.ctx = ctx
        super().__init__(entries, per_page=per_page)

    async def format_page(self, menu: menus.Menu, page):
        embed = discord.Embed(title = 'Flags')
        for a in range(len(page)):
            embed.add_field(name=f"Flag {a+1}", value=page[a], inline=False)
        return embed

    def is_paginating(self):
        return True

class Khan(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['l', 'browse', 'b'])
    @commands.cooldown(1, 10, BucketType.user)
    async def list(self, ctx, page = 'hot'):
        if page in ['hot', 'h']:
            toload = linkstoload[0]
        elif page in ['recent', 'r']:
            toload = linkstoload[1]
        elif page in ['votes', 'v']:
            toload = linkstoload[2]
        else:
            return await ctx.send('Thats a invalid list! Select from `[hot | h], [recent | r], [votes | v]`')

        pronum = 1
        data = get_data(toload)
        msg = await ctx.send(embed=discord.Embed(
        description=f'Project: [{data["scratchpads"][pronum-1]["title"]}]({data["scratchpads"][pronum-1]["url"]}) | [{"Created By: "+data["scratchpads"][pronum-1]["authorNickname"]}]({"https://khanacademy.org/profile/"+data["scratchpads"][pronum-1]["authorKaid"]+"/projects"})')
        .add_field(name='\u200b', value="Votes: "+str(data["scratchpads"][pronum-1]["sumVotesIncremented"])+" | "+"Spin Offs: "+str(data["scratchpads"][pronum-1]["spinoffCount"]))
        .set_image(url=data["scratchpads"][pronum-1]["url"]+"/latest.png")
        .set_footer(text=f"Page {pronum}/30")
        .set_author(name='Khan Academy | Browse Projects'))

        for a in ["◀️", "▶️", "⏹️"]:
            await msg.add_reaction(a)

        while True:
            def check(reaction, user):
                return user == ctx.author and str(reaction.emoji) in ("◀️", "▶️", "⏹️") and reaction.message.id == msg.id

            reaction, __ = await self.bot.wait_for('reaction_add', check=check)

            if str(reaction) == "◀️":
                if pronum-1 == 0:
                    pronum = 30
                else:
                    pronum -= 1

                await msg.edit(embed=discord.Embed(
        description=f'Project: [{data["scratchpads"][pronum-1]["title"]}]({data["scratchpads"][pronum-1]["url"]}) | [{"Created By: "+data["scratchpads"][pronum-1]["authorNickname"]}]({"https://khanacademy.org/profile/"+data["scratchpads"][pronum-1]["authorKaid"]+"/projects"})')
        .add_field(name='\u200b', value="Votes: "+str(data["scratchpads"][pronum-1]["sumVotesIncremented"])+" | "+"Spin Offs: "+str(data["scratchpads"][pronum-1]["spinoffCount"]))
        .set_image(url=data["scratchpads"][pronum-1]["url"]+"/latest.png")
        .set_footer(text=f"Page {pronum}/30")
        .set_author(name='Khan Academy | Browse Projects'))

            elif str(reaction) == "▶️":
                if pronum+1 == 31:
                    pronum = 1
                else:
                    pronum += 1

                await msg.edit(embed=discord.Embed(
        description=f'Project: [{data["scratchpads"][pronum-1]["title"]}]({data["scratchpads"][pronum-1]["url"]}) | [{"Created By: "+data["scratchpads"][pronum-1]["authorNickname"]}]({"https://khanacademy.org/profile/"+data["scratchpads"][pronum-1]["authorKaid"]+"/projects"})')
        .add_field(name='\u200b', value="Votes: "+str(data["scratchpads"][pronum-1]["sumVotesIncremented"])+" | "+"Spin Offs: "+str(data["scratchpads"][pronum-1]["spinoffCount"]))
        .set_image(url=data["scratchpads"][pronum-1]["url"]+"/latest.png")
        .set_footer(text=f"Page {pronum}/30")
        .set_author(name='Khan Academy | Browse Projects'))

            elif str(reaction) == "⏹️":
                await msg.delete()
                break

            try:
                await msg.remove_reaction(reaction, ctx.author)
            except:
                pass

    @commands.command(aliases=['u'])
    @commands.cooldown(1, 10, BucketType.user)
    async def user(self, ctx, user : str):
        if "/" in user:
            return await ctx.send('You cant break me nerd')
        user = user.split("&")[0]
        data = get_data(f"https://www.khanacademy.org/api/internal/user/profile?username={user}")
        try:
            await ctx.send(
                embed = discord.Embed(
                    title = data["bio"] or "No Bio",
                    description = f"Account Link: [{data['username']}]({'https://khanacademy.org'+data['childPageRoot']+'projects'})" or "No Account"
                ).set_author(
                    name = data["nickname"] or "No Nickname"
                )
            )
        except Exception as e:
            await ctx.send('Couldnt find that user')

    @commands.command(aliases=['p'])
    @commands.cooldown(1, 10, BucketType.user)
    async def projects(self, ctx, user : str):
        if "/" in user:
            return await ctx.send('You cant break me nerd')

        user = user.split("&")[0]

        toload = f"https://www.khanacademy.org/api/internal/user/scratchpads?username={user}&limit=30"

        try:
            pronum = 1
            data = get_data(toload)
            msg = await ctx.send(embed=discord.Embed(
            description=f'Project: [{data["scratchpads"][pronum-1]["title"]}]({data["scratchpads"][pronum-1]["url"]}) | [{"Created By: "+data["scratchpads"][pronum-1]["authorNickname"]}]({"https://khanacademy.org/profile/"+data["scratchpads"][pronum-1]["authorKaid"]+"/projects"})')
            .add_field(name='\u200b', value="Votes: "+str(data["scratchpads"][pronum-1]["sumVotesIncremented"])+" | "+"Spin Offs: "+str(data["scratchpads"][pronum-1]["spinoffCount"]))
            .set_image(url=data["scratchpads"][pronum-1]["url"]+"/latest.png")
            .set_footer(text=f"Page {pronum}/30")
            .set_author(name=f'Khan Academy | {user} Projects'))

            for a in ["◀️", "▶️", "⏹️"]:
                await msg.add_reaction(a)

            while True:
                def check(reaction, user):
                    return user == ctx.author and str(reaction.emoji) in ("◀️", "▶️", "⏹️") and reaction.message.id == msg.id

                reaction, __ = await self.bot.wait_for('reaction_add', check=check)

                if str(reaction) == "◀️":
                    if pronum-1 == 0:
                        pronum = 30
                    else:
                        pronum -= 1

                    await msg.edit(embed=discord.Embed(
            description=f'Project: [{data["scratchpads"][pronum-1]["title"]}]({data["scratchpads"][pronum-1]["url"]}) | [{"Created By: "+data["scratchpads"][pronum-1]["authorNickname"]}]({"https://khanacademy.org/profile/"+data["scratchpads"][pronum-1]["authorKaid"]+"/projects"})')
            .add_field(name='\u200b', value="Votes: "+str(data["scratchpads"][pronum-1]["sumVotesIncremented"])+" | "+"Spin Offs: "+str(data["scratchpads"][pronum-1]["spinoffCount"]))
            .set_image(url=data["scratchpads"][pronum-1]["url"]+"/latest.png")
            .set_footer(text=f"Page {pronum}/30")
            .set_author(name=f'Khan Academy | {user} Projects'))

                elif str(reaction) == "▶️":
                    if pronum+1 == 31:
                        pronum = 1
                    else:
                        pronum += 1

                    await msg.edit(embed=discord.Embed(
            description=f'Project: [{data["scratchpads"][pronum-1]["title"]}]({data["scratchpads"][pronum-1]["url"]}) | [{"Created By: "+data["scratchpads"][pronum-1]["authorNickname"]}]({"https://khanacademy.org/profile/"+data["scratchpads"][pronum-1]["authorKaid"]+"/projects"})')
            .add_field(name='\u200b', value="Votes: "+str(data["scratchpads"][pronum-1]["sumVotesIncremented"])+" | "+"Spin Offs: "+str(data["scratchpads"][pronum-1]["spinoffCount"]))
            .set_image(url=data["scratchpads"][pronum-1]["url"]+"/latest.png")
            .set_footer(text=f"Page {pronum}/30")
            .set_author(name=f'Khan Academy | {user} Projects'))

                elif str(reaction) == "⏹️":
                    await msg.delete()
                    break

                try:
                    await msg.remove_reaction(reaction, ctx.author)
                except:
                    pass
        except:
            await ctx.send('No Projects Found')

    @commands.command(aliases=['f'])
    @commands.cooldown(1, 10, BucketType.user)
    async def flags(self, ctx, program : int):
        data = get_data(f"https://www.khanacademy.org/api/internal/scratchpads/{program}")
        try:
            if len(data["flags"]) < 1:
                if data["hideFromHotlist"]:
                    message = "No Flags\nHidden from hotlist"
                else:
                    message = "No Flags\nNot hidden from hotlist"
            else:
                allflags = [f"`{a}`" for a in data["flags"]]
                flags = ", ".join(allflags)
                if data["hideFromHotlist"]:
                    message = f"Hidden from hotlist\nFlags: below"
                else:
                    message = f"Not hidden from hotlist\nFlags: below"  

            await ctx.send(
                embed = discord.Embed(
                    title = data["title"],
                    description = message
                )
            )

            if len(data["flags"]) >= 1:
                pages = PaginatorSource(ctx=ctx, entries=allflags)
                paginator = menus.MenuPages(source=pages, timeout=None, delete_message_after=True)
                return await paginator.start(ctx)

        except Exception as e:
            print(e)
            await ctx.send('Couldnt find that project')

    @commands.command(aliases=['random'])
    @commands.cooldown(1, 10, BucketType.user)
    async def comment(self, ctx):
        projects = random.randint(150, 200)
        msg = await ctx.send(f"Fetching {projects} Projects")

        info = get_data("https://www.khanacademy.org/api/internal/scratchpads/top?casing=camel&sort=3&page=0&limit="+str(projects)+"&subject=all&lang=en")
        hotlist = info["scratchpads"]

        await msg.edit(content="Success")

        while True:
            project_id = hotlist[random.randint(0, len(hotlist) - 1)]["url"][-16:]

            await msg.edit(content="Getting project comments")

            project_comments = get_data(f"https://www.khanacademy.org/api/internal/discussions/scratchpad/{project_id}/comments")["feedback"]

            if(len(project_comments) == 0):
                await msg.edit(content="No comments found, retrying")
            else:
                try:
                    comment_data = random.choice(project_comments)
                    author = comment_data['authorNickname']
                    content = comment_data['content']
                    quality = comment_data['lowQualityScore']
                    url = f"https://www.khanacademy.org/computer-programming/-/{project_id}"

                    project_name = get_data('https://www.khanacademy.org/api/internal/scratchpads/'+project_id+'?projection={"title":1}')["title"]
                    await msg.edit(content=None, embed = discord.Embed(title=project_name, description=f"{content}\n[Project Link]({url})").set_author(name=f"{author}").set_footer(text=f"Quality: {quality}"))
                except Exception as e:
                    print(e)
                break

def setup(bot):
    bot.add_cog(Khan(bot))
