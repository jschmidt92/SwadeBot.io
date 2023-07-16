from dotenv import load_dotenv
from discord.ext import commands

from api.MoneyAPI import *

import discord
import os

load_dotenv()

CHARACTER_CHANNEL_ID = int(os.environ["CHARACTER_CHANNEL_ID"])


class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        return (
            ctx.channel.id == CHARACTER_CHANNEL_ID
            and ctx.guild.me.guild_permissions.manage_messages
        )

    @commands.Cog.listener()
    async def on_command(self, ctx):
        try:
            await ctx.message.delete()
        except discord.errors.NotFound:
            pass
        except discord.errors.Forbidden:
            pass

    @commands.command(aliases=["gm"])
    @commands.has_role("GameMaster")
    async def give_money(
        self,
        ctx,
        player: discord.User = commands.parameter(
            description="User ID to whom to fetch character."
        ),
        character_name: str = commands.parameter(
            description="Name of character of whom to give money."
        ),
        amount: int = commands.parameter(description="Amount of money."),
    ):
        """
        Description: Give money to player character.

        Params:
        !gm UserID NameOfCharacter Amount

        Example:
        !gm 1234567890 John 100
        """

        response = add_money(player.id, character_name, amount)

        if response.ok:
            await ctx.send(
                f"Gave {amount} money to {character_name} belonging to {player.name}."
            )
        else:
            await ctx.send("An error occurred.")

    @commands.command(aliases=["rm"])
    @commands.has_role("GameMaster")
    async def take_money(
        self,
        ctx,
        player: discord.User = commands.parameter(
            description="User ID of whom to fetch character."
        ),
        character_name: str = commands.parameter(
            description="Name of character of whom to remove money."
        ),
        amount: int = commands.parameter(description="Amount of money."),
    ):
        """
        Description: Remove money from player character.

        Params:
        !rm UserID NameOfCharacter Amount

        Example:
        !rm 1234567890 John 100
        """

        response = subtract_money(player.id, character_name, amount)

        if response.ok:
            await ctx.send(
                f"Took {amount} money to {character_name} belonging to {player.name}."
            )
        else:
            await ctx.send("An error occurred.")

    @give_money.error
    @take_money.error
    async def command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.author.send(
                "You must specify a user, character name, and amount of money to give or take."
            )


async def setup(bot):
    await bot.add_cog(Economy(bot))
