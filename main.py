#!/usr/bin/python3
#-*- coding: utf8 -*-

###########
# Imports #
###########

import discord
from discord.ext import commands
import json
import subprocess
import sys
import traceback
import os
import re
import time
import threading
import asyncio
from termcolor import colored
from sanic import Sanic, response

#############
# Fonctions #
#############

# Préfixe
def prefixe(bot, message): 
    with open("config.json", "r") as fichier:
        config = json.loads(fichier.read())
        try:
            return config[str(message.guild.id)]["prefixe"]
        except:
            return "&"

# Traductions
def getmsg(ctx, txt):
    with open("config.json", "r") as fichier:
        config = json.loads(fichier.read())
    try:
        return trad[config[str(ctx.message.guild.id)]["lang"]][txt]
    except:
        return " "

#############
# Variables #
#############

bot = commands.Bot(command_prefix=prefixe)

# Secrets
with open("secrets.json", "r") as fichier:
        secrets = json.loads(fichier.read())

# Config
defaultConfig = \
{"prefixe": "&",
"lang": "en"}

# Traductions
with open("trads.json", "r") as fichier:
    trad = json.loads(fichier.read())

##############
# Coroutines #
##############

bot.remove_command("help")

# On ready
@bot.event
async def on_ready():
    # Moi
    bot.owner = await bot.get_user_info(436105272310759426)
    print(colored("Je suis connecté !", "white"))
    # Présence
    await bot.change_presence(status=discord.Status.dnd, activity=discord.Activity(name="&help", type=discord.ActivityType.listening), afk=False)
    # Charger les cogs
    for fichier in os.listdir("cogs"):
        if re.match(r".*\.py.swp", fichier):
            pass
        elif re.match(r".*\.py", fichier):
            print(colored("Chargement de " + fichier, "white"))
            bot.load_extension("cogs." + fichier.replace(".py", ""))
    # Chargement de la config
    with open("config.json", "r") as fichier:
        config = json.loads(fichier.read())
    # Config par défaut
    for server in bot.guilds:
        if str(server.id) in config:
            for param in defaultConfig:
                if not param in config[str(server.id)]:
                    config[str(server.id)][param] = defaultConfig[param]
        else:
            config[str(server.id)] = defaultConfig
    with open("config.json", "w") as fichier:
        fichier.write(json.dumps(config, indent=4))
    # Séparateur
    print("------------")

# Halt
@bot.command(name="halt", aliases=["shutdown"])
async def halt(ctx):
    if ctx.message.author == bot.owner:
        with open("config.json", "r") as fichier:
            config = json.loads(fichier.read())
        await ctx.send(getmsg(ctx, "I must get away"))
        sys.exit(0)
    else:
                await ctx.send(trad[config[str(ctx.message.guild.id)]["lang"]]["youcant"])

# Reboot
@bot.command(name="reboot", usage="reboot")
async def reboot(ctx):
    if ctx.message.author == bot.owner:
        print("Je redémarre")
        await ctx.send(getmsg(ctx, "I'll be back very soon"))
        subprocess.call(["bash", "~/code/python/TheBotKiller/reboot.sh"])
        sys.exit(0)
    else:
        await ctx.send(getmsg(ctx, "You can't do this"))
        
# Load        
@bot.command(name="load", aliases=["charge"])
async def load(ctx, arg):
    if ctx.message.author == bot.owner:
        try:
            bot.load_extension("cogs." + arg)
            await ctx.send(getmsg(ctx, "Module loaded").format(arg))  
        except ModuleNotFoundError:
            await ctx.send(getmsg(ctx, "Sorry but I don't have this module"))
    else:
        await ctx.send(getmsg(ctx, "You can't do this"))

# Reload
@bot.command(name="reload", aliases=["recharge"])
async def reload(ctx, arg):
    if ctx.message.author == bot.owner:
        try:
            bot.unload_extension("cogs." + arg)
            bot.load_extension("cogs." + arg)
            await ctx.send(getmsg(ctx, "Module reloaded").format(arg))
        except ModuleNotFoundError:
            await ctx.send(getmsg(ctx, "Sorry but I don't have this module"))
    else:
        await ctx.send(getmsg(ctx, "You can't do this"))

# Unload
@bot.command(name="unload", aliases=["décharge"])
async def unload(ctx, arg):
    if ctx.message.author == bot.owner:
        try:
            bot.unload_extension("cogs." + arg)
            await ctx.send(getmsg(ctx, "Module unloaded").format(arg))
        except ModuleNotFoundError:
            await ctx.send(getmsg(ctx, "Module unloaded"))
    else:
        await ctx.send(getmsg(ctx, "Sorry but I don't have this module"))

# Commande qui génère des erreurs
@bot.command(name="error", aliases=["erreur"])
async def error(ctx):
    raise NameError("lol")

