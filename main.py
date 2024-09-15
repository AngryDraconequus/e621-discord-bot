import discord
from discord.ext import commands
import json
import os
import asyncio

# Load the configuration file
with open('config.json', 'r') as f:
    config = json.load(f)

# Initialize the bot with command prefix and intents
intents = discord.Intents.default()
intents.message_content = True  # Enable the privileged intent for message content

bot = commands.Bot(command_prefix=config['Bot_name']['command_prefix'], intents=intents)

# Register commands and sync them with Discord
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    
	# Sync slash commands after all extensions are loaded
    try:
        synced = await bot.tree.sync()  # Sync the slash commands with Discord
        print(f"Synced {len(synced)} command(s): {[cmd.name for cmd in synced]}")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

# Dynamically load the modules from the 'modules' folder
async def load_extensions():
    modules_folder = config['Bot_name']['modules_folder']
    for filename in os.listdir(modules_folder):
        if filename.endswith('.py'):
            try:
                await bot.load_extension(f"{modules_folder}.{filename[:-3]}")
                print(f"Loaded extension '{filename[:-3]}'")
            except Exception as e:
                print(f"Failed to load extension {filename}: {e}")

async def main():
    await load_extensions()
    await bot.start(config['Bot_name']['token'])

if __name__ == "__main__":
    asyncio.run(main())
