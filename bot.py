import discord
from os import getenv
from discord.ext import commands
from db_manager import setup_server,get_group,add_user,get_group_from_server,remove_user
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/',intents=intents)

@bot.command(name='setup')
async def setup(ctx):
    id = ctx.guild.id
    name = ctx.guild.name
    res = setup_server(str(id),name)
    if res['success']:
        await ctx.send('Server setup')
    else:
        await ctx.send(res['error'])
    
@bot.command(name='members')
async def get_members(ctx):
    id = ctx.guild.id
    res = get_group_from_server(str(id))
    if not res['success']:
        await ctx.send(res['error'])
    else:
        res = get_group(res['group_id'])
        if not res['success']:
            await ctx.send(res['error'])
        elif len(res['users']) == 0:
            await ctx.send('No members in group')
        else:
            users = map(lambda x: x['username'],res['users'])
            await ctx.send('\n'.join(users))

@bot.command(name='add')
async def add(ctx,user:str):
    if user == '':
        await ctx.send('Please provide a username')
    id = ctx.guild.id
    res = get_group_from_server(str(id))
    if not res['success']:
        await ctx.send(res['error'])
    else:
        res = add_user(res['group_id'],user)
        if res['success']:
            await ctx.send('User added')
        else:
            await ctx.send(res['error'])

@bot.command(name='remove')
async def remove(ctx,user:str):
    if user == '':
        await ctx.send('Please provide a username')
    id = ctx.guild.id
    res = get_group_from_server(str(id))
    if not res['success']:
        await ctx.send(res['error'])
    else:
        res = remove_user(res['group_id'],user)
        if res['success']:
            await ctx.send('User removed')
        else:
            await ctx.send(res['error'])

@bot.command(name='ranking')
async def ranking(ctx):
    id = ctx.guild.id
    res = get_group_from_server(str(id))
    if not res['success']:
        await ctx.send(res['error'])
    else:
        res = get_group(res['group_id'])
        if not res['success']:
            await ctx.send(res['error'])
        elif len(res['users']) == 0:
            await ctx.send('No members in group')
        else:
            users = res['users']
            sorted_users = [f'{idx + 1}. {x["username"]} : {x["points"]} points' for idx,x in enumerate(sorted(users,key=lambda x: int(x['points']),reverse=True))]
            await ctx.send('\n'.join(sorted_users))

def run_bot():
    token = getenv('DISCORD_TOKEN')
    bot.run(token)
