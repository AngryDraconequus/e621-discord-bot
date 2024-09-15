import discord
from discord.ext import commands
from discord import app_commands
import requests
from bs4 import BeautifulSoup
from typing import Literal
import re

class Module2(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="furrymale", description="Finds random furry image with male character(s)")
    @app_commands.describe(
    body_type="Body type to look for (optional)",
    body_part="What body part to focus on (optional)",
    how_many="How many characters (optional)",
    kind="What kind of characters (optional, all except for feral by default)"
    )
    async def furrymale(
        self, 
        interaction: discord.Interaction, 
        body_type: Literal['Femboy', 'Skinny', 'Thicc', 'Athletic', 'Muscular', 'Chubby'] = '',
        body_part: Literal['Butt', 'Big_Butt', 'Penis', 'Big_Penis', 'Balls', 'Anus', 'Bulge'] = '',
        how_many: Literal['Solo', 'Duo', 'Trio', 'Group'] = 'Solo',
        kind: Literal['Anthro', 'Feral', 'Taur', 'Humanoid'] = '-feral',
    ):
    
        match body_type:
            case 'Skinny':
                body_type='slim'
            case 'Athletic':
                body_type='athletic'
            case 'Muscular':
                body_type='muscular'
            case 'Chubby':
                body_type='slightly_chubby'
            case 'Thicc':
                body_type='thick_thighs+wide_hips+-overweight+-slightly_chubby'
                
        match how_many:
            case 'Duo':
                how_many='Duo+-female+-intersex'
            case 'Trio':
                how_many='Trio+-female+-intersex'
            case 'Group':
                how_many='Group+-female+-intersex+-trio'
                
        match body_part:
            case 'Butt':
                body_type='~presenting_butt+~butt_focus'
            case 'Big_Butt':
                body_type='~presenting_butt+~butt_focus+big_butt'
            case 'Penis':
                body_type='~presenting_penis+~penis_focus'
            case 'Big_Penis':
                body_type='~presenting_penis+~penis_focus+big_penis'
            case 'Balls':
                body_type='~presenting_balls+~balls_focus'
            case 'Anus':
                body_type='~presenting_anus+~anus_focus'
                
        match kind:
            case 'Anthro':
                kind='Anthro+-feral'
            case 'Humanoid':
                kind='humanoid+-feral'

        search_query = "male order:random score:>125 -rating:s -young "+kind+"+"+how_many+"+"+body_part+"+"+body_type

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
                        embed = discord.Embed(title="Random furry male ("+stripped_url+")")
                        embed.set_image(url=direct_image_url)
                        await interaction.response.send_message(embed=embed)
                    else:
                        await interaction.response.send_message(f"[Random furry male video]("+stripped_url+") ")
                    return

            await interaction.response.send_message("No image found, try again later.", ephemeral=True)

        except requests.RequestException as e:
            print(f"Error fetching content: {e}")

async def setup(bot):
    await bot.add_cog(Module2(bot))
    print("Module2 cog loaded and commands registered.")  # Added for debugging