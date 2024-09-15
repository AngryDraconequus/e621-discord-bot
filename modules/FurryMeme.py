import discord
from discord.ext import commands
from discord import app_commands
import requests
from bs4 import BeautifulSoup
from typing import Literal
import re

class Module5(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="furrymeme", description="Finds random furry meme")
    @app_commands.describe(
    rating="Define age rating (optional, SFW by default)"
    )
    async def furrymeme(
        self, 
        interaction: discord.Interaction, 
        rating: Literal['SFW', 'Risque', 'NSFW'] = 'SFW',
    ):
    
        match rating:
            case 'SFW':
                rating='rating:safe'
            case 'Risque':
                rating='rating:questionable'        
            case 'NSFW':
                rating='rating:explicit'   
                               
        search_query = "~meme ~reaction_image -meme_clothing order:random score:>50 "+rating

        headers = {
            "User-Agent": "Discord Bot (https://your-bot-url.com)",
            "Accept": "text/html"
        }
        
        try:
            response = requests.get(f"https://e621.net/posts?tags={search_query}", headers=headers, timeout=8)
            if response.status_code != 200:
                await interaction.response.send_message("Error: Unable to fetch image. Please try again later.", ephemeral=True)
                return  
            soup = BeautifulSoup(response.content, 'html.parser')
            post_elements = soup.find_all('a', href=re.compile(r'^/posts/\d+'))
            
            for post_element in post_elements:
                direct_image_url = None
                image_page_url = f"https://e621.net{post_element['href']}"
                image_page_response = requests.get(image_page_url, headers=headers, timeout=8)
                stripped_url = image_page_url.split('?', 1)[0]
                if image_page_response.status_code == 200:
                    image_page_soup = BeautifulSoup(image_page_response.content, 'html.parser')
                    direct_image_element = image_page_soup.find('a', href=re.compile(r'^https://static1\.e621\.net/data/[a-z0-9]{2}/[a-z0-9]{2}/[a-z0-9]{32}\.(jpg|jpeg|png|gif|webp|mp4|webm)'))
                    if direct_image_element:
                        direct_image_url = direct_image_element['href']
                
                if direct_image_url:
                    if direct_image_url.endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
                        embed = discord.Embed(title="Random furry meme ("+stripped_url+")")
                        embed.set_image(url=direct_image_url)
                        await interaction.response.send_message(embed=embed)
                    else:
                        await interaction.response.send_message(f"[Random furry meme video]("+stripped_url+") ")
                    return
            
            await interaction.response.send_message("No memes found, try again later.", ephemeral=True)
            
        except requests.RequestException as e:
            print(f"Error fetching content: {e}")

async def setup(bot):
    await bot.add_cog(Module5(bot))
    print("Module5 cog loaded and commands registered.")  # Added for debugging