import argparse
import csv
from os import getenv

from discord.ext import commands

bot = commands.Bot(command_prefix="/")


def fetch_talk_channels_information(guild, csv_to_save):
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

    with open(csv_to_save, "w", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows([headers] + data)


@bot.event
async def on_ready():
    print("ready!")

    guild = bot.get_guild(int(getenv("GUILD_ID")))

    if args.subcommand == "fetch_talk_channels":
        fetch_talk_channels_information(guild, args.csv_to_save)

    breakpoint()


parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest="subcommand")

fetch_talk_channels_parser = subparsers.add_parser("fetch_talk_channels")
fetch_talk_channels_parser.add_argument("csv_to_save")

args = parser.parse_args()

token = getenv("DISCORD_BOT_TOKEN")
bot.run(token)
