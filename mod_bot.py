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


@bot.tree.command(name='zahlenraten', description='Spiele ein kleines Zahl-raten-Spiel.')
async def zahlenraten(interaction: discord.Interaction):
    zahl = random.randint(1, 10)

    embed = discord.Embed(
        title="Zahlenraten Spiel",
        description="Ich habe eine Zahl zwischen 1 und 10 gewählt. Gib deine Schätzung ein!",
        color=discord.Color.blue()
    )

    await interaction.response.send_message(embed=embed)

    class ZahlRateModal(discord.ui.Modal, title="Zahl Raten"):
        zahl = discord.ui.TextInput(label='Welche Zahl habe ich gewählt?', style=discord.TextStyle.short,
                                    placeholder='1-10', required=True)

        async def on_submit(self, interaction: discord.Interaction):
            user_zahl = int(self.zahl.value)

            if user_zahl == zahl:
                await interaction.response.send_message(f'Glückwunsch! Du hast die richtige Zahl {zahl} erraten.',
                                                        ephemeral=True)
            else:
                await interaction.response.send_message(
                    f'Schade, die richtige Zahl war {zahl}. Versuche es noch einmal!', ephemeral=True)

    await interaction.response.send_modal(ZahlRateModal())


@bot.tree.command(name='ping', description='Zeigt die Latenz des Bots')
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f'Pong! {round(bot.latency * 1000)}ms', delite_after=10)
    print(f'Ping: {round(bot.latency * 1000)}ms for the user {interaction.user}')


bot.run(TOKEN)
