# !csv {channelID}で指定したチャンネルで送信されたメッセージを文字列のみcsvに保存します
import discord
from discord.ext import commands
import csv
import os

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

CSV_FILENAME = "out.csv"

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command()
async def csv(ctx, channel_id: int):
    channel = bot.get_channel(channel_id)
    if channel is None:
        await ctx.send("チャンネルが見つかりませんでした。")
        return

    messages = []
    async for message in channel.history(limit=None, oldest_first=True):
        content = message.content.strip().replace('\n', ' ')
        if content:  # 空メッセージは無視
            messages.append([content])

    if not messages:
        await ctx.send("有効なメッセージが見つかりませんでした。")
        return

    with open(CSV_FILENAME, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(messages)

    await ctx.send(f"{len(messages)} 件のメッセージを `{CSV_FILENAME}` に追記しました。")

bot.run('TOKENHERE')
