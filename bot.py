import discord
from os import getenv
from discord.app_commands import command
from discord.ext import commands
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!',intents=intents)

class RZERO(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name='group')
    async def create_group(self, interaction):
        print(interaction)
        await interaction.response.send_message('Group created!')
def run_bot():
    token = getenv('DISCORD_TOKEN')
    bot.add_cog(RZERO(bot))
    print(bot.all_commands)
    bot.run(token)