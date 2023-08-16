import disnake
from disnake.ext import commands
import json
import random
import time


with open('questions.json', encoding='utf-8') as f:
    questions = json.load(f)

intents = disnake.Intents.all()
bot = commands.Bot(intents=intents, command_prefix="!")

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command()
async def quiz(ctx):
    question = random.choice(list(questions.keys()))
    await ctx.send(f'Question: {question}')
    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel
    try:
        start_time = time.time()
        answer = await bot.wait_for('message', check=check, timeout=60)
        end_time = time.time()
    except TimeoutError:
        await ctx.send(f"Time up! Answer: {answer}")
        return
    if answer.content == questions[question]:
        duration = round(end_time - start_time, 2)
        embed = disnake.Embed(title='Result', color=disnake.Color.green())
        embed.set_author(name=answer.author.name, icon_url=answer.author.avatar.url)
        embed.add_field(name='Answer', value=answer.content, inline=False)
        embed.add_field(name='Time', value=f'{duration} seconds', inline=False)
        await ctx.send('Correct!', embed=embed)
        return
    else:
        await ctx.send(f"Answer: {answer}")

bot.run("TOKEN")
