import discord

from database.db import register_user, get_ra_username
from utils.api import get_recent_achievements
from utils.date import convert_utc_to_brt

async def register_ra_user(message, ra_username):
    register_user(str(message.author.id), ra_username)
    await message.channel.send(f"{message.author.mention}, seu usuário `{ra_username}` foi registrado com sucesso!")

async def fetch_user_achievements(message):
    ra_username = get_ra_username(str(message.author.id))
    if ra_username:
        achievements = get_recent_achievements(ra_username)
        if achievements:
            for ach in achievements:
                
                hardcore_status = "Hardcore" if ach['HardcoreMode'] == 1 else "Softcore"
                game_icon_url = f"https://retroachievements.org{ach['GameIcon']}"
                achievement_icon_url = f"https://retroachievements.org{ach['BadgeURL']}"
                
                embed = discord.Embed(
                    title = f"🏆 {ach['Title']}",
                    url = f"https://retroachievements.org/achievement/{ach['AchievementID']}",
                    description = f"*{ach['Description']}*",
                    color = discord.Color.gold() if hardcore_status == "Hardcore" else discord.Color.dark_gray()
                )
                
                embed.set_image(url = game_icon_url)
                embed.set_thumbnail(url = achievement_icon_url)
                embed.add_field(name = "Points", value = f"{ach['Points']} ({ach['TrueRatio']})", inline = False)
                embed.add_field(name = "Unloked in", value = convert_utc_to_brt(ach['Date']), inline = False)
                embed.add_field(name = "Game", value = ach['GameTitle'], inline = True)
                
                await message.channel.send(embed=embed)
        else:
            await message.channel.send(f"Não consegui buscar as conquistas de `{ra_username}`.")
    else:
        await message.channel.send("Você ainda não registrou seu usuário. Use o comando `!registrar <seu_usuario>` para registrar.")
