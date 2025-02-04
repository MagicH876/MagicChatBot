from dotenv import load_dotenv
import os, discord
from discord.ext import commands

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

class HelpCommand(commands.HelpCommand):
    def __init__(self):
        super().__init__()
        self.no_cat = "Other Commands"

    async def send_bot_help(self, mapping):
        """Called when the user inputs the help command with no arguments"""
        embed = discord.Embed(
            tile='Bot Commands', 
            description='Here are the commands you can use:',
            color=discord.Color.dark_purple()
            )
        
        for cog, commands_list in mapping.items():
            filtered = await self.filter_commands(commands_list, sort=True)
            if not filtered:
                continue

            cog_name = cog.qualified_name if cog else self.no_cat
            command_signatures = [self.get_command_signature(c) for c in filtered]
            embed.add_field(
                name=cog_name, value="\n".join(command_signatures), inline=False
            )
        
        destination = self.get_destination()
        await destination.send(embed=embed)

    async def sens_cog_help(self, cog):
        """Called when a category is used after help"""
        embed = discord.Embed(
            title=f"{cog.qualified_name} Commands",
            description=cog.description or "No description provided.",
            color=discord.Color.dark_purple()
        )
        filtered = await self.filter_commands(cog.get_commands(), sort=True)
        if filtered:
            for command in filtered:
                embed.add_field(
                    name=self.get_command_signature(command), 
                    value=command.help or "No help provided",
                    inline=False
                )
        else:
            embed.add_field(
                name="No commands",
                value="No available commands in this category",
                inline=False
            )
        
        destination = self.get_destination()
        await destination.send(embed=embed)

@bot.event
async def on_ready():
    print(f"Logged as {bot.user}  :  ID {bot.user.id}\n")

bot.run(TOKEN)