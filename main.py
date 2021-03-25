import os
import discord
from discord.ext import commands
from fpl import get_fixture, SHORT_TEAMS, get_team_fixture, get_live_stats, get_team_details, fpl_team_info
from scorecard import get_score
from standings import get_table
from cricket import get_cricket_score

client = commands.Bot(command_prefix="!")


@client.event
async def on_ready():
    print(f"Bot ready")


@client.command()
async def hello(ctx):
    text = None
    with open('README.md', 'r') as op:
        text = op.read()
    await ctx.send(text.replace('# ', '***'))


@client.command()
async def fplLive(ctx):
    try:
        await ctx.send(f"```{get_live_stats()}```")
    except:
        await ctx.send("No live match in progress")


@client.command()
async def cricScore(ctx, *, arg):
    try:
        await ctx.send(get_cricket_score(arg))
    except:
        await ctx.send("try passing something else as parameter")


@client.command()
async def fplTeamInfo(ctx, id: int):
    # try:
    mi, gw, cl, h2h = fpl_team_info(id)
    await ctx.send(f"```{mi}```")
    await ctx.send(f"```{gw[:1961]}```")
    await ctx.send(f"```{gw[1961:]}```")
    await ctx.send(f"```{cl}```")
    await ctx.send(f"```{h2h}```")

    # except:
    #     await ctx.send("Re-check Team id")


@client.command()
async def fplTeamDetail(ctx, id: int):
    try:
        await ctx.send(get_team_details(id))
    except:
        await ctx.send("Re-check Team id")


@client.command()
async def gwFixture(ctx, gw: int = None):
    if gw:
        await ctx.send(f"```{get_fixture(gw)}```")
    else:
        await ctx.send(f"```{get_fixture()}```")


@client.command()
async def teamFixture(ctx, team: str, gw: int = 5):
    await ctx.send("\n".join(get_team_fixture(team, gw)))


@client.command()
async def getTeams(ctx):
    teams = "\n".join(SHORT_TEAMS.values())

    await ctx.send(teams)


@client.command()
async def getTable(ctx, *, arg):
    try:
        await ctx.send(f"```{get_table(arg)}```")
    except:
        await ctx.send(""" 
        Valid league names :
  - epl : English Premier League (England)
  - bundesliga : Bundesliga (Germany)
  - la-liga : La Liga (Spain)
  - serie a : Serie A (Italy)
  - efl : EFL Championship (England Tier 2)
  - isl : Indian Super League (India)
         """)


@client.command()
async def liveScore(ctx, *, arg):
    try:
        await ctx.send(get_score(arg))
    except:
        await ctx.send(f"No match in progress for {arg}.\nTry adding Football club if you are sure there is an ongoing match.")

client.run(os.environ.get('DISCORD_TOKEN'))