# Erreurs
@bot.event
async def on_error(event, *args, **kwargs):
    err = traceback.format_exc()
    print(colored(err, "red"))
    try:
        message = args[0]
        await message.channel.send(getmsg(ctx, "An error happened"))
        await bot.owner.send(err)
    except:
        pass
    try:
        commande = message.content.split(" ")[0]
    except: 
        commande = " "

# Erreurs de commandes
@bot.event
async def on_command_error(ctx, ex):
    if isinstance(ex, commands.CommandNotFound):
        pass
    elif isinstance(ex, commands.MissingRequiredArgument) or isinstance(ex, commands.BadArgument):
        em = discord.Embed(title=getmsg(ctx, "Usage of the command"), description="`" + ctx.command.usage+ "`", color=0xEA2027)
        em.set_footer(text=getmsg(ctx, "If you think this error is abnormal"))
        await ctx.send(embed=em)
    else:
        await bot.owner.send("[" + ctx.command.name + "] " + str(ex))
        await ctx.send(ex)

## Cogs chargées
#@commands.command(name="cogs", aliases=["modules"], brief="Liste des modules")
#async def cogs(ctx):

# Config
@bot.command(aliases=["config"], usage="(conf|config) setting value")
async def conf(ctx, param, valeur):
    if param in defaultConfig:
        with open("config.json", "r") as fichier:
            config = json.loads(fichier.read())
        config[str(ctx.message.guild.id)][param] = valeur
        with open("config.json", "w") as fichier:
            fichier.write(json.dumps(config, indent=4))
    else:
        await ctx.send(getmsg(ctx, "noavailableset"))

# Help
@bot.command(aliases=["aide"], usage="(help|aide)")
async def help(ctx, arg="defaultarg"):
    if arg == "defaultarg":
        dico = {}
        em = discord.Embed(title=getmsg(ctx, "List of available commands"), color=0xff0000)
        for commande in bot.commands:
            if commande.hidden == False:
                if not commande.cog_name in dico:
                    dico[commande.cog_name] = []
                dico[commande.cog_name].append("`" + commande.name + "`: " + getmsg(ctx, commande.name))
        for index, categorie in enumerate(dico):
            if categorie == None:
                em.add_field(name="Main", value="\n".join(dico[categorie]))
            else:
                em.add_field(name=categorie, value="\n".join(dico[categorie]))
            em.set_footer(text=getmsg(ctx, "Most of the commands are also available in french with aliases, to get more info on a command, do `help command`"))
        await ctx.send(embed=em)
    else:
        for commande in bot.commands:
            if commande.name == arg:
                em = discord.Embed(title=commande.name.capitalize(), description=getmsg(ctx, commande.name), color=0xff0000)
                if commande.aliases != []:
                    em.add_field(name="Aliases", value=", ".join(commande.aliases))
                if isinstance(commande.usage, str):
                    n = "\n"
                    em.add_field(name="Usage", value="`\n" + command.usage + "\n`")
                if isinstance(commande.cog_name, str):
                    em.add_field(name="Category", value=commande.cog_name)
                await ctx.send(embed=em)

# Logs
@bot.event
async def on_command(ctx):
    if ctx.message.guild:
        if len(ctx.message.guild.name) > 15:
            guild = ""
            for word in ctx.message.guild.name.split(" "):
                guild += word[0].upper()
        else:
            guild = ctx.message.guild.name
    else:
        guild = "PM"
    print("[" + colored("COMMAND", "green") + "][" + colored(time.asctime(), "yellow") + "]: " + colored(guild, 'blue') + ", " + colored(ctx.message.author.name, 'red') + ", " + ctx.message.content)

# Web server
app = Sanic()

# Generate the HTML page
def html(text):
    return """
    <head>
        <meta charset="utf-8" />
        <style>
            img {
                width: 200px
            }
            p {
                font: "DejaVu";
                align: center;
            }
        </style>
    </head>
    <body>
        <img src="https://cdn.discordapp.com/avatars/462604575514558465/e9b219da4ba57d934323f28922af2670.png?size=2048" />
        <p>""" + text + """</p>
    </body>
    """

# Say command
@app.route("/say/<servId>/<chanId>/<msg>")
async def index(req, servId, chanId, msg):
    serv = bot.get_guild(int(servId))
    chan = serv.get_channel(int(chanId))
    await chan.send(msg)
    return response.html(html("Message successfully sended"))

# Getchans
@app.route("/getchans")
async def index(req):
    dic = []
    for i, server in enumerate(bot.guilds):
        dic.append({"name": server.name, "id": string(server.id), "channels": []})
        for channel in server.channels:
            dic[i]["channels"].append({"name": channel.name, "id": string(channel.id)})
    return response.json(dic, headers={"Access-Control-Allow-Origin": "*"})

# Test
@bot.command()
async def test(ctx):
    print(ctx.guild.id)

# Bot
botApp = bot.start(secrets["token"])
botTask = asyncio.ensure_future(botApp)

# Webserver
webserver = app.create_server(host="localhost", port=8080)
webserverTask = asyncio.ensure_future(webserver)

# Start both
loop = asyncio.get_event_loop()
loop.run_forever()
