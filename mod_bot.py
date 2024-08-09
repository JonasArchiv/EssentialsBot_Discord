import discord
from discord.ext import commands
from discord import app_commands

TOKEN = 'YOUR_BOT_TOKEN'
MODERATOR_ROLE_NAME = 'MODERATOR'

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=';', intents=intents)


@bot.event
async def on_ready():
    print(f'Bot eingeloggt als {bot.user}')
    tree = bot.tree
    await tree.sync()


@bot.tree.command(name='kick', description='Kicke ein Mitglied vom Server')
@app_commands.describe(member='Das Mitglied, das gekickt werden soll', reason='Der Grund für das Kicken')
async def kick(interaction: discord.Interaction, member: discord.Member, reason: str = None):
    if not any(role.name == MODERATOR_ROLE_NAME for role in interaction.user.roles):
        await interaction.response.send_message('Du hast nicht die Berechtigung, diesen Befehl auszuführen.',
                                                ephemeral=True)
        return
    await member.kick(reason=reason)
    await interaction.response.send_message(f'{member} wurde gekickt. Grund: {reason}')


@bot.tree.command(name='ban', description='Banne ein Mitglied vom Server')
@app_commands.describe(member='Das Mitglied, das gebannt werden soll', reason='Der Grund für das Bannen')
async def ban(interaction: discord.Interaction, member: discord.Member, reason: str = None):
    if not any(role.name == MODERATOR_ROLE_NAME for role in interaction.user.roles):
        await interaction.response.send_message('Du hast nicht die Berechtigung, diesen Befehl auszuführen.',
                                                ephemeral=True)
        return
    await member.ban(reason=reason)
    await interaction.response.send_message(f'{member} wurde gebannt. Grund: {reason}')


@bot.tree.command(name='unban', description='Hebe den Ban eines Users auf')
@app_commands.describe(member='Das Mitglied, dessen Bann aufgehoben werden soll')
async def unban(interaction: discord.Interaction, member: discord.User):
    if not any(role.name == MODERATOR_ROLE_NAME for role in interaction.user.roles):
        await interaction.response.send_message('Du hast nicht die Berechtigung, diesen Befehl auszuführen.',
                                                ephemeral=True)
        return
    banned_users = await interaction.guild.bans()
    for banned_entry in banned_users:
        user = banned_entry.user
        if user == member:
            await interaction.guild.unban(user)
            await interaction.response.send_message(f'{user} wurde entbannt.')
            return
    await interaction.response.send_message(f'{member} wurde nicht gefunden.')


bot.run(TOKEN)
