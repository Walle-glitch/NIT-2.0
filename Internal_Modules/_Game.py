# Internal_Modules/_Game.py

import discord
from discord import app_commands
from discord.ext import commands
import random

# This class defines the interactive view for the Rock, Paper, Scissors game
class GameView(discord.ui.View):
    def __init__(self, player: discord.Member):
        super().__init__(timeout=60)  # The view will time out after 60 seconds
        self.player = player
        self.player_choice = None
        self.bot_choice = None

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        # Only allow the player who started the game to interact
        if interaction.user.id != self.player.id:
            await interaction.response.send_message("This is not your game!", ephemeral=True)
            return False
        return True

    async def on_timeout(self):
        for item in self.children:
            item.disabled = True
        # It's good practice to edit the original message on timeout
        if hasattr(self, 'message'):
            await self.message.edit(content="The game timed out.", view=self)

    def get_winner(self):
        """Determines the winner of the game."""
        if self.player_choice == self.bot_choice:
            return None, "It's a tie!"
        
        winning_moves = {
            "rock": "scissors",
            "paper": "rock",
            "scissors": "paper"
        }
        
        if winning_moves.get(self.player_choice) == self.bot_choice:
            return self.player, f"{self.player.mention} wins!"
        else:
            return "bot", f"The bot wins!"

    async def update_message(self, interaction: discord.Interaction):
        """Called after a choice is made to update the message and show results."""
        for item in self.children:
            item.disabled = True # Disable all buttons

        winner, result_text = self.get_winner()
        
        embed = discord.Embed(
            title="Rock, Paper, Scissors - Results",
            description=result_text,
            color=discord.Color.green() if winner == self.player else discord.Color.red() if winner == "bot" else discord.Color.greyple()
        )
        embed.add_field(name=f"{self.player.display_name}'s choice", value=f"**{self.player_choice.capitalize()}**", inline=True)
        embed.add_field(name="Bot's choice", value=f"**{self.bot_choice.capitalize()}**", inline=True)
        
        await interaction.response.edit_message(embed=embed, view=self)
        self.stop() # Stop the view from listening for more interactions

    @discord.ui.button(label="Rock", style=discord.ButtonStyle.grey, emoji="🪨")
    async def rock(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.player_choice = "rock"
        self.bot_choice = random.choice(["rock", "paper", "scissors"])
        await self.update_message(interaction)

    @discord.ui.button(label="Paper", style=discord.ButtonStyle.grey, emoji="📄")
    async def paper(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.player_choice = "paper"
        self.bot_choice = random.choice(["rock", "paper", "scissors"])
        await self.update_message(interaction)

    @discord.ui.button(label="Scissors", style=discord.ButtonStyle.grey, emoji="✂️")
    async def scissors(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.player_choice = "scissors"
        self.bot_choice = random.choice(["rock", "paper", "scissors"])
        await self.update_message(interaction)

# --- SETUP FUNCTION ---
def setup(bot: commands.Bot):
    """
    This function is called by main.py to register the /game command.
    """
    @bot.tree.command(name="game", description="Play a game of Rock, Paper, Scissors.")
    @app_commands.describe(opponent="The member you want to challenge (optional).")
    async def game(interaction: discord.Interaction, opponent: discord.Member = None):
        """Starts a game of Rock, Paper, Scissors."""
        
        # Currently, the game is only against the bot.
        # The 'opponent' parameter is here for future expansion.
        
        player = interaction.user
        
        embed = discord.Embed(
            title="Rock, Paper, Scissors",
            description=f"{player.mention}, make your choice!",
            color=discord.Color.blue()
        )
        
        view = GameView(player)
        await interaction.response.send_message(embed=embed, view=view)
        view.message = await interaction.original_response() # Store the message for later editing