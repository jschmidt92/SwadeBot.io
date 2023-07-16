from discord.ext import commands
from dotenv import load_dotenv
from api.CharacterAPI import *
import asyncio
import discord
import os

load_dotenv()

CHARACTER_CHANNEL_ID = int(os.getenv("CHARACTER_CHANNEL_ID"))


class Characters(commands.Cog):
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
            await asyncio.sleep(30)
            await ctx.message.delete()
        except discord.errors.NotFound:
            pass
        except discord.errors.Forbidden:
            pass

    @commands.command(aliases=["display"])
    async def display_character(
        self,
        ctx,
        character_name: str = commands.parameter(description="Name of character."),
        player: discord.User = commands.parameter(
            description="User ID to fetch character from.", default=None
        ),
    ):
        """
        Description: Display a character.

        Params:
        !display NameOfCharacter UserID

        Example:
        !display John
        !display John 1234567890
        """

        if player is None:
            player_id = str(ctx.author.id)
        else:
            player_id = player.id

        response = get_player_character(player_id, character_name)
        character = response.json()

        if character is None:
            await ctx.author.send("Player doesn't have any characters yet.")
            return

        gear = []
        for item in character["gear"]:
            gear.append(f"{item['name']}")

        powers = []
        for power in character["powers"]:
            powers.append(f"{power['name']}")

        weapons = []
        for weapon in character["weapons"]:
            weapons.append(f"{weapon['name']}")

        attributes = "\n".join(
            f"{k}: **{v}**" for k, v in character["attributes"].items()
        )
        skills = "\n".join(f"{k}: **{v}**" for k, v in character["skills"].items())

        embed = discord.Embed(
            title=f"Character **{character['character_name']}**",
            description=f"Race: **{character['race']}** \n Gender: **{character['gender']}** \n Charisma: **{character['charisma']}** \n Pace: **{character['pace']}** \n Parry: **{character['parry']}** \n Toughness: **{character['toughness']}**",
            color=discord.Color.green(),
        )

        embed.add_field(name="Attributes", value=attributes, inline=False)
        embed.add_field(name="Skills", value=skills, inline=False)
        embed.add_field(name="Gear", value="\n".join(gear), inline=False)
        embed.add_field(name="Hindrances", value=character["hindrances"], inline=False)
        embed.add_field(name="Edges", value=character["edges"], inline=False)
        embed.add_field(name="Powers", value="\n".join(powers), inline=False)
        embed.add_field(name="Weapons", value="\n".join(weapons), inline=False)
        embed.add_field(name="Money", value=str(character["money"]), inline=False)

        await ctx.send(embed=embed)

    @commands.command(aliases=["view"])
    async def view_character(
        self,
        ctx,
        character_name: str = commands.parameter(description="Name of character."),
        player: discord.User = commands.parameter(
            description="User ID to fetch character from.", default=None
        ),
    ):
        """
        Description: Display a character.

        Params:
        !view NameOfCharacter UserID

        Example:
        !view John
        !view John 1234567890
        """

        if player is None:
            player_id = str(ctx.author.id)
        else:
            player_id = player.id

        response = get_player_character(player_id, character_name)
        character = response.json()

        if character is None:
            await ctx.author.send("Player doesn't have any characters yet.")
            return

        gear = []
        for item in character["gear"]:
            gear.append(f"{item['name']}")

        powers = []
        for power in character["powers"]:
            powers.append(f"{power['name']}")

        weapons = []
        for weapon in character["weapons"]:
            weapons.append(f"{weapon['name']}")

        attributes = "\n".join(
            f"{k}: **{v}**" for k, v in character["attributes"].items()
        )
        skills = "\n".join(f"{k}: **{v}**" for k, v in character["skills"].items())

        embed = discord.Embed(
            title=f"Character **{character['character_name']}**",
            description=f"Race: **{character['race']}** \n Gender: **{character['gender']}** \n Charisma: **{character['charisma']}** \n Pace: **{character['pace']}** \n Parry: **{character['parry']}** \n Toughness: **{character['toughness']}**",
            color=discord.Color.green(),
        )

        embed.add_field(name="Attributes", value=attributes, inline=False)
        embed.add_field(name="Skills", value=skills, inline=False)
        embed.add_field(name="Gear", value="\n".join(gear), inline=False)
        embed.add_field(name="Hindrances", value=character["hindrances"], inline=False)
        embed.add_field(name="Edges", value=character["edges"], inline=False)
        embed.add_field(name="Powers", value="\n".join(powers), inline=False)
        embed.add_field(name="Weapons", value="\n".join(weapons), inline=False)
        embed.add_field(name="Money", value=str(character["money"]), inline=False)

        await ctx.author.send(embed=embed)

    @commands.command(aliases=["list"])
    async def list_character(
        self,
        ctx,
        player: discord.User = commands.parameter(
            description="User ID to fetch characters from.", default=None
        ),
    ):
        """
        Description: View list of player characters.

        Params:
        !list UserID

        Example:
        !list 1234567890
        """

        if player is None:
            player_id = str(ctx.author.id)
        else:
            player_id = player.id

        response = get_player_characters(player_id)
        characters = response.json()

        if characters is None:
            await ctx.author.send("Player doesn't have any characters yet.")
            return

        for character in characters:
            gear = []
            for item in character["gear"]:
                gear.append(f"{item['name']}")

            powers = []
            for power in character["powers"]:
                powers.append(f"{power['name']}")

            weapons = []
            for weapon in character["weapons"]:
                weapons.append(f"{weapon['name']}")

            attributes = "\n".join(
                f"{k}: **{v}**" for k, v in character["attributes"].items()
            )
            skills = "\n".join(f"{k}: **{v}**" for k, v in character["skills"].items())

            embed = discord.Embed(
                title=f"Character **{character['character_name']}**",
                description=f"Race: **{character['race']}** \n Gender: **{character['gender']}** \n Charisma: **{character['charisma']}** \n Pace: **{character['pace']}** \n Parry: **{character['parry']}** \n Toughness: **{character['toughness']}**",
                color=discord.Color.green(),
            )

            embed.add_field(name="Attributes", value=attributes, inline=False)
            embed.add_field(name="Skills", value=skills, inline=False)
            embed.add_field(name="Gear", value="\n".join(gear), inline=False)
            embed.add_field(
                name="Hindrances", value=character["hindrances"], inline=False
            )
            embed.add_field(name="Edges", value=character["edges"], inline=False)
            embed.add_field(name="Powers", value="\n".join(powers), inline=False)
            embed.add_field(name="Weapons", value="\n".join(weapons), inline=False)
            embed.add_field(name="Money", value=str(character["money"]), inline=False)

            await ctx.author.send(embed=embed)

    @view_character.error
    async def view_character_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please specify a character name.")


async def setup(bot):
    await bot.add_cog(Characters(bot))
