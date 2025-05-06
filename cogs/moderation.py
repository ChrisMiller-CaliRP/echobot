from main import modlog, log_action, handle_error
import nextcord
from nextcord.ext import commands
from nextcord import Interaction, SlashOption, activity, ActivityType
import traceback
import json
from datetime import datetime, timedelta
import os
import asyncio


class Moderation(commands.Cog):
              def __init__(self, bot):
                      self.bot = bot
                      with open('data/permissions.json', 'r') as file:
                              self.permissions = json.load(file)

              def banperms(self, member: nextcord.Member):
                      banperms = self.permissions.get('banperms', [])
                      return any(role.id in banperms for role in member.roles)
              
              def kickperms(self, member: nextcord.Member):
                      kickperms = self.permissions.get('kickperms', [])
                      return any(role.id in kickperms for role in member.roles)
              
              def timeoutperms(self, member: nextcord.Member):
                      timeoutperms = self.permissions.get('timeoutperms', [])
                      return any(role.id in timeoutperms for role in member.roles)
              
              def warnperms(self, member: nextcord.Member):
                      warnperms = self.permissions.get('warnperms', [])
                      return any(role.id in warnperms for role in member.roles)
              


              @nextcord.slash_command(name="ban", description="Ban a member from the server")
              async def ban(self, interaction: nextcord.Interaction, user: nextcord.Member, reason: str = "No reason provided"):
                      try:
                              if not self.banperms(interaction.user) and not interaction.user.guild_permissions.administrator:
                                      embed = nextcord.Embed(title="Permission Denied", description="You do not have the required permissions to use this command", color=nextcord.Color.red())
                                      await interaction.response.send_message(embed=embed, ephemeral=True)
                                      await log_action(interaction.guild, "Unauthorized Ban Attemp", f"{interaction.user.mention}, tried to ban {user}", color=nextcord.Color.red())
                                      return
                              
                              await user.ban(reason=reason)
                              embed = nextcord.Embed(title="User Banned", description=f"{user}, has been banned.\n**Reason:** {reason}", color=nextcord.Color.red())
                              await interaction.response.send_message(embed=embed, ephemeral=True)
                              await modlog(interaction, 2 ,f"User Banned", f"{user.mention}\n```{user.id}```", f"{reason}")
                      except Exception as e:
                              await handle_error(interaction)


              @nextcord.slash_command(name="unban", description="Unban a member from the server")
              async def unban(self, interaction: nextcord.Interaction, user_id: str):
                      try:
                              if not self.banperms(interaction.user) and not interaction.user.guild_permissions.administrator:
                                      embed = nextcord.Embed(title="Permission Denied", description="You do not have the required permissions to use this command", color=nextcord.Color.red())
                                      await interaction.response.send_message(embed=embed, ephemeral=True)
                                      await log_action(interaction.guild, "Unauthorized Unban Attempt", f"{interaction.user.mention}, tried to unban <@{user_id}>", color=nextcord.Color.red())
                                      return
                              
                              user_id_int = int(user_id)
                              bans = await interaction.guild.bans().flatten()
                              banned_entry = next((ban for ban in bans if ban.user.id == user_id_int), None)

                              if not banned_entry:
                                      embed = nextcord.Embed(title="Unban Failed", description=f"No active ban found of ID ```{user_id}```", color=nextcord.Color.orange())
                                      await interaction.response.send_message(embed=embed, ephemeral=True)
                                      return
                              
                              await interaction.guild.unban(banned_entry.user)
                              
                              embed = nextcord.Embed(title="User Banned", description=f"{banned_entry.user}, has been unbanned", color=nextcord.Color.green())
                              await interaction.response.send_message(embed=embed)
                              await modlog(interaction, 2, "User Unbanned", f"{banned_entry.user}\n```{user_id}```", "")
                      except Exception as e:
                              await handle_error(interaction)





              @nextcord.slash_command(name="kick", description="Kick a member from the server")
              async def kick(self, interaction: nextcord.Interaction, user: nextcord.Member, reason: str = "No reason provided"):
                      try:
                              if not self.kickperms(interaction.user) and not interaction.user.guild_permissions.administrator:
                                      embed = nextcord.Embed(title="Permission Denied", description="You do not have the required permissions to use this command", color=nextcord.Color.red())
                                      await interaction.response.send_message(embed=embed, ephemeral=True)
                                      await log_action(interaction.guild, "Unauthorized Kick Attempt", f"{interaction.user.mention} tried to kick {user}", color=nextcord.Color.red())
                                      return
                              
                              await user.kick(reason=reason)
                              await interaction.response.send_message(f"{user.mention} just got booted")
                              await modlog(interaction, 2 ,f"User Kicked", f"{user.mention}\n```{user.id}```", f"{reason}")
                      except Exception as e:
                              await handle_error(interaction)



              
              @nextcord.slash_command(name="timeout", description="Timeout a member from the server")
              async def timeout(self, interaction: nextcord.Interaction, user: nextcord.Member, duration_in_minutes: int, reason: str = "No reason provided"):
                      try:
                              if not self.timeoutperms(interaction.user) and not interaction.user.guild_permissions.administrator:
                                      embed = nextcord.Embed(title="Permission Denied", description="You do not have the required permissions to use this command", color=nextcord.Color.red())
                                      await interaction.response.send_message(embed=embed, ephemeral=True)
                                      await log_action(interaction.guild, "Unauthorized Timeout Attempt", f"{interaction.user.mention} tried to kick {user}", color=nextcord.Color.red())
                                      return
                              
                              timeout_duration = timedelta(minutes=duration_in_minutes)
                              await user.edit(timout=nextcord.utils.utcnow() + timeout_duration)

                              try:
                                      embed = nextcord.Embed(title="Chill out", description=f"You have been put in timeout in `{interaction.guild.name}`", color=nextcord.Color.blurple())
                                      embed.add_field(name="**Duration**", value=f"{duration_in_minutes} minutes", inline=False)
                                      embed.add_field(name="**Reason**", value=f"{reason}", inline=False)
                                      await user.send(embed=embed)
                              except:
                                      pass
                              
                              await interaction.response.send_message(f"{user.mention} just got put in the corner for {duration_in_minutes} minutes")
                              await modlog(interaction, 2 ,f"User Timeout", f"{user.mention}\n ```{user.id}```", f"{duration_in_minutes} Minutes for: {reason}")
                      except Exception as e:
                              await handle_error(interaction)


              
              @nextcord.slash_command(name="warn", description="Warn a member in the server")
              async def warn(self, interaction: nextcord.Interaction, user: nextcord.Member, reason: str = "No reason provided"):
                      try:
                              if not self.warnperms(interaction.user) and not interaction.user.guild_permissions.administrator:
                                      embed = nextcord.Embed(title="Permission Denied", description="You do not have the required permissions to use this command", color=nextcord.Color.red())
                                      await interaction.response.send_message(embed=embed, ephemeral=True)
                                      await log_action(interaction.guild, "Unauthrized Warn Attempt", f"{interaction.user.mention} tried to warn {user} for `{reason}`", color=nextcord.Color.red())
                                      return
                              
                              try:
                                      embed = nextcord.Embed(title="Warning", description=f"You have been warned in `{interaction.guild.name}`", color=nextcord.Color.red())
                                      embed.add_field(name="**Reason**", value=reason, inline=False)
                                      await user.send(embed=embed)
                              except:
                                      pass
                              
                              await interaction.response.send_message(f"{user} has been warned fro `{reason}`")
                              await modlog(interaction, 2 ,f"User Warned", f"{user.mention}\n ```{user.id}```", f"{reason}")
                      except Exception as e:
                              await handle_error(interaction)



def setup(bot):
        try:
                bot.add_cog(Moderation(bot))
                print("[Moderation Commands] Successfully Loaded.")
        except Exception as e:
                print(f"[Moderation Commands] Failed to load: {e}")
                traceback.print_exc()