import discord
import youtube_dl
import os
import json
import requests
from bs4 import BeautifulSoup
from mcstatus import MinecraftServer
from asyncio import sleep
from discord.ext import commands
from discord.utils import get
from discord_components import DiscordComponents, Button,  ButtonStyle

#-----------DiscordComponents-----------
bot = commands.Bot(command_prefix='!', intents = discord.Intents.all())


@bot.event
async def on_ready():
    DiscordComponents(bot)
    print("Logged in as")
    print(bot.user.name)
    print(bot.user.id)
    print("---------")
    while True:
        server = MinecraftServer("localhost", 25545)
        query = server.query()
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,
                                  name=f"онлайн сервера {query.players.online}/12000"))
        await sleep(15)


@bot.command(name = "srv")
async def _server(ctx, nick):
    #----------parsing----------
    event = str(BeautifulSoup(requests.get("https://belkinark.github.io/events/index.html").text, "html.parser").find("h1")).replace("<h1>", "").replace("</h1>", "")
    date = str(BeautifulSoup(requests.get("https://belkinark.github.io/events/index.html").text, "html.parser").find("h2")).replace("<h2>", "").replace("</h2>", "")
    version = str(BeautifulSoup(requests.get("https://belkinark.github.io/events/index.html").text, "html.parser").find("h3")).replace("<h3>", "").replace("</h3>", "")
    time = str(BeautifulSoup(requests.get("https://belkinark.github.io/events/index.html").text, "html.parser").find("h4")).replace("<h4>", "").replace("</h4>", "")
    discript = str(BeautifulSoup(requests.get("https://belkinark.github.io/events/index.html").text, "html.parser").find("h5")).replace("<h5>", "").replace("</h5>", "")
    img = str(BeautifulSoup(requests.get("https://belkinark.github.io/events/index.html").text, "html.parser").find("h6")).replace("<h6>", "").replace("</h6>", "")


    #----------server----------
    server = MinecraftServer("localhost", 25545)
    query = server.query()
    players = ", ".join(query.players.names)


    #----------funcs----------
    if nick.lower() in players.lower():
        online = f"Игрок {nick} сейчас играет на сервере!"
        emb = discord.Embed(
                            title = "NootiPlay",
                            url = "http://www.nootipland.online/Play.html",
                            description = online,
                            color = discord.Color.orange()
                            )
        emb.set_thumbnail(url = "http://www.nootipland.online/icon/NootiPlay.png")
        emb.add_field(name = "Онлайн:", value = f"{query.players.online}/12000")
        emb.add_field(name = "Версия", value = f"{query.software.version}")
        emb.add_field(name = "Ближайший ивент:", value = event)
        await ctx.send(embed = emb)


    elif nick == "event":
        emb = discord.Embed(
                            title = "NootiPlay",
                            description = event,
                            url = "http://www.nootipland.online/Play.html",
                            color = discord.Color.orange()
                            )
        emb.set_thumbnail(url = "http://www.nootipland.online/icon/NootiPlay.png")
        emb.add_field(name = "Дата:", value = date)
        emb.add_field(name = "Версия:", value = version)
        emb.add_field(name = "Время начала:", value = time)
        emb.add_field(name = "Описание:", value = discript)
        emb.set_image(url = img)
        await ctx.send(embed = emb)


    elif nick == "info":
        emb = discord.Embed(
                            title = "NootiPlay",
                            url = "http://www.nootipland.online/Play.html",
                            color = discord.Color.orange()
                            )
        emb.set_thumbnail(url = "http://www.nootipland.online/icon/NootiPlay.png")
        emb.add_field(name = "Ближайший ивент:", value = event)
        emb.add_field(name = "Версия", value = f"{query.software.version}")
        emb.add_field(name = "Онлайн:", value = f"{query.players.online}/12000")
        await ctx.send(embed = emb)


    else:
        offline = f"Игрок {nick} не в сети("
        emb = discord.Embed(
                            title = "NootiPlay",
                            url = "http://www.nootipland.online/Play.html",
                            description = offline,
                            color = discord.Color.orange()
                            )
        emb.set_thumbnail(url = "http://www.nootipland.online/icon/NootiPlay.png")
        emb.add_field(name = "Онлайн:", value = f"{query.players.online}/12000")
        emb.add_field(name = "Версия", value = f"{query.software.version}")
        emb.add_field(name = "Ближайший ивент:", value = event)
        await ctx.send(embed = emb)



bot.run("TOKEN")
