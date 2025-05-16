import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
WELCOME_CHANNEL_ID = int(os.getenv("WELCOME_CHANNEL_ID"))
ROLES_CHANNEL_ID = int(os.getenv("ROLES_CHANNEL_ID"))

intents = discord.Intents.default()
intents.members = True  # Needed for member join/leave events
intents.reactions = True
intents.message_content = True  # Needed to identify messages
intents.guilds = True

bot = commands.Bot(command_prefix="?", intents=intents)

reaction_roles = {
    "🧌": "TOP",  # Emoji : Role name
    "🦧": "JUNGLE",
    "👻": "MID",
    "🔫": "ADC",
    "🦐": "SUPPORT",
}


@bot.event
async def on_ready():
    print(f"Bot connected as {bot.user}")


@bot.event
async def on_member_join(member):
    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    if channel:
        await channel.send(
            f"Welcome to the Archive {member.mention}. Your first task? Choose your identity — react in <#{ROLES_CHANNEL_ID}>"
        )


@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    if channel:
        await channel.send(
            f"🔮 Another page closed. Farewell, {member.display_name}. May Runeterra remember you."
        )


@bot.event
async def on_raw_reaction_add(payload):
    if payload.channel_id == ROLES_CHANNEL_ID:
        guild = bot.get_guild(payload.guild_id)
        role_name = reaction_roles.get(str(payload.emoji))
        if role_name:
            role = discord.utils.get(guild.roles, name=role_name)
            member = guild.get_member(payload.user_id)
            if role and member:
                await member.add_roles(role)
                print(f"Assigned {role_name} to {member.display_name}")


@bot.event
async def on_raw_reaction_remove(payload):
    if payload.channel_id == ROLES_CHANNEL_ID:
        guild = bot.get_guild(payload.guild_id)
        role_name = reaction_roles.get(str(payload.emoji))
        if role_name:
            role = discord.utils.get(guild.roles, name=role_name)
            member = guild.get_member(payload.user_id)
            if role and member:
                await member.remove_roles(role)
                print(f"Removed {role_name} from {member.display_name}")


@bot.event
async def on_ready():
    print(f"Bot connected as {bot.user}")

    # Sync roles for reactions on the role message(s)
    channel = bot.get_channel(ROLES_CHANNEL_ID)
    if channel:
        async for message in channel.history(
            limit=20
        ):  # Adjust limit based on how deep you want to check
            for reaction in message.reactions:
                role_name = reaction_roles.get(str(reaction.emoji))
                if role_name:
                    role = discord.utils.get(message.guild.roles, name=role_name)
                    if not role:
                        print(f"Role {role_name} not found in guild.")
                        continue
                    async for user in reaction.users():
                        if user.bot:
                            continue  # skip bot reactions
                        member = message.guild.get_member(user.id)
                        if member and role not in member.roles:
                            await member.add_roles(role)
                            print(
                                f"Synced: Assigned {role_name} to {member.display_name}"
                            )


bot.run(TOKEN)
