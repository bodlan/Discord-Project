import asyncio
import re
import discord
import requests
import random
from datetime import datetime
from libraries import CONFIG
from libraries.database import create_member
from libraries.database import update_member
from libraries.database import get_member
from libraries.database import get_all_members
from discord.ext import commands


intents = discord.Intents.all()
command_prefix = "!"
bot = commands.Bot(command_prefix=command_prefix, intents=intents)
bet_data = {}
bot_start = True
Vlad_greeting = True


def get_quote():
    json_data = requests.get("http://zenquotes.io/api/random").json()
    quote_data = json_data[0]["q"] + " -" + json_data[0]["a"]
    return quote_data


async def send_message(ctx, args):
    await ctx.message.channel.send(args)


@bot.event
async def on_presence_update(before, after):
    # guild = bot.get_guild(CONFIG.BodlanServerID)
    # channel = guild.get_channel(CONFIG.TestChannelID)
    global bot_start, Vlad_greeting
    if bot_start:
        for user in after.guild.members:
            if user.status != discord.Status.offline and not user.bot:
                update_member(user.id, str(user.status), bot_start)
                print(user.name + "#" + user.discriminator, "Updated time with start of the bot!")
        bot_start = False
    for user in after.guild.members:
        if user.status != discord.Status.offline and not user.bot:
            update_member(user.id, str(user.status))


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    # res = bot.get_guild(CONFIG.BodlanServerID).fetch_members()


@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if message.author == bot.user:
        return
    if message.content.startswith(f"{command_prefix}hello"):
        await message.channel.send(f"{CONFIG.Emoji.TrollDespair} Hi")
    if message.content.startswith(f"{command_prefix}quote"):
        quote = get_quote()
        await message.channel.send(quote)
    if re.findall("(\W|^)[f|F](\W|$)", message.content):
        await message.channel.send("o7")


@bot.command()
async def start(ctx):
    for user in ctx.guild.members:
        if not user.bot:
            create_member(user.id, user.name, user.discriminator, 100, str(user.status))
            print(user.name + "#" + user.discriminator, "Created!")


@bot.command(aliases=["gamba", "g"])
async def gamble(ctx, gamble_points: int = 10):
    """
    Gambling your points that you earn each 10 seconds
    """
    user_id = ctx.message.author.id
    user_status = ctx.message.author.status
    if get_member(user_id).points < gamble_points:
        await send_message(
            ctx,
            ctx.message.author.mention
            + " you have not enough points to gamble!\n"
            + "Your points: "
            + str(get_member(user_id).points),
        )
        return
    random_value = random.random()
    if random_value >= 0.5:
        update_member(user_id, str(user_status), gamble_points=gamble_points)
        await send_message(ctx, ctx.message.author.mention + " has won " + str(gamble_points) + " points")
    else:
        update_member(user_id, str(user_status), gamble_points=-gamble_points)
        await send_message(ctx, ctx.message.author.mention + " has lost " + str(gamble_points) + " points")


@bot.command(aliases=["FB", "fb", "Fbet"])
async def finish_bet(ctx):
    """
    Finishes current bet
    args: option number from options in bet
    Example: !FB 2  - to conclude the winner of the bet 2nd option
    """
    message = ctx.message
    channel = message.channel
    user_id = message.author.id
    user_status = message.author.status
    print("Bet data:", bet_data)
    if bet_data:
        res = re.findall("\d", message.content)[0]
        for key, value in bet_data.items():
            if key.startswith("bet_option"):
                if res in key:
                    for winner in value:
                        update_member(user_id, str(user_status), gamble_points=winner["bet"])
                else:
                    for loser in value:
                        if loser:
                            update_member(user_id, str(user_status), gamble_points=-loser["bet"])
        bet_data.clear()
        await channel.send("Bet finished!")
    else:
        await channel.send("No active bet!")


@bot.command(aliases=["NB", "nb"])
async def new_bet(ctx, *args):
    """args:
    title: name of the bet
    options: options of bet, max 5!
    """
    message = ctx.message
    channel = message.channel
    print("Args:", args)
    args = [arg.lower() for arg in args]
    if "title" and "options" in args:
        try:
            title_index = args.index("title")
            options_index = args.index("options")
            title = args[title_index + 1 : options_index]
            options = args[options_index + 1 :]
            bet_data["title"] = title
            # await channel.send("Creating new bet with\nTitle: "+" ".join(title)+"\nOptions: " +
            # " ".join(options))
            option_message = "New bet started, options to choose:\n"
            for index in range(1, len(options) + 1):
                option_message += f"{index}: {options[index - 1]}\n"
                bet_data[f"bet_option_{index}"] = []
            await channel.send(option_message)
            # [await res.add_reaction(emoji) for emoji in CONFIG.Emoji.bet_list[:len(options)]]
        except Exception as e:
            await channel.send("Exception during processing bet!")
            print("Exception:", e)

        def check(ctx):
            check_message = ctx.content
            user_id = ctx.author.id
            if check_message.startswith(f"{command_prefix}bet"):
                try:
                    res = check_message.partition("!bet")[2].partition("option")
                    print("res:", res)
                    bet_sum = int(res[0])
                    bet_option = int(res[2])
                    bet_id = user_id
                    if bet_sum < get_member(user_id).points:
                        bet_data[f"bet_option_{bet_option}"].append(
                            {"id": bet_id, "bet": bet_sum, "timestamp": datetime.now()}
                        )
                    else:
                        raise discord.ClientException
                    return ctx
                except ValueError:
                    raise ValueError
            return None

        while True:
            try:
                check_message = await bot.wait_for("message", timeout=30.0, check=check)
                await check_message.add_reaction(CONFIG.Emoji.ThumbUp)
            except discord.ClientException:
                await channel.send(message.author.mention + "\nNot enough points to make a bet!")
                continue
            except ValueError:
                await channel.send(message.author.mention + "\nSomething happened while executing request! Check input")
                continue
            except asyncio.TimeoutError:
                await channel.send("Bet closed!")
                break

    else:
        await channel.send("No title or options in request")


@bot.command(aliases=["cls"])
async def delete_chat(ctx, amount: int = 5):
    channel = ctx.message.channel
    max_num = 100
    if amount > max_num:
        for i in range(int(amount / max_num)):
            await channel.purge(limit=max_num)


@bot.command(aliases=["P", "p"])
async def points(ctx, args=None):
    """
    While you are online in discord you earn points
    10 seconds = 1 point
    Example: !P all to see all user points
    !p to see your current points
    """
    user_id = ctx.message.author.id
    if args == "all":
        all_data: str = ""
        for member in get_all_members():
            all_data += member.name + "#" + str(member.desc) + " has " + str(member.points) + " points\n"
        await send_message(ctx, all_data)
    else:
        await ctx.message.channel.send(ctx.message.author.mention + "\nYour points: " + str(get_member(user_id).points))
