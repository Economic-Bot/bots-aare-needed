import keep_alive  # to keep the bot alive
import discord
from discord.ext import commands
import os
import json


def get_prefix(client, message):
    with open("perfix_data.json", "r") as f:
        prefixes = json.load(f)
    return prefixes.get(str(message.guild.id), "?")

bot = commands.Bot(command_prefix=get_prefix)

# go the chats, in repl
bot.remove_command('help')

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching, name=f'{len(bot.guilds)} Servers'))
        
  
@bot.event
async def on_command_error(ctx, error):
    channel = bot.get_channel(810542077448159292)
    await channel.send(str(error)) 


@bot.command(aliases=["reload"])
async def re_load_ext(ctx, *name_of_ext):
    """To reload extension(s)"""

    if str(ctx.author.id) in ("740633806569996358", "759129467414380554"):
        try:
            for i in name_of_ext:
                bot.reload_extension(i)

        except Exception as err:
            await ctx.send(err)

        else:
            await ctx.send(f"{name_of_ext} was successfully reloaded")

    else:
        await ctx.send(
            f"You don't have perms <@{ctx.author.id}>, _ stupid just why are you a dick or somthing just why?_"
        )


# when bot is added to other server
@bot.event
async def on_guild_join(guild):
    with open("perfix_data.json", "r") as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = "?"

    # storing the data
    with open("perfix_data.json", "w") as f:
        json.dump(prefixes, f, indent=4)


# when bot removed from server
@bot.event
async def on_guild_remove(guild):
    with open("perfix_data.json", "r") as f:
        prefixes = json.load(f)

    prefixes.pop(str(guild.id))

    # storing the data
    with open("perfix_data.json", "w") as f:
        json.dump(prefixes, f, indent=4)


@bot.command()
@commands.has_permissions(administrator=True)
async def change_prefix(ctx, prefix):
    """To allow the prefix to be changed"""

    with open("perfix_data.json", "r") as f:
        prefixes = json.load(f)

    prefixes[str(ctx.guild.id)] = prefix
    # storing the data
    with open("perfix_data.json", "w") as f:
        json.dump(prefixes, f, indent=4)

    await ctx.send(f"Prefix has been changed to **{prefix}**")


cogs = [f"cogs.{i[:-3]}" for i in os.listdir(".//cogs") if i[-3:] == ".py"]

for i in cogs:
    if not i in ("cogs.lockdown", "cogs.prefix"):
        try:
            print(i)
            bot.load_extension(i)
        except Exception as f:
            print(f)
            
bot.load_extension("jishaku")
bot.run(os.environ.get("bot_token"))
