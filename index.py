import discord
from discord.ext import commands
import covid19cases as covid

TOKEN = open("token.txt","r").readline()
prefix = 'info '
client = commands.Bot(command_prefix = prefix)

client.remove_command("help")

@client.command(pass_context=True)
async def help(ctx):
    embed = discord.Embed(
        colour = discord.Colour.blue())
    embed.set_author(name='Commands')
    embed.add_field(name='cases', value='Returns general data about global cases, or add the name of a country or continent after to get data for it. NOTE: Not all countries will have data, so it might output an error.', inline=False)
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
        if region == "Asia" or region == "Europe" or region == "North America" or region == "South America" or region == "Africa" or region == "Australia":
            cases = covid.get_continent_cases(region)
            
            embed = discord.Embed(
                colour = discord.Colour.red()
            )
            embed.set_author(name=region + ' Statistics')
            embed.add_field(name='Cases', value=cases["TotalCases"], inline=False)
            embed.add_field(name="Deaths", value=cases["TotalDeaths"], inline=False)
            embed.add_field(name="Recovered", value=cases["TotalRecovered"], inline=False)
            embed.add_field(name="Active Cases", value=cases["ActiveCases"], inline=False)
            embed.add_field(name="Critical", value=cases["Critical"], inline=False)
            embed.add_field(name="Last Updated", value=cases["LastUpdated"], inline=False)

            await ctx.send(embed=embed)
        else:    
            cases = covid.get_country_cases(region)
            
            embed = discord.Embed(
                colour = discord.Colour.red()
            )
            embed.set_author(name=region + ' Statistics')
            embed.add_field(name='Cases', value=cases["TotalCases"], inline=False)
            embed.add_field(name="Deaths", value=cases["TotalDeaths"], inline=False)
            embed.add_field(name="Recovered", value=cases["TotalRecovered"], inline=False)
            embed.add_field(name="Active Cases", value=cases["ActiveCases"], inline=False)
            embed.add_field(name="Critical", value=cases["Critical"], inline=False)
            embed.add_field(name="Cases Per Million", value=cases["CasesPerOneMillion"], inline=False)
            embed.add_field(name="Deaths Per Million", value=cases["DeathsPerOneMillion"], inline=False)
            embed.add_field(name="Last Updated", value=cases["LastUpdated"], inline=False)

            await ctx.send(embed=embed)

@client.command()
async def credits(ctx):
    api = 'https://pypi.org/project/COVID-19-Cases/ - COVID-19-Cases was used to take data from the source and output \n'
    source = 'https://www.worldometers.info/coronavirus/ - Info from here'

    await ctx.send(api + source)

client.run(TOKEN)