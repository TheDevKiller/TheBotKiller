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

    return trad[config[str(ctx.message.guild.id)]["lang"]][txt]

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
        global thedevkiller

        thedevkiller = await bot.get_user_info(436105272310759426)

        print("Je suis connecté !")

        # Présence
        #await bot.change_presence(activity=discord.Streaming("&help"))
        
        # Charger les cogs
        for fichier in os.listdir("cogs"):
            if re.match(r".*\.py.swp", fichier):
                pass
            elif re.match(r".*\.py", fichier):
                print("Chargement de " + fichier)
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

        print("------------")

# Halt
@bot.command(name="halt", aliases=["shutdown"], brief="Éteint le bot")
async def halt(ctx):
        if ctx.message.author == thedevkiller:
            with open("config.json", "r") as fichier:
                config = json.loads(fichier.read())
            await ctx.send(getmsg(ctx, "shutdown"))
            sys.exit(0)
        else:
                await ctx.send(trad[config[str(ctx.message.guild.id)]["lang"]]["youcant"])

# Reboot
@bot.command(name="reboot", brief="Redémarre le bot", usage="reboot")
async def reboot(ctx):
        if ctx.message.author == thedevkiller:
                print("Je redémarre")
                await ctx.send(getmsg(ctx, "reboot"))
                subprocess.call(["bash", "/home/thedevkiller/TheBotKiller/reboot.sh"])
                sys.exit(0)
        else:
                await ctx.send(getmsg(ctx, "youcant"))
        
# Load        
@bot.command(name="load", aliases=["charge"], brief="Charge un module")
async def load(ctx, arg):
        if ctx.message.author == thedevkiller:
                try:
                        bot.load_extension("cogs." + arg)
                        await ctx.send(getmsg(ctx, "loaded").format(arg))  
                except ModuleNotFoundError:
                    await ctx.send(getmsg(ctx, "idonthavemodule"))
        else:
                await ctx.send(getmsg(ctx, "youcant"))

# Reload
@bot.command(name="reload", aliases=["recharge"], brief="Recharge un module")
async def reload(ctx, arg):
        if ctx.message.author == thedevkiller:
                try:
                        bot.unload_extension("cogs." + arg)
                        bot.load_extension("cogs." + arg)
                        await ctx.send(getmsg(ctx, "reloaded").format(arg))
                except ModuleNotFoundError:
                        await ctx.send(getmsg(ctx, "idonthavemodule"))
        else:
                await ctx.send(getmsg(ctx, "youcant"))

# Unload
@bot.command(name="unload", aliases=["décharge"], brief="Décharge un module")
async def unload(ctx, arg):
        if ctx.message.author == thedevkiller:
                try:
                        bot.unload_extension("cogs." + arg)
                        await ctx.send(getmsg(ctx, "unloaded").format(arg))
                except ModuleNotFoundError:
                        await ctx.send(getmsg(ctx, "unloaded"))
        else:
                await ctx.send(getmsg(ctx, "youcant"))

# Erreurs
@bot.event
async def on_error(event, *args, **kwargs):
    
    message = args[0]
    em = discord.Embed(title="C'est con !", description="```python\n{}\n```".format(traceback.format_exc()), color=0xff0000)
    
    await thedevkiller.send(embed=em)

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
        await ctx.send(trad[config[str(ctx.message.guild.id)]["lang"]]["noavailableset"])

# Replace help
@bot.command(aliases=["aide"], usage="(help|aide)")
async def help(ctx):

    em = discord.Embed(title=getmsg(ctx, "helptitlembed"))

    await ctx.send(embed=em)

# Logs
@bot.event
async def on_command(ctx):
    print("[COMMAND][%s]: %s, %s, %s"%(time.asctime(), ctx.message.content, ctx.message.author.name, ctx.message.guild))

bot.run(secrets["token"])
