###########
# Imports #
###########

import discord
from discord.ext import commands

#############
# Fonctions #
#############

def ri(string):
	string = list(string)
	for index, char in enumerate(string):
		char = char.lower()
		letters = "abcdefghijklmnopqrstuvwxyz"
		numbers = "123456789"
		if char in letters:
			string[index] = ":regional_indicator_" + char + ":"
		elif char in numbers:
			emojis = \
			{"1": ":one:",
			"2": ":two:",
			"3": ":three:",
			"4": ":four:",
			"5": ":five:",
			"6": ":six:",
			"7": ":seven",
			"8": ":eight:",
			"9": ":nine:"}
			string[index] = emojis[char]
		elif char == " ":
			string[index] = "    "
	string = "".join(string)
	return string
	

########
# Code #
########

class Discussions:
	
	def __init__(self, bot):
		self.bot = bot

	async def on_message(self, message):
	
		if "kop1 cha" in message.content:
			await message.channel.send(ri("kop1 cha mraw") + "    :smiley_cat:")

		elif "mraw" in message.content:
			await message.channel.send(ri("mraw"))

		elif "kop1" in message.content:
			await message.channel.send(ri("kop1"))

def setup(bot):
	bot.add_cog(Discussions(bot))
