import requests
from bs4 import BeautifulSoup
import discord
from discord.ext import commands, tasks 

def get_tiktok_follower_count():
    url = "REDACTED"
    data = requests.get(url)
    soup = BeautifulSoup(data.content, 'html.parser')
    follower_count_tag = soup.find('strong', {'title': 'Followers', 'data-e2e': 'followers-count'})
    follower_count = follower_count_tag.text
    return follower_count

def get_yt_follower_count():
    API_KEY = ' REDACTED'
    CHANNEL_ID = 'REDACTED'

    url = f'https://www.googleapis.com/youtube/v3/channels?part=statistics&id={CHANNEL_ID}&key={API_KEY}'

    response = requests.get(url)
    data = response.json()

    subscriber_count = data['items'][0]['statistics']['subscriberCount']
    return subscriber_count


def get_ig_follower_count():
    URL = "REDACTED"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    meta_tag = soup.find("meta", attrs={"property": "og:description"})
    content = meta_tag.get("content")
    followers_count = content.split(",")[0]
    return followers_count

intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
intents.message_content = True 

prefix = "$"
bot = commands.Bot(command_prefix=prefix, intents=intents)
cID = None

bot.remove_command('help')


allowed_user_id = REDACTED

@bot.event  
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f"Command not found. Use `{prefix}help` to see available commands.")


        
@bot.command()
async def setup(ctx):
    if ctx.author.id == REDACTED:

        guild = ctx.guild 

        category = await guild.create_category("Para Stats Counter")
        ig_follower_count = get_ig_follower_count()
        yt_follower_count = get_yt_follower_count()
        tt_follower_count = get_tiktok_follower_count()
        member_counter = ctx.guild.member_count

        ig_voice_channel = await category.create_voice_channel(f"Instagram : {ig_follower_count}")
        twitter = await category.create_voice_channel(f"Twitter : SOON")
        yt_voice_channel = await category.create_voice_channel(f"Youtube : {yt_follower_count} ")
        tt_voice_channel = await category.create_voice_channel(f"Tiktok : {tt_follower_count}")
        member_count = await category.create_voice_channel(f"Server Members: {member_counter}")

        await category.set_permissions(guild.default_role, view_channel=True, connect=False)
        await ig_voice_channel.set_permissions(guild.default_role, view_channel=True, connect=False)
        await yt_voice_channel.set_permissions(guild.default_role, view_channel=True, connect=False)
        await tt_voice_channel.set_premissions(guild.default_role, view_channel=True, connect=False)
        await twitter.set_premissions(guild.default_role, view_channel=True, connect=False)
        await member_count.set_premissions(guild.default_role, view_channel=True, connect=False)

        await ctx.send(f'Category "{category.name}" and voice channels "{ig_voice_channel.name}" & "{yt_voice_channel.name}" & "{member_count.name}" & "{tt_voice_channel.name}" with the IDs "{ig_voice_channel.id}" & "{yt_voice_channel.id}" & "{member_count.id}" & "{tt_voice_channel.id}" created.')
    else:
        await ctx.send("You are not authorized to run this command.")





@bot.command()
async def help(ctx):
    await ctx.send(f"Prefix {prefix} \n Command List: \n {prefix}setup - Creates Category & Voice Channel \n {prefix}help - Runs This Command \n {prefix}run <yt_channel_id> <ig_channel_id> <tk_channel_id> <guild_id> <update_channel_id> - Starts The Updating Task ")

 

@bot.command()
async def run(ctx, yt_channel_id: int,ig_channel_id: int, tk_channel_id:int, member_count_id: int ,guild_id: int, update_channel:int):
    if ctx.author.id == REDACTED:    
        update_followers.start(yt_channel_id,ig_channel_id,tk_channel_id,member_count_id,guild_id,update_channel)
        await ctx.send("Starting.")
    else:
        await ctx.send("You are not authorized to run this command.")


@bot.command()
async def stop(ctx):
    if ctx.author.id == REDACTED:
        update_followers.stop()
        await ctx.send("Bot stopped.")
    else:
        await ctx.send("You are not authorized to run this command.")


@tasks.loop(minutes=30)  
async def update_followers(yt_channel_id, ig_channel_id, tk_channel_id, member_count_id, guild_id, update_channel):
    ig_channel = bot.get_channel(ig_channel_id) 
    yt_channel = bot.get_channel(yt_channel_id)
    tk_channel = bot.get_channel(tk_channel_id)
    member_channel = bot.get_channel(member_count_id)

    ig_follower_count = get_ig_follower_count()
    yt_follower_count = get_yt_follower_count()
    tk_follower_count = get_tiktok_follower_count() 

    guild = bot.get_guild(guild_id)  
    if guild:
        get_member_count = guild.member_count  

        u_channel = bot.get_channel(update_channel)

        if ig_channel and yt_channel and u_channel:
            await ig_channel.edit(name=f"Instagram : {ig_follower_count}")
            await yt_channel.edit(name=f"Youtube : {yt_follower_count}")
            await tk_channel.edit(name=f"Tiktok : {tk_follower_count}")
            await member_channel.edit(name=f"Server Members : {get_member_count}")
            await u_channel.send(f'Follower counters updated\nCurrent followers:\n Instagram : {str(ig_follower_count)} \n Youtube : {str(yt_follower_count)} \n Tiktok : {str(tk_follower_count)} \n Server Count : {str(get_member_count)}')
            print("Update Done")
        else:   
            print("Channels or update channel not found")
    else:
        print("Guild not found")

bot.run('REDACTED')



# to-do list:
# add a member count tracker DONE 
# figure out twitter scraping  Not free
# tiktok scraping  DONE 
# youtube scraping  DONE
# Instagram Scraping DONE
