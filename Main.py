from dotenv import load_dotenv
import os, discord
from discord.ext import commands

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

class HelpCommand(commands.HelpCommand):
    def __init__(self):
        super().__init__()
        self.no_cat = "Other Commands"

    async def send_bot_help(self, mapping):
        """Called when the user inputs the help command with no arguments."""
        embed = discord.Embed(
            title='Bot Commands', 
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

    async def send_cog_help(self, cog):
        """Called when a category is used after help."""
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

    async def send_command_help(self, command):
        """Called when asked for help on a specific command."""
        embed = discord.Embed(
            title=self.get_command_signature(command),
            description=command.help or "No help provided.",
            color=discord.Color.dark_purple()
        )
        destination = self.get_destination()
        await destination.send(embed=embed)

    async def send_error_message(self, error):
        """Called when a help error happens."""
        destination = self.get_destination()
        await destination.send(error)

bot = commands.Bot(command_prefix='!', intents=intents, help_command=HelpCommand())

# NOTE : Add cogs into on_ready() event

@bot.event
async def on_ready():
    print(f"Logged as {bot.user}  :  ID {bot.user.id}\n")
    await bot.add_cog(MathCog(bot))
    await bot.add_cog(UtilityCog(bot=bot))

class UtilityCog(commands.Cog, name="Utility Commands"):
    """Commands for interacting with the server."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ping", help="Pings the bot.")
    async def ping(self, ctx):
        """Checks the bots latency"""
        latency = round(bot.latency * 1000)
        await ctx.send(f"# Pong!\n### Latency: `{latency}ms`")

    @commands.command(name="memberInfo", help="Provides member info for yourself or another user.")
    async def memberInfo(self, ctx):
        """Fetches general info about a user"""
        mentions = ctx.message.mentions
        if not mentions:
            guildUser = ctx.author
            user = await bot.fetch_user(guildUser.id)
        else:
            guildUser = ctx.message.mentions[0]
            user = await bot.fetch_user(guildUser.id)

        if user.banner:
            banner = user.banner.url
        else:
            banner = "User has no banner."

        if guildUser.status == discord.Status.online:
            userColor = discord.Color.green()
        elif guildUser.status == discord.Status.idle:
            userColor = discord.Color.gold()
        elif guildUser.status == discord.Status.dnd:
            userColor = discord.Color.red()
        else:
            userColor = discord.Color.dark_gray()

        embed = discord.Embed(
            title = "User Info:",
            color = userColor
            )

        embed.add_field(
            name = "userId",
            value = guildUser.id,
            inline = False
        )

        embed.add_field(
            name = "username",
            value = guildUser.name,
            inline = False
        )

        embed.add_field(
            name = "nick",
            value = guildUser.nick,
            inline = False
        )

        embed.add_field(
            name = "banner",
            value = banner,
            inline = False
        )

        embed.add_field(
            name = "username",
            value = user.avatar.url,
            inline = False
        )

        embed.add_field(
            name = "activity",
            value = guildUser.activity,
            inline = False
        )

        embed.add_field(
            name = "status",
            value = guildUser.status,
            inline = False
        )

        embed.add_field(
            name = "roles",
            value = str(len(guildUser.roles)),
            inline = False
        )

        await ctx.send(embed=embed)

# THE FOLLOWING IS PREGENERATED TESTING CONTENT THIS IS NOT FINALIZED.

# Example command in the default (no cog) category
@bot.command(help="Says hello!")
async def hello(ctx):
    """Greets the user."""
    await ctx.send(f"Hello {ctx.author.mention}!")

# Example cog with a command
class MathCog(commands.Cog, name="Math Commands"):
    """Commands for math operations."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(help="Adds two numbers.")
    async def add(self, ctx, a: float, b: float):
        """Adds two numbers and returns the result."""
        result = a + b
        await ctx.send(f"The result is {result}")

# Adding the cog to the bot

bot.run(TOKEN)