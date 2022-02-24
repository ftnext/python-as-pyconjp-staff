import argparse
import csv
from itertools import chain
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


async def edit_topic(guild, channel_id: int, topic: str):
    channel = guild.get_channel(channel_id)
    await channel.edit(topic=topic)


async def edit_channels_topic(guild, csv_path):
    with open(csv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            message = f"Zoom: {row['zoom']}"
            await edit_topic(guild, int(row["channel_id"]), message)


async def sync_channel_permissions_with_category(guild):
    for category_channel in guild.categories:
        for channel in chain(
            category_channel.text_channels, category_channel.voice_channels
        ):
            # カテゴリに属すチャンネルで、権限がカテゴリと同期していなければ同期する
            if channel.category and not channel.permissions_synced:
                print(channel.category.name, channel.name)
                # TODO: 必須ではないが、Missing Access (discord.errors.Forbidden) 対応
                await channel.edit(sync_permissions=True)


@bot.event
async def on_ready():
    print("ready!")

    guild = bot.get_guild(int(getenv("GUILD_ID")))

    if args.subcommand == "fetch_talk_channels":
        fetch_talk_channels_information(guild, args.csv_to_save)

    if args.subcommand == "edit_channels_topic":
        await edit_channels_topic(guild, args.input_csv)

    if args.subcommand == "archive":
        if args.archive_command == "sync_channel_permissions":
            await sync_channel_permissions_with_category(guild)

    print("Command completed!")


parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest="subcommand")

fetch_talk_channels_parser = subparsers.add_parser("fetch_talk_channels")
fetch_talk_channels_parser.add_argument("csv_to_save")

edit_channels_topic_parser = subparsers.add_parser("edit_channels_topic")
edit_channels_topic_parser.add_argument("input_csv")

archive_parser = subparsers.add_parser("archive")
archive_subparsers = archive_parser.add_subparsers(dest="archive_command")
sync_channel_permissions_parser = archive_subparsers.add_parser(
    "sync_channel_permissions"
)

args = parser.parse_args()

token = getenv("DISCORD_BOT_TOKEN")
bot.run(token)
