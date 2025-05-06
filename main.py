import nextcord
from nextcord.ext import commands
from nextcord import Interaction, Activity, ActivityType, Status
import os
from dotenv import load_dotenv
import traceback
import json
from datetime import datetime, timedelta
load_dotenv()

TOKEN = os.getenv("TOKEN")
intents = nextcord.Intents.all()
intents.message_content = True
intents.messages = True
intents.guilds = True
intents.members = True
client = commands.Bot(command_prefix="*", intents=intents)


######################################################################################################################################################
##############################                               Log Handling                                               ##############################
######################################################################################################################################################

async def modlog(interaction: nextcord.Interaction, type, command, user, reason):
              with open("data/channels.json", 'r') as file:
                      channel_id = json.load(file)
              channel = client.get_channel(channel_id["modlog"])
              if type == 1:
                      embed = nextcord.Embed(title="Echo Bot Log", timestamp=datetime.now(), color=nextcord.Color.green)
              elif type ==2:
                      embed = nextcord.Embed(title="Echo Bot Log", timestamp=datetime.now(), color=nextcord.Color.red)
              embed.add_field(name="Command", value=command, inline=False)
              embed.add_field(name="User", value=user, inline=False)
              embed.add_field(name="Reason", value=reason, inline=False)
              try:
                      embed.add_field(name="Executed by", value=f"{interaction.user.mention} ```{interaction.user.id}```", inline=True)
              except AttributeError:
                      pass
              await channel.send(embed=embed)


async def log_action(self, guild: nextcord.Guild, title: str, description: str, color=nextcord.Color.red()):
        with open("data/channels.json", 'r') as file:
                channel_id = json.load(file)
        log_channel_id = client.get_channel(channel_id["modlog"])
        if log_channel_id:
                log_channel = guild.get_channel(log_channel_id)
                if log_channel:
                        embed = nextcord.Embed(title=title, description=description, color=color)
                        await log_channel.send(embed=embed)


async def memberlogs(interaction: nextcord.Interaction, type: int, event: str, user: str, age: str):
        with open("data/channels.json", 'r') as file: 
                channel_id = json.load(file)
        channel = client.get_channel(channel_id["joinleavelog"])
        if type == 1:
                color = nextcord.Color.green()
        elif type == 2:
                color = nextcord.Color.red()
        else:
                color = nextcord.Color.default()

        embed = nextcord.Embed(title="Echo Bot Log", timestamp=datetime.now(), color=color)
        embed.add_field(name="Event", value=event, inline=False)
        embed.add_field(name="User", value=user, inline=False)
        embed.add_field(name="Account Age", value=age, inline=False)
        if channel:
                await channel.send(embed=embed)


async def msgeditlogs(interaction: nextcord.Interaction, type: int, event: str, user: str, before: str, after: str):
        with open("data.channels.json", 'r') as file:
                channel_id = json.load(file)
        channel = client.get_channel(channel_id["msglogs"])
        if type == 1:
                color = nextcord.Color.green()
        elif type == 2:
                color = nextcord.Color.red()
        else:
                color = nextcord.Color.default()

        embed = nextcord.Embed(title="Echo Bot Log", timestamp=datetime.now(), color=color)
        embed.add_field(name="Event", value=event, inline=False)
        embed.add_field(name="User", value=user, inline=False)
        embed.add_field(name="Before Content", value=before, inline=False)
        embed.add_field(name="After Content", value=after, inline=False)
        if channel:
                await channel.send(embed=embed)


async def msgdeletelogs(interaction: nextcord.Interaction, type: int, event: str, user: str, message: str):
        with open("data/channels.json", 'r') as file:
                channel_id = json.load(file)
        channel = client.get_channel(channel_id["modlog"])
        if type == 1:
                color = nextcord.Color.green()
        elif type == 2:
                color = nextcord.Color.red()
        else:
                color = nextcord.Color.default()

        embed = nextcord.Embed(title="Echo Bot Log", timestamp=datetime.now(), color=color)
        embed.add_field(name="Event", value=event, inline=False)
        embed.add_field(name="User", event=user, inline=False)
        embed.add_field(name="Message Deleted", value=message, inline=False)
        if channel:
                await channel.send(embed=embed)


async def roleadd(interaction: nextcord.Interaction, type: int, event: str, user: str, roledsadded: int):
        with open("data/channels.json", 'r') as file:
                channel_id = json.load(file)
        channel = client.get_channel(channel_id["modlog"])
        if type == 1:
                color = nextcord.Color.green()
        elif type == 2:
                color = nextcord.Color.red()
        else:
                color = nextcord.Color.default()

        embed = nextcord.Embed(title="Echo Bot Log", timestamp=datetime.now(), color=color)
        embed.add_field(name="Event", value=event, inline=False)
        embed.add_field(name="User", value=user, inline=False)
        embed.add_field(name="Roles Added", value=roledsadded, inline=False)
        if channel:
                await channel.send(embed=embed)


async def roleremove(interaction: nextcord.Interaction, type: int, event: str, user: str, rolesremoved: int):
        with open("data/channels.json", 'r') as file:
                channel_id = json.load(file)
        channel = client.get_channel(channel_id["modlog"])
        if type == 1:
                color = nextcord.Color.green()
        elif type == 2:
                color = nextcord.Color.red()
        else:
                color = nextcord.Color.default()

        embed = nextcord.Embed(title="Echo Bot Log", timestamp=datetime.now(), color=color)
        embed.add_field(name="Event", value=event, inline=False)
        embed.add_field(name="User", value=user, inline=False)
        embed.add_field(name="Roles Removed", value=user, inline=False)
        if channel:
                await channel.send(embed=embed)


async def logview(interaction: nextcord.Interaction, option, outcome):
        with open("data/channels.json", 'r') as file:
                channel_id = json.load(file)
        channel = client.get_channel(channel_id["modlog"])

        embed = nextcord.Embed(title="Echo Bot Log", timestamp=datetime.now(), color=nextcord.Color.green())
        embed.add_field(name="Choice", value=option, inline=False)
        embed.add_field(name="Outcome", value=f"displayed {outcome}", inline=False)
        embed.add_field(name="Executed by", value=f"{Interaction.user.mention} ```{interaction.user.id}```", inline=False)
        await channel.send(embed=embed)



######################################################################################################################################################
##############################                               Error Handling                                             ##############################
######################################################################################################################################################

async def handle_error(self, interaction: nextcord.Interaction):
        error_text = traceback.format_exc()
        print(error_text)
        embed = nextcord.Embed(title="An error occurred", description="Something went wrong. Open a ticket and ping <@1009455422865932318>", color=nextcord.Color.dark_red())
        await interaction.response.send_message(embed=embed, ephemeral=True)



######################################################################################################################################################
######################################################################################################################################################
######################################################################################################################################################


@client.event
async def on_ready():
        print(f"{client.user} is ready | {client.id}")
        activity = Activity(type=ActivityType.watching, name="your mom shower")
        await client.change_presence(status=Status.online, activity=activity)






for fn in os.listdir("./cogs"):
        if fn.endswith(".py"):
                client.load_extension(f"cogs.{fn[:-3]}")






token = os.getenv('TOKEN')
client.run(TOKEN)