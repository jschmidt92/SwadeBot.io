from dotenv import load_dotenv
from discord.ext import commands
from api.StoreAPI import *
import discord
import os


load_dotenv()

MARKET_CHANNEL_ID = int(os.environ["MARKET_CHANNEL_ID"])


class Store(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        return (
            ctx.channel.id == MARKET_CHANNEL_ID
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

    @commands.command()
    async def view_gear(self, ctx):
        """
        Description: View gear in store.

        Params:
        N/A

        Example:
        !view_gear
        """

        response = list_gear()

        if response.status_code != 200:
            await ctx.send("Failed to retrieve gear from the store.")
            return

        gear = response.json()

        if not gear:
            await ctx.send("The store is currently empty.")
            return

        message = "Gear available in the store:\n"
        for item in gear:
            message += f"{item['name']}: **${item['cost']}**\n"

        await ctx.send(message)

    @commands.command()
    async def view_weapons(self, ctx):
        """
        Description: View weapons in store.

        Params:
        N/A

        Example:
        !view_weapons
        """

        response = list_weapons()

        if response.status_code != 200:
            await ctx.send("Failed to retrieve weapons from the store.")
            return

        weapons = response.json()

        if not weapons:
            await ctx.send("The store is currently empty.")
            return

        message = "Weapons available in the store:\n"
        for item in weapons:
            message += f"{item['name']}: **${item['cost']}** Min-Strength: **{item['min_str']}**\n"

        await ctx.send(message)

    @commands.command()
    async def buy_gear(
        self,
        ctx,
        # player: discord.User = commands.parameter(
        #     description="User ID to whom to fetch character."
        # ),
        character_name: str = commands.parameter(description="Name of character."),
        gear_name: str = commands.parameter(description="Name of gear."),
        quantity: int = commands.parameter(description="Quantity to buy", default=1),
        player_id: int = commands.parameter(
            description="User ID to fetch character", default=None
        ),
    ):
        """
        Description: Buy an gear from store.

        Params:
        !buy_gear NameOfCharacter NameOfGear Quantity

        Example:
        !buy_gear John Tent 1
        !buy_gear John Tent 1 1234567890
        """

        if player_id is None:
            player_id = str(ctx.author.id)
        else:
            player_id = player_id

        # response = buy_gear(player.id, character_name, gear_name, quantity)
        response = buy_gear(player_id, character_name, gear_name, quantity)

        if response.ok:
            await ctx.send(
                f"Your character **{character_name}** has bought {quantity} unit(s) of {gear_name}."
            )
        else:
            await ctx.send("An error occurred.")

    @commands.command()
    async def buy_weapon(
        self,
        ctx,
        # player: discord.User = commands.parameter(
        #     description="User ID to whom to fetch character."
        # ),
        character_name: str = commands.parameter(description="Name of character."),
        weapon_name: str = commands.parameter(description="Name of weapon."),
        quantity: int = commands.parameter(description="Quantity to buy", default=1),
        player_id: int = commands.parameter(
            description="User ID to fetch character", default=None
        ),
    ):
        """
        Description: Buy an weapon from store.

        Params:
        !buy_weapon NameOfCharacter NameOfWeapon Quantity

        Example:
        !buy_weapon John Machete 1
        !buy_weapon John Machete 1 1234567890
        """

        # response = buy_weapon(player.id, character_name, weapon_name, quantity)

        if player_id is None:
            player_id = str(ctx.author.id)
        else:
            player_id = player_id

        response = buy_weapon(player_id, character_name, weapon_name, quantity)

        if response.ok:
            await ctx.send(
                f"Your character **{character_name}** has bought {quantity} unit(s) of {weapon_name}."
            )
        else:
            await ctx.send("An error occurred.")

    @commands.command()
    async def view_money(
        self,
        ctx,
        character_name: str = commands.parameter(description="Name of character"),
        player_id: int = commands.parameter(
            description="User ID to fetch character", default=None
        ),
    ):
        """
        Description: View character's money.

        Params:
        !view_money NameOfCharacter UserID

        Example:
        !view_money John
        """

        if player_id is None:
            player_id = str(ctx.author.id)
        else:
            player_id = player_id

        response = check_money(player_id, character_name)

        if response.ok:
            money = response.json()
            await ctx.author.send(f"Character **{character_name}** has ${money}.")
        else:
            await ctx.send("An error occurred.")

    @view_gear.error
    @view_weapons.error
    @buy_gear.error
    @buy_weapon.error
    @view_money.error
    async def command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(
                "Missing argument. Please check the command syntax and try again."
            )


async def setup(bot):
    await bot.add_cog(Store(bot))
