import argparse
import csv
from itertools import chain
from os import getenv

from discord import PermissionOverwrite, Permissions
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


def create_read_only_overwrite():
    allow_permissions = Permissions(
        read_messages=True, read_message_history=True
    )
    deny_permissions = Permissions.all()
    deny_permissions.read_messages = False
    deny_permissions.read_message_history = False
    overwrite = PermissionOverwrite.from_pair(
        allow_permissions, deny_permissions
    )
    return overwrite


async def set_categories_read_only(guild, role_name):
    # カテゴリの@everyoneの権限の対応で済むことが分かり、実装中のこの関数は使わなくなった
    # TODO: @everyoneの権限の編集の自動化の余地あり（BotのOAuthがいるかも）
    role = [role for role in guild.roles if role.name == role_name][0]
    read_only = create_read_only_overwrite()
    for category_channel in guild.categories[:2]:
        await category_channel.set_permissions(role, overwrite=read_only)


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
        if args.archive_command == "set_read_only":
            await set_categories_read_only(guild, args.role_name)

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
set_read_only_parser = archive_subparsers.add_parser("set_read_only")
set_read_only_parser.add_argument("role_name")

args = parser.parse_args()

token = getenv("DISCORD_BOT_TOKEN")
bot.run(token)
