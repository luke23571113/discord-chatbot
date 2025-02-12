import discord
from discord.ext import commands
from stable_diffusion import StableDiffusion  # Ensure this package exists
import asyncio

## Setting up bot
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')


# IMPLEMENT IMG GEN WITH StableDiffusion
class ImageGenerator:
    def __init__(self):
        self.sd = StableDiffusion()  # Ensure this works with your setup

    async def generate_image(self, prompt):
        try:
            image = self.sd.generate_image(
                prompt=prompt,
                width=512,
                height=512,
                num_inference_steps=50,
                negative_prompt=''
            )
            return image
        except Exception as e:
            print(f"Error generating image: {e}")
            return None

# Handle Discord Commands


# Run Bot
TOKEN = "your_discord_bot_token_here"
# Need token from the Discord Developer Portal

bot.run(TOKEN)
