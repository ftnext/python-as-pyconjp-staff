import csv
from os import getenv

from discord.ext import commands

bot = commands.Bot(command_prefix="/")


def fetch_talk_channels_information(guild):
    categories_for_talk = [
        category
        for category in guild.categories
        if category.name.startswith("day")
    ]
    headers = ("category_id", "category_name", "channel_id", "channel_name")
    data = [
        (category.id, category.name, channel.id, channel.name)
        for category in categories_for_talk
        for channel in category.text_channels
    ]

    with open("talk_channels.csv", "w", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows([headers] + data)


@bot.event
async def on_ready():
    print("ready!")

    guild = bot.get_guild(int(getenv("GUILD_ID")))

    breakpoint()


token = getenv("DISCORD_BOT_TOKEN")
bot.run(token)
