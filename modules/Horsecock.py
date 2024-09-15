import discord
from discord.ext import commands
from discord import app_commands
import requests
from bs4 import BeautifulSoup
from typing import Literal
import re

class Module7(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="horsecock", description="Finds random furry cock")
    @app_commands.describe(
    size="Penis size (optional)",
    body_gender="What gender does it belong to? (optional)",
    other_cock="Or maybe a different type of penis? (optional)",
    how_many="Does the character have more than one penis? Ignores other options above two (optional)"
    )
    async def horsecock(
        self, 
        interaction: discord.Interaction, 
        size: Literal['Micropenis', 'Small', 'Average', 'Big', 'Huge', 'Hyper'] = '',
        body_gender: Literal['Male', 'Gynomorph (female body, male genitals)', 'Herm (female body, both genitals)', 'MaleHerm (male body, both genitals)'] = '',
        other_cock: Literal['Canine_Penis', 'Feline_Penis', 'Bovine_Penis', 'Cervine_Penis', 'Cetacean_Penis', 'Tapering_Penis', 'Humanoid_Penis', 'Unusual_Penis', 'Mechanical_Penis', 'Hemipenes'] = 'Equine_Penis',
        how_many: Literal['Two', 'Three', 'Four', 'Five', 'Six', 'More'] = 'One'
    ):
        
        match size:
            case 'Small':
                size='small_penis+-micropenis'
            case 'Average':
                size='average_penis'
            case 'Big':
                size='big_penis+-huge_penis+-hyper_penis'
            case 'Huge':
                size='huge_penis+-hyper_penis'
            case 'Hyper':
                size='hyper_penis'
        
        match body_gender:
            case 'Gynomorph (female body, male genitals)':
                body_gender='gynomorph'
            case 'Herm (Female body, both genitals)':
                body_gender='herm'
            case 'Maleherm (male body, both genitals)':
                body_gender='maleherm'
                
        match how_many:
            case 'One':
                how_many='-multi_penis+score:>100'
                search_query = "~penis_close-up ~penis_focus ~presenting_penis ~penis_towards_viewer -barely_visible_penis order:random -rating:s -young "+how_many+"+"+size+"+"+body_gender+"+"+other_cock
            case 'Two':
                how_many='2_penises+score:>25'
                search_query = "-barely_visible_penis order:random -rating:s -young "+size+"+"+body_gender+"+"+other_cock+"+"+how_many
            case 'Three':
                how_many='3_penises+score:>25'
                search_query = "-barely_visible_penis order:random -rating:s -young "+other_cock+"+"+how_many
            case 'Four':
                how_many='4_penises+score:>25'
                search_query = "-barely_visible_penis order:random -rating:s -young "+how_many
            case 'Five':
                how_many='5_penises+score:>15'
                search_query = "-barely_visible_penis order:random -rating:s -young "+how_many
            case 'Six':
                how_many='6_penises+score:>15'
                search_query = "-barely_visible_penis order:random -rating:s -young "+how_many
            case 'More':
                how_many='~7_penises+~8_penises+~9_penises+~10_penises+~11_penises+~12_penises+~13_penises+~14_penises+~15_penises+score:>15'
                search_query = "-barely_visible_penis order:random -rating:s -young "+how_many

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
                        embed = discord.Embed(title="Random furry cock ("+stripped_url+")")
                        embed.set_image(url=direct_image_url)
                        await interaction.response.send_message(embed=embed)
                    else:
                        await interaction.response.send_message(f"[Random furry cock video]("+stripped_url+") ")
                    return

            await interaction.response.send_message("No image found, try again later.", ephemeral=True)

        except requests.RequestException as e:
            print(f"Error fetching content: {e}")

async def setup(bot):
    await bot.add_cog(Module7(bot))
    print("Module7 cog loaded and commands registered.")  # Added for debugging