import discord
from discord.ext import commands
import covid19cases as covid19
from covid.api import CovId19Data
from covid import Covid
from case_predictors import predict_uncontrolled
from datetime import datetime
import matplotlib.pyplot as plt
import os

api = CovId19Data(force=False)
covid = Covid()

TOKEN = open("token.txt","r").readline()
prefix = 'info '
client = commands.Bot(command_prefix = prefix)

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='a pandemic | info'))

client.remove_command("help")

@client.command(pass_context=True)
async def help(ctx):
    embed = discord.Embed(
        colour = discord.Colour.blurple())
    embed.set_author(name='Commands')
    embed.add_field(name='cases', value='Returns general data about global cases, or add the name of a country after to get data for it. NOTE: Use `list` to see all country names.')
    embed.add_field(name='credits', value='Returns data source and APIs used in the bot')
    embed.add_field(name='list', value='Returns all the avaliable country names that can be used with `info cases` and `info predict`')
    embed.add_field(name='predict', value='Predicts total _active_ cases for following 7 days, if days are not given. Format: `info predict 7 USA` will predict the active cases in the US for the next 7 days. You can also use `info predict` or `info predict _days_`.')
    embed.add_field(name='compare', value='Returns a graph comparing two countries. Format: `info compare country1 country2`. If there is more that one word in the name of the country, seperate it with a dash. eg. `info compare Saudi-Arabia USA')
    embed.add_field(name='release_notes', value='View the latest updates of the new release.')
    embed.add_field(name='server', value='Get invites to the official COVID-19 Tracker servers.')
    await ctx.send(embed=embed)

@client.event
async def on_command_error(ctx, error):
    
    await ctx.send(f'Whoops... seems that there\'s an error. Use `help` to check if you\'re using the right command. \n Absolutely sure you are? Then submit a issue (with `{error}` as the error message) on GitHub at https://github.com/epispot/covid19-tracker/issues')

@client.command()
async def cases(ctx, region=None, region2=None, region3=None, region4=None):
    if region is None:
        cases = covid19.get_global_cases()
        
        embed = discord.Embed(
            colour = discord.Colour.red()
        )
        embed.set_author(name='Global Statistics')
        embed.add_field(name='Cases', value=cases["TotalCases"])
        embed.add_field(name='New Cases', value=cases["NewCases"])
        embed.add_field(name="Deaths", value=cases["TotalDeaths"])
        embed.add_field(name="New Deaths", value=cases["NewDeaths"])
        embed.add_field(name="Recovered", value=cases["TotalRecovered"])
        embed.add_field(name="New Recovered Patients", value=cases["NewRecovered"])
        embed.add_field(name="Active Cases", value=cases["ActiveCases"])
        embed.add_field(name="Critical", value=cases["Critical"])
        embed.add_field(name="Cases Per Million", value=cases["CasesPerOneMillion"])
        embed.add_field(name="Deaths Per Million", value=cases["DeathsPerOneMillion"])
        embed.add_field(name="Last Updated", value=cases["LastUpdated"])

        await ctx.send(embed=embed)
    
    if region2 is None and region != None:
        
        data = covid.get_status_by_country_name(region)

        embed = discord.Embed(
            colour = discord.Colour.blue()
        )
        embed.set_author(name='covid-19')
        embed.title = region + ' Statistics'
        embed.add_field(name='Cases', value=data['confirmed'], inline=False)
        embed.add_field(name='Recovered', value=data['recovered'], inline=False)
        embed.add_field(name='Deaths', value=data['deaths'], inline=False)
        embed.add_field(name='Active', value=data['active'], inline=False)

        await ctx.send(embed=embed)
    
    if region2 != None and region3 is None:
        data = covid.get_status_by_country_name(region+" "+region2)

        embed = discord.Embed(
            colour = discord.Colour.blue()
        )
        embed.set_author(name='covid-19')
        embed.title = region + ' ' + region2 + ' Statistics'
        embed.add_field(name='Cases', value=data['confirmed'], inline=False)
        embed.add_field(name='Recovered', value=data['recovered'], inline=False)
        embed.add_field(name='Deaths', value=data['deaths'], inline=False)
        embed.add_field(name='Active', value=data['active'], inline=False)

        await ctx.send(embed=embed)

    if region3 != None and region4 is None: 
        data = covid.get_status_by_country_name(region+" "+region2+" "+region3)

        embed = discord.Embed(
            colour = discord.Colour.blue()
        )
        embed.set_author(name='covid-19')
        embed.title = region + " " + region2 + " " + region3 + ' Statistics'
        embed.add_field(name='Cases', value=data['confirmed'], inline=False)
        embed.add_field(name='Recovered', value=data['recovered'], inline=False)
        embed.add_field(name='Deaths', value=data['deaths'], inline=False)
        embed.add_field(name='Active', value=data['active'], inline=False)

    if region4 != None:
        data = covid.get_status_by_country_name(region+" "+region2+" "+region3+" "+region4)

        embed = discord.Embed(
            colour = discord.Colour.blue()
        )
        embed.set_author(name='covid-19')
        embed.title = region + " " + region2 + " " + region3 + " " + region4 +  ' Statistics'
        embed.add_field(name='Cases', value=data['confirmed'], inline=False)
        embed.add_field(name='Recovered', value=data['recovered'], inline=False)
        embed.add_field(name='Deaths', value=data['deaths'], inline=False)
        embed.add_field(name='Active', value=data['active'], inline=False)

        await ctx.send(embed=embed)

        await ctx.send(embed=embed)

@client.command()
async def predict(ctx, days=None, region=None, region2=None, region3=None, region4=None, region5=None):
    if daysisNone:
        cases = covid19.get_global_cases()
        embed = discord.Embed(
            colour = discord.Colour.green()
        )
        embed.set_author(name='Prediction')
        embed.add_field(name='What this represents', value='If all restrictions were let loose for the following 7 days, we\'d have the following amount of active cases:')
        embed.add_field(name='Day 1', value=predict_uncontrolled(int(cases["TotalCases"].replace(',', '')), int(cases["ActiveCases"].replace(',', '')), 7800000000000, 1), inline=False)
        embed.add_field(name='Day 2', value=predict_uncontrolled(int(cases["TotalCases"].replace(',', '')), int(cases["ActiveCases"].replace(',', '')), 7800000000000, 2), inline=False)
        embed.add_field(name='Day 3', value=predict_uncontrolled(int(cases["TotalCases"].replace(',', '')), int(cases["ActiveCases"].replace(',', '')), 7800000000000, 3), inline=False)
        embed.add_field(name='Day 4', value=predict_uncontrolled(int(cases["TotalCases"].replace(',', '')), int(cases["ActiveCases"].replace(',', '')), 7800000000000, 4), inline=False)
        embed.add_field(name='Day 5', value=predict_uncontrolled(int(cases["TotalCases"].replace(',', '')), int(cases["ActiveCases"].replace(',', '')), 7800000000000, 5), inline=False)
        embed.add_field(name='Day 6', value=predict_uncontrolled(int(cases["TotalCases"].replace(',', '')), int(cases["ActiveCases"].replace(',', '')), 7800000000000, 6), inline=False)
        embed.add_field(name='Day 7', value=predict_uncontrolled(int(cases["TotalCases"].replace(',', '')), int(cases["ActiveCases"].replace(',', '')), 7800000000000, 7), inline=False)
        embed.add_field(name='Current Active Cases', value=cases["ActiveCases"], inline=False)
        embed.add_field(name='Current Total Cases', value=cases['TotalCases'])
        embed.set_footer(text='NOTE: The following predictions cannot be relied on and might not actually happen.')
        await ctx.send(embed=embed)
    
    elif regionisNone and days!=None:
        cases = covid19.get_global_cases()
        embed = discord.Embed(
            colour = discord.Colour.green()
        )
        embed.set_author(name='Prediction')
        embed.add_field(name='What this represents', value='If all restrictions were let loose for the following ' + days + ' day(s), we\'d have the following amount of active cases:')
        embed.add_field(name='Day '+ days, value=predict_uncontrolled(int(cases["TotalCases"].replace(',', '')), int(cases["ActiveCases"].replace(',', '')), 7800000000000, int(days)), inline=False)
        embed.set_footer(text='NOTE: The following predictions cannot be relied on and might not actually happen.')
        embed.add_field(name='Current Active Cases', value=cases["ActiveCases"], inline=False)
        embed.add_field(name='Current Total Cases', value=cases['TotalCases'])
        await ctx.send(embed=embed)
    
    elif region2isNone and region != None:
        cases = covid19.get_country_cases(region)
        embed = discord.Embed(
            colour = discord.Colour.green()
        )
        embed.set_author(name='Prediction')
        embed.add_field(name='What this represents', value='If all restrictions were let loose for the following ' + days + ' day(s), we\'d have the following amount of active cases:')
        embed.add_field(name='Day '+ days, value=predict_uncontrolled(int(cases["TotalCases"].replace(',', '')), int(cases["ActiveCases"].replace(',', '')), int(cases["Population"].replace(',', '')), int(days)), inline=False)
        embed.add_field(name='Current Active Cases', value=cases["ActiveCases"], inline=False)
        embed.add_field(name='Current Total Cases', value=cases['TotalCases'])
        embed.set_footer(text='NOTE: The following predictions cannot be relied on and might not actually happen.')
        await ctx.send(embed=embed)
    
    elif region3isNone and region2 != None:
        cases = covid19.get_country_cases(region+" "+region2)
        embed = discord.Embed(
            colour = discord.Colour.green()
        )
        embed.set_author(name='Prediction')
        embed.add_field(name='What this represents', value='If all restrictions were let loose for the following ' + days +  ' day(s), we\'d have the following amount of active cases:')
        embed.add_field(name='Day '+ days, value=predict_uncontrolled(int(cases["TotalCases"].replace(',', '')), int(cases["ActiveCases"].replace(',', '')), int(cases["Population"].replace(',', '')), int(days)), inline=False)
        embed.add_field(name='Current Active Cases', value=cases["ActiveCases"], inline=False)
        embed.add_field(name='Current Total Cases', value=cases['TotalCases'])
        embed.set_footer(text='NOTE: The following predictions cannot be relied on and might not actually happen.')
        await ctx.send(embed=embed)
    
    elif region4isNone and region3 != None:
        cases = covid19.get_country_cases(region+" "+region2+" "+region3)
        embed = discord.Embed(
            colour = discord.Colour.green()
        )
        embed.set_author(name='Prediction')
        embed.add_field(name='What this represents', value='If all restrictions were let loose for the following ' + days + ' day(s), we\'d have the following amount of active cases:')
        embed.add_field(name='Day '+ days, value=predict_uncontrolled(int(cases["TotalCases"].replace(',', '')), int(cases["ActiveCases"].replace(',', '')), int(cases["Population"].replace(',', '')), int(days)), inline=False)
        embed.add_field(name='Current Active Cases', value=cases["ActiveCases"], inline=False)
        embed.add_field(name='Current Total Cases', value=cases['TotalCases'])
        embed.set_footer(text='NOTE: The following predictions cannot be relied on and might not actually happen.')
        await ctx.send(embed=embed)
    
    elif region5isNone and region4 != None:
        cases = covid19.get_country_cases(region+" "+region2+" "+region3+" "+region4)
        embed = discord.Embed(
            colour = discord.Colour.green()
        )
        embed.set_author(name='Prediction')
        embed.add_field(name='What this represents', value='If all restrictions were let loose for the following ' + days + ' day(s), we\'d have the following amount of active cases:')
        embed.add_field(name='Day '+ days, value=predict_uncontrolled(int(cases["TotalCases"].replace(',', '')), int(cases["ActiveCases"].replace(',', '')), int(cases["Population"].replace(',', '')), int(days)), inline=False)
        embed.add_field(name='Current Active Cases', value=cases["ActiveCases"], inline=False)
        embed.add_field(name='Current Total Cases', value=cases['TotalCases'])
        embed.set_footer(text='NOTE: The following predictions cannot be relied on and might not actually happen.')
        await ctx.send(embed=embed)
    
    elif region5!=None:
        cases = covid19.get_country_cases(region+" "+region2+" "+region3+" "+region4+" "+region5)
        embed = discord.Embed(
            colour = discord.Colour.green()
        )
        embed.set_author(name='Prediction')
        embed.add_field(name='What this represents', value='If all restrictions were let loose for the following ' + days + ' day(s), we\'d have the following amount of active cases:')
        embed.add_field(name='Day '+ days, value=predict_uncontrolled(int(cases["TotalCases"].replace(',', '')), int(cases["ActiveCases"].replace(',', '')), int(cases["Population"].replace(',', '')), int(days)), inline=False)
        embed.add_field(name='Current Active Cases', value=cases["ActiveCases"], inline=False)
        embed.add_field(name='Current Total Cases', value=cases['TotalCases'])
        embed.set_footer(text='NOTE: The following predictions cannot be relied on and might not actually happen.')
        await ctx.send(embed=embed)

