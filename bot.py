import eliza
import discord
from discord.ext import commands

import os


client = commands.Bot(command_prefix="!", intents=discord.Intents.all())
 
sessions = {}
 
def speak(instance, message):
    response = instance.respond(message)
    return response
 
@client.event
async def on_message(message):
    client_id = message.author.id
    if client_id in sessions and not message.content.lower().startswith('!start'):
        if message.content == "bye":
            await message.reply(sessions[client_id].final())
            del sessions[client_id]
            return
        await message.reply(speak(sessions[client_id], message.content), mention_author=False)
    await client.process_commands(message)
 
@client.command()
async def start(ctx, script='doctor'):
    client_id = ctx.message.author.id
                            
    if client_id in sessions:
        await ctx.reply("You already have an ELIZA session running. Please say 'bye' to ELIZA to end your current session")
        return
    else:
        bot = eliza.Eliza()
        bot.load(f'./scripts/{script}.txt')
        sessions.update({client_id: bot})
        await ctx.reply(bot.initial())
        return
 
client.run(os.environ['BOT_TOKEN'])