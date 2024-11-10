import discord
from discord.ext import commands
import datetime

bot = commands.Bot(command_prefix="!")

# Anti-Alt Protection
@bot.event
async def on_member_join(member):
    account_age_threshold = datetime.timedelta(days=30)
    if (datetime.datetime.utcnow() - member.created_at) < account_age_threshold:
        await member.kick(reason="Anti-Alt: Account too new")
        print(f"Kicked {member.name} for suspected alt account.")

# Anti-Nuke Protection
kick_counts = {}

@bot.event
async def on_member_remove(member):
    async for entry in member.guild.audit_logs(limit=1, action=discord.AuditLogAction.kick):
        if entry.target == member:
            user = entry.user
            kick_counts[user.id] = kick_counts.get(user.id, 0) + 1
            if kick_counts[user.id] > 5:
                await member.guild.ban(user, reason="Anti-Nuke: Excessive kicks")
                await member.guild.owner.send(f"{user} has been banned for attempting a nuke.")
                print(f"Banned {user} for suspected nuke attempt.")

# Anti-Link Protection
@bot.event
async def on_message(message):
    trusted_roles = ["Admin", "Moderator"]

    if "http" in message.content or "www" in message.content:
        if not any(role.name in trusted_roles for role in message.author.roles):
            await message.delete()
            await message.channel.send(f"{message.author.mention}, links are not allowed.")
            print(f"Deleted link from {message.author} in {message.channel}.")
    
    await bot.process_commands(message)

TOKEN = 'YOUR_BOT_TOKEN'
bot.run(TOKEN)
