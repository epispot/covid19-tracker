import discord
from discord.ext import commands
import covid19cases as covid

TOKEN = open("token.txt","r").readline()
client = commands.Bot(command_prefix = '.')

client.remove_command("help")

@client.command(pass_context=True)
async def help(ctx):
    embed = discord.Embed(
        colour = discord.Colour.green())
    embed.set_author(name='Commands')
    embed.add_field(name='.cases', value='Returns general data about global cases', inline=False)
    await ctx.send(embed=embed)

@client.event
async def on_command_error(ctx, error):
    await ctx.send(f'{error}. Error. Use .help to find a complete list of commands.')

@client.command()
async def cases(ctx):
    await ctx.send(covid.get_global_cases())

client.run(TOKEN)