import discord
from discord.ext import commands
import covid19cases as covid
from covid.api import CovId19Data

api = CovId19Data(force=False)

TOKEN = open("token.txt","r").readline()
prefix = 'info '
client = commands.Bot(command_prefix = prefix)

client.remove_command("help")

@client.command(pass_context=True)
async def help(ctx):
    embed = discord.Embed(
        colour = discord.Colour.blue())
    embed.set_author(name='Commands')
    embed.add_field(name='cases', value='Returns general data about global cases, or add the name of a country after to get data for it. NOTE: Not all countries will have data, so it might output an error.', inline=False)
    embed.add_field(name='credits', value='Returns data source and APIs used in the bot')
    await ctx.send(embed=embed)

@client.event
async def on_command_error(ctx, error):
    await ctx.send(f'Error. {error} Use `help` to find a complete list of commands.')

@client.command()
async def cases(ctx, region=None):
    if region == None:
        cases = covid.get_global_cases()
        
        embed = discord.Embed(
            colour = discord.Colour.red()
        )
        embed.set_author(name='Global Statistics')
        embed.add_field(name='Cases', value=cases["TotalCases"], inline=False)
        embed.add_field(name='New Cases', value=cases["NewCases"], inline=False)
        embed.add_field(name="Deaths", value=cases["TotalDeaths"], inline=False)
        embed.add_field(name="New Deaths", value=cases["NewDeaths"], inline=False)
        embed.add_field(name="Recovered", value=cases["TotalRecovered"], inline=False)
        embed.add_field(name="New Recovered Patients", value=cases["NewRecovered"], inline=False)
        embed.add_field(name="Active Cases", value=cases["ActiveCases"], inline=False)
        embed.add_field(name="Critical", value=cases["Critical"], inline=False)
        embed.add_field(name="Cases Per Million", value=cases["CasesPerOneMillion"], inline=False)
        embed.add_field(name="Deaths Per Million", value=cases["DeathsPerOneMillion"], inline=False)
        embed.add_field(name="Last Updated", value=cases["LastUpdated"], inline=False)

        await ctx.send(embed=embed)
    else:
        data = api.filter_by_country("ireland")

        embed = discord.Embed(
            colour = discord.Colour.blue()
        )
        embed.set_author(name='COVID-19')
        embed.title = region + ' Statistics'
        embed.add_field(name='Cases', value=data['confirmed'], inline=False)
        embed.add_field(name='Recovered', value=data['recovered'], inline=False)
        embed.add_field(name='Deaths', value=data['deaths'], inline=False)
        embed.add_field(name='Last Updated', value=data['last_updated'], inline=False)

        await ctx.send(embed=embed)

@client.command()
async def credits(ctx):
    api = 'https://pypi.org/project/COVID-19-Cases/ - COVID-19-Cases was used to take data from the source and output stats. \n'
    api2 = 'https://pypi.org/project/covid-data-api/ - The _COVID Data API_ was used to take data from John Hopkins and output stats.'
    source = 'https://www.worldometers.info/coronavirus/ - Info from here \n'

    await ctx.send(api + source + api2)

client.run(TOKEN)