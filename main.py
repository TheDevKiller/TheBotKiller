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

#############
# Fonctions #
#############

def prefixe(bot, message):
    with open("config.json", "r") as fichier:
        config = json.loads(fichier.read())
        try:
            return config[str(message.guild.id)]["prefixe"]
        except:
            return "&"

def getmsg(ctx, txt):
    with open("config.json", "r") as fichier:
        config = json.loads(fichier.read())

    return trad[config[str(ctx.message.guild.id)]["lang"]][txt]

#############
# Variables #
#############

bot = commands.Bot(command_prefix=prefixe)

with open("secrets.json", "r") as fichier:
        secrets = json.loads(fichier.read())

defaultConfig = \
{"prefixe": "&",
"lang": "en"}

with open("trads.json", "r") as fichier:
    trad = json.loads(fichier.read())

##############
# Coroutines #
##############

#bot.remove_command("help")

@bot.event
async def on_ready():
        global thedevkiller
        print("Je suis connecté !")
        thedevkiller = await bot.get_user_info(436105272310759426)
        for fichier in os.listdir("cogs"):
            if re.match(r".*\.py.swp", fichier):
                pass
            elif re.match(r".*\.py", fichier):
                print("Chargement de " + fichier)
                bot.load_extension("cogs." + fichier.replace(".py", ""))
        with open("config.json", "r") as fichier:
            config = json.loads(fichier.read())
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

@bot.command(name="halt", aliases=["shutdown"], brief="Éteint le bot")
async def halt(ctx):
        if ctx.message.author == thedevkiller:
            with open("config.json", "r") as fichier:
                config = json.loads(fichier.read())
            await ctx.send(getmsg(ctx, "shutdown"))
            sys.exit(0)
        else:
                await ctx.send(trad[config[str(ctx.message.guild.id)]["lang"]]["youcant"])

@bot.command(name="reboot", brief="Redémarre le bot")
async def reboot(ctx):
        if ctx.message.author == thedevkiller:
                print("Je redémarre")
                await ctx.send(getmsg(ctx, "reboot"))
                subprocess.call("./reboot.sh")
                sys.exit(0)
        else:
                await ctx.send(getmsg(ctx, "youcant"))
        
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

#@commands.command(name="cogs", aliases=["modules"], brief="Liste des modules")
#async def cogs(ctx):

@bot.command(aliases=["config"])
async def conf(ctx, param, valeur):
    if param in defaultConfig:
        with open("config.json", "r") as fichier:
            config = json.loads(fichier.read())
        config[str(ctx.message.guild.id)][param] = valeur
        with open("config.json", "w") as fichier:
            fichier.write(json.dumps(config, indent=4))
    else:
        await ctx.send(trad[config[str(ctx.message.guild.id)]["lang"]]["noavailableset"])

#@bot.command()
#async def help(ctx):
#    for command in bot.commands:
#        if command.cog_name == None: cog_name = getmsg(ctx, "nocathelp")
#        if 
#        print(command.name + " " + command.cog_name)

@bot.event
async def on_command(ctx):
        print("{author} a dit \"{msg}\" sur le serveur {serveur}".format(author=ctx.message.author.name, msg=ctx.message.content, serveur=ctx.message.guild.name))

bot.run(secrets["token"])