@client.command()
async def credits(ctx):
    api = 'https://pypi.org/project/COVID-19-Cases/ - Covid-19-Cases was used to take data from the source and output stats. \n'
    api2 = 'https://pypi.org/project/covid-data-api/ - The _COVID Data API_ was used to take data from John Hopkins and output stats. \n'
    api3 = 'https://epispot.github.io - The epispot python package was used in the predicion mechanism. \n'
    source = 'https://www.worldometers.info/coronavirus/ - Info from here \n'

    await ctx.send(api + source + api2 + api3)

@client.command()
async def list(ctx):
    listc = covid.list_countries()
    await ctx.send('There are many different countries and regions to use (including the Diamond Princess cruise ship):')
    for i in listc:
        await ctx.send(i['name'])
    await ctx.send('Those are all of the country and regions that you can use. NOTE: If predicting, use `USA` instead of `US` as the country name.')

@client.command()
async def compare(ctx, c1, c2):
    data = [int(covid19.get_country_cases(c1.replace('-', ' '))["TotalCases"].replace(',', '')), int(covid19.get_country_cases(c2.replace('-', ' '))["TotalCases"].replace(',', ''))]
    
    fig = plt.subplots()
    plt.bar([c1.replace('-', ' '), c2.replace('-', ' ')], data)
    plt.suptitle(c1.replace('-', ' ') + " compared to " + c2.replace('-', ' '))
    plt.savefig('graph.png',dpi=400)

    await ctx.send(file=discord.File('graph.png'))

    
    os.remove("graph.png")
    plt.clf()

@client.command()
async def release_notes(ctx):
    embed = discord.Embed(
            colour = discord.Colour.red()
        )
    embed.set_author(name='Release Notes')
    embed.title = 'v1.1.0'
    embed.add_field(name='Bug Fixes', value='- Can use more than one word country names, while before it would return an error.')
    embed.add_field(name='New Features', value='- Prediction of the world and countries for uncontrolled spread. \n - Country list, to view whether to use "USA" or "US" for example'+
        '\n - A status! \n - More statistics! \n - Compare Countries with `info compare...`')
    embed.set_footer(text='You can view the release notes for all of the releases at https://github.com/epispot/covid19-tracker/releases')
    await ctx.send(embed=embed)

@client.command()
async def server(ctx):
    embed = discord.Embed(
        color = discord.Colour.dark_gold()
    )
    embed.set_author(name='Servers')
    embed.add_field(name='Support Server', value='https://top.gg/bot/784949651303301150/invite')

    await ctx.send(embed=embed)

client.run(TOKEN)
