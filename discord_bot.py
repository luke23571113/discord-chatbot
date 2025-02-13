import discord
from discord.ext import commands
from stable_diffusion import StableDiffusion  # Ensure this package is installed and properly configured
import os

# Initialize the bot with default intents
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# Event triggered when the bot is ready
@bot.event
async def on_ready():
    await bot.tree.sync()  # Synchronize slash commands with Discord
    print(f'Logged in as {bot.user}')

# Class to handle image generation using Stable Diffusion
class ImageGenerator:
    def __init__(self):
        self.sd = StableDiffusion()  # Initialize the StableDiffusion model

    async def generate_image(self, prompt):
        try:
            # Generate the image based on the prompt
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

# Slash command to generate an image from a prompt
@bot.tree.command(name="generate", description="Generate an image based on a prompt")
async def generate(interaction: discord.Interaction, prompt: str):
    await interaction.response.defer()  # Defer the response to allow time for image generation
    generator = ImageGenerator()
    await interaction.followup.send("Generating image...")

    image = await generator.generate_image(prompt)

    if image:
        # Save the generated image to a file
        image_path = "generated_image.png"
        image.save(image_path)

        # Send the image file in the Discord channel
        with open(image_path, "rb") as file:
            await interaction.followup.send(file=discord.File(file, filename="image.png"))

        # Optionally, delete the image file after sending
        os.remove(image_path)
    else:
        await interaction.followup.send("Failed to generate image.")

# Run the bot with your Discord token
TOKEN = "your_discord_bot_token_here"
bot.run(TOKEN)
