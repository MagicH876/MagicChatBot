from dotenv import load_dotenv
import os, discord
from discord.ext import commands

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f"Logged as {bot.user}  :  ID {bot.user.id}\n")

bot.run(TOKEN)