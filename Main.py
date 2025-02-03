from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
DGAPI = os.getenv('DGAPI_KEY')
GPTAPI = os.getenv('GPTAPI_KEY')

print(f"BOT TOKEN: {TOKEN}")
print(f"DGAPI KEY: {DGAPI}")
print(f"GPTAPI KEY: {GPTAPI}")