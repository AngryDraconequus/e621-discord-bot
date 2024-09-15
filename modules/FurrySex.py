import discord
from discord.ext import commands
from discord import app_commands
import requests
from bs4 import BeautifulSoup
from typing import Literal
import re

class Module8(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="furrysex", description="Finds random furry image with sexual interaction")
    @app_commands.describe(
    genders="Define interacting genders (optional)",
    sextype="Define specific type of sex(optional)",
    how_many="How many characters (optional, duo by default)",
    kind="What kind of characters (optional, all except for feral by default)"
    )
    async def furrysex(
        self, 
        interaction: discord.Interaction, 
        genders: Literal['Male/Female', 'Female/Female', 'Male/Male', 'Gynomorph/Female', 'Gynomorph/Male', 'Gynomorph/Gynomorph', 'Andromorph/Gynomorph', 'Andromorph/Female', 'Andromorph/Male'] = '',
        sextype: Literal['Anal', 'Vaginal', 'Oral', 'Handjob', 'Fingering', 'Titfuck', 'Thigh_Sex', 'Urethral', 'Footjob', 'Frottage', 'Tribadism'] = '',
        how_many: Literal['Duo', 'Trio', 'Foursome', 'Group'] = 'Duo',
        kind: Literal['Anthro', 'Feral', 'Taur', 'Humanoid'] = '-feral',
    ):
    
        match genders:
            case 'Gynomorph/Female':
                genders='~Gynomorph/Female+~herm/female'
            case 'Gynomorph/Male':
                genders='~Gynomorph/male+~herm/male'
            case 'Gynomorph/Gynomorph':
                genders='~Gynomorph/Gynomorph+~Gynomorph/herm+~herm/herm'
            case 'Andromorph/Gynomorph':
                genders='~andromorph/gynomorph+~andromorph/herm+~maleherm/gynomorph+~maleherm/herm'
            case 'Andromorph/Female':
                genders='~Andromorph/Female+~maleherm/female'
            case 'Andromorph/Male':
                genders='~Andromorph/Male+~maleherm/male'       
                
        match how_many:
            case 'Group':
                how_many='Group+-duo+-trio+-foursome'
                
        match kind:
            case 'Anthro':
                kind='Anthro+-feral'
            case 'Humanoid':
                kind='humanoid+-feral'
                
        search_query = "sex order:random score:>125 -rating:s -young "+genders+"+"+sextype+"+"+how_many+"+"+kind

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
                        embed = discord.Embed(title="Random furry sex ("+stripped_url+")")
                        embed.set_image(url=direct_image_url)
                        await interaction.response.send_message(embed=embed)
                    else:
                        await interaction.response.send_message(f"[Random furry sex video]("+stripped_url+") ")
                    return
                    
            await interaction.response.send_message("No image found, try again later.", ephemeral=True)
            
        except requests.RequestException as e:
            print(f"Error fetching content: {e}")

async def setup(bot):
    await bot.add_cog(Module8(bot))
    print("Module8 cog loaded and commands registered.")  # Added for debugging