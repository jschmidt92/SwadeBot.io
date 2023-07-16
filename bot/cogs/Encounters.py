from discord.ext import commands
from dotenv import load_dotenv
from api.EncounterAPI import *
from models.EncounterModel import Encounter
from models.EncounterCharModel import EncounterChar
from models.EncounterMonModel import EncounterMon
from models.MonsterModel import Monster
import asyncio
import discord
import os

load_dotenv()

TRACKER_CHANNEL_ID = int(os.getenv("TRACKER_CHANNEL_ID"))


class Encounters(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.encounters = {}
        self.encounter = Encounter()
        self.char = EncounterChar()
        self.mon = EncounterMon()
        self.monster = Monster()

    async def cog_check(self, ctx):
        return (
            ctx.channel.id == TRACKER_CHANNEL_ID
            and ctx.guild.me.guild_permissions.manage_messages
        )

    @commands.Cog.listener()
    async def on_command(self, ctx):
        try:
            await asyncio.sleep(30)  # Add a 30-second delay
            await ctx.message.delete()
        except discord.errors.NotFound:
            pass  # The message is already deleted.
        except discord.errors.Forbidden:
            pass  # Bot doesn't have the required permission to delete the message.

    @commands.command(aliases=["ec"])
    @commands.has_role("GameMaster")
    async def encounter_create(
        self,
        ctx,
        name: str = commands.parameter(description="Name of encounter."),
        notes: str = commands.parameter(description="Notes for encounter.", default=""),
    ):
        """
        Description: Create an encounter.

        Params:
        !ec NameOfEncounter

        Example:
        !ec Bandits
        """

        if not isinstance(name, str):
            await ctx.send("Encounter Name must be a string.")
            return

        # self.encounter.insert(name)
        response = create_encounter(name, notes)

        if response.ok:
            await ctx.send(f"Encounter **{name}** created successfully")
        else:
            await ctx.send("An error occured")

    @commands.command(aliases=["efa"])
    @commands.has_role("GameMaster")
    async def encounter_fetch_all(self, ctx):
        """
        Description: Fetch all created encounters.

        Params:
        N/A

        Example:
        !efa
        """

        # encounters = self.encounter.read_all()
        response = get_all_encounters()
        encounters = response.json()

        if response.ok:
            embed = discord.Embed(title="Encounters")
            for encounter in encounters:
                embed.add_field(
                    name="Encounter Name:", value=encounter["name"], inline=False
                )
            await ctx.send(embed=embed)
        else:
            await ctx.send("An error occured")

    @commands.command(aliases=["ed"])
    @commands.has_role("GameMaster")
    async def encounter_delete(
        self,
        ctx,
        encounter_id: int = commands.parameter(description="ID of encounter."),
    ):
        """
        Description: Delete an encounter.

        Params:
        !ed EncounterID

        Example:
        !ed 1
        """

        if not isinstance(encounter_id, int):
            await ctx.send("Encounter ID must be an integer.")
            return

        self.encounter.delete(encounter_id)

        await ctx.send(f"Encounter **{encounter_id}** deleted successfully")

    @commands.command(aliases=["eac"])
    @commands.has_role("GameMaster")
    async def encounter_add_character(
        self,
        ctx,
        encounter_id: int = commands.parameter(description="ID of encounter."),
        player: discord.User = commands.parameter(
            description="User ID of whome to fetch character."
        ),
        name: str = commands.parameter(description="Name of character."),
    ):
        """
        Description: Add character to encounter.

        Params:
        !eac EncounterID UserID NameOfCharacter

        Example:
        !eac 1 1234567890 John
        """

        if not isinstance(encounter_id, int):
            await ctx.send("Encounter ID must be an integer.")
            return

        if not isinstance(player, object):
            await ctx.send("Player must be an object.")
            return

        if not isinstance(name, str):
            await ctx.send("Name must be a string.")
            return

        encounter_character = (encounter_id, player.id, name)
        self.char.insert(encounter_character)

        embed = discord.Embed(
            title="Character Added to Encounter",
            description=f"Character **{name}** added to encounter successfully",
            color=discord.Color.yellow(),
        )

        await ctx.send(embed=embed)

    @commands.command(aliases=["efc"])
    @commands.has_role("GameMaster")
    async def encounter_fetch_characters(
        self,
        ctx,
        encounter_id: int = commands.parameter(description="ID of encounter."),
    ):
        """
        Description: Fetch all characters in encounter.

        Params:
        !efc EncounterID

        Example:
        !efc 1
        """

        if not isinstance(encounter_id, int):
            await ctx.send("Encounter ID must be an int.")
            return

        data = self.char.read(encounter_id)
        encounter_name = data[0] if data else None
        characters = data[1] if data else None

        embed = discord.Embed(
            title="Characters in Encounter",
            description=f"Encounter **{encounter_name}**",
            color=0x00FF00,
        )

        for character in characters:
            embed.add_field(name="Character Name:", value=character[1], inline=False)
            embed.add_field(name="Health:", value=character[2], inline=True)

        await ctx.send(embed=embed)

    @commands.command(aliases=["erc"])
    @commands.has_role("GameMaster")
    async def encounter_remove_character(
        self,
        ctx,
        encounter_id: int = commands.parameter(description="ID of encounter."),
        player: discord.User = commands.parameter(
            description="User ID to whome to fetch character."
        ),
        name: str = commands.parameter(description="Name of character."),
    ):
        """
        Description: Remove a character from encounter.

        Params:
        !erc EncounterID UserID NameOfCharacter

        Example:
        !erc 1 1234567890 John
        """

        if not isinstance(encounter_id, int):
            await ctx.send("Encounter ID must be an integer.")
            return

        if not isinstance(player, object):
            await ctx.send("Player must be an object.")
            return

        if not isinstance(name, str):
            await ctx.send("Name must be a string.")
            return

        encounter_character = (encounter_id, player.id, name)
        self.char.delete(encounter_character)

        embed = discord.Embed(
            title="Character Removed from Encounter",
            description=f"Character **{name}** removed from encounter successfully",
            color=discord.Color.yellow(),
        )

        await ctx.send(embed=embed)

    @commands.command(aliases=["eam"])
    @commands.has_role("GameMaster")
    async def encounter_add_monster(
        self,
        ctx,
        encounter_id: int = commands.parameter(description="ID of encounter."),
        monster_id: int = commands.parameter(description="ID of monster."),
    ):
        """
        Description: Add a monster to encounter.

        Params:
        !eam EncounterID MonsterID

        Example:
        !eam 1 1
        """

        if not isinstance(encounter_id, int):
            await ctx.send("Encounter ID must be an integer.")
            return

        if not isinstance(monster_id, int):
            await ctx.send("Monster ID must be an integer.")
            return

        encounter_monster = (encounter_id, monster_id)
        self.mon.insert(encounter_monster)

        embed = discord.Embed(
            title="Monster Added to Encounter",
            description=f"Monster added to encounter successfully",
            color=discord.Color.yellow(),
        )

        await ctx.send(embed=embed)

    @commands.command(aliases=["efm"])
    @commands.has_role("GameMaster")
    async def encounter_fetch_monsters(
        self,
        ctx,
        encounter_id: int = commands.parameter(description="ID of encounter."),
    ):
        """
        Description: Fetch all monsters in encounter.

        Params:
        !efm EncounterID

        Example:
        !efm 1
        """
        if not isinstance(encounter_id, int):
            await ctx.send("Encounter ID must be an int.")
            return

        data = self.mon.read(encounter_id)
        encounter_name = data[0] if data else None
        monsters = data[1] if data else None

        embed = discord.Embed(
            title="Monsters in Encounter",
            description=f"Encounter **{encounter_name}**",
            color=0x00FF00,
        )

        for monster in monsters:
            embed.add_field(name="Monster Name:", value=monster[1], inline=False)
            embed.add_field(name="Health:", value=monster[2], inline=True)

        await ctx.send(embed=embed)

    @commands.command(aliases=["erm"])
    @commands.has_role("GameMaster")
    async def encounter_remove_monster(
        self,
        ctx,
        encounter_id: int = commands.parameter(description="ID of encounter."),
        monster_id: int = commands.parameter(description="ID of monster."),
    ):
        """
        Description: Remove a monster from encounter.

        Params:
        !erm EncounterID MonsterID

        Example:
        !erm 1 1
        """

        if not isinstance(encounter_id, int):
            await ctx.send("Encounter ID must be an integer.")
            return

        if not isinstance(monster_id, int):
            await ctx.send("Monster ID must be an integer.")
            return

        encounter_monster = (encounter_id, monster_id)
        self.mon.delete(encounter_monster)

        embed = discord.Embed(
            title="Character Removed from Encounter",
            description=f"Monster removed from encounter successfully",
            color=discord.Color.yellow(),
        )

        await ctx.send(embed=embed)

    @commands.command(aliases=["cm"])
    async def create_monster(
        self,
        ctx,
        monster_name: str = commands.parameter(
            description="Name of monster.", default=""
        ),
        attributes: str = commands.parameter(
            description="List of attributes.", default=""
        ),
        skills: str = commands.parameter(description="List of skills.", default=""),
        equipment: str = commands.parameter(
            description="List of equipment.", default=""
        ),
    ):
        """
        Description: Creat a new monster.

        Params:
        !create NameOfMonster "NameOfAttribute:Value,NameOfAttribute:Value" "NameOfSkill:Value,NameOfSkill:Value" "NameOfGear:Amount,NameOfGear:Amount"

        Example:
        !create Bandit "Agility:1d4,Spirit:1d6+2,Strength:1d6" "Athletics:1d6,Common Knowledge:1d6,Persuation:1d6-2" "Machete:1"
        """

        if not isinstance(monster_name, str):
            await ctx.send("Name must be a string.")
            return
        if not isinstance(attributes, str):
            await ctx.send("Attributes must be a string.")
            return
        if not isinstance(skills, str):
            await ctx.send("Skills must be a string.")
            return
        if not isinstance(equipment, str):
            await ctx.send("Equipment must be a string.")
            return

        health = 100
        money = 0

        attributes_string = attributes.replace(",", ", ")
        skills_string = skills.replace(",", ", ")

        monster = (
            monster_name,
            health,
            attributes_string,
            skills_string,
            equipment,
            money,
        )
        self.monster.insert(monster)

        await ctx.send(f"Monster **{monster_name}** created successfully.")

    @commands.command(aliases=["um"])
    async def update_monster(
        self,
        ctx,
        monster_id: int = commands.parameter(description="ID of monster."),
        *,
        kwargs,
    ):
        """
        Description: Update a monster.

        Params:
        !update MonsterID attributes="NameOfAttribute:Value,NameOfAttribute:Value" skills="NameOfSkill:Value,NameOfSkill:Value" equipment="NameOfGear:Amount,NameOfGear:Amount"

        Example:
        !update 1 attributes="Agility:1d4,Spirit:1d6+2,Strength:1d6" skills="Athletics:1d6,Common Knowledge:1d6,Persuation:1d6-2" equipment="Machete:1"
        """

        monster = self.monster.read(monster_id)

        if not monster:
            await ctx.send(f"Monster **{monster[1]}** not found.")
            return

        updates = dict(token.split("=") for token in kwargs.split())

        current_health = monster[2]
        current_attributes = monster[3]
        current_skills = monster[4]
        current_equipment = monster[5]
        current_money = monster[6]

        attributes = updates.get("attributes", current_attributes)
        skills = updates.get("skills", current_skills)
        equipment = updates.get("equipment", current_equipment)
        money = int(updates.get("money", current_money))
        health = int(updates.get("health", current_health))

        if attributes != current_attributes and attributes:
            existing_attributes = dict(
                attr.split(":") for attr in current_attributes.split(",")
            )
            updated_attributes = dict(attr.split(":") for attr in attributes.split(","))
            merged_attributes = {**existing_attributes, **updated_attributes}
            attributes = ",".join(
                [f"{attr}:{value}" for attr, value in merged_attributes.items()]
            )
        elif not current_attributes:
            attributes = updates.get("attributes", "")

        if skills != current_skills and skills:
            existing_skills = dict(
                skill.split(":") for skill in current_skills.split(",")
            )
            updated_skills = dict(skill.split(":") for skill in skills.split(","))
            merged_skills = {**existing_skills, **updated_skills}
            skills = ",".join(
                [f"{skill}:{value}" for skill, value in merged_skills.items()]
            )
        elif not current_skills:
            skills = updates.get("skills", "")

        if equipment:
            existing_equipment = {}
            if current_equipment:
                existing_equipment = dict(
                    item.split(":") for item in current_equipment.split(",")
                )

            for item_update in equipment.split(","):
                item_name, item_quantity = item_update.split(":")
                item_quantity = int(item_quantity)

                if item_quantity <= 0:
                    existing_equipment.pop(item_name, None)
                else:
                    existing_equipment[item_name] = str(item_quantity)

            equipment = ",".join(
                [f"{item}:{quantity}" for item, quantity in existing_equipment.items()]
            )
        elif not current_equipment:
            equipment = updates.get("equipment", "")

        updated_monster = (health, attributes, skills, equipment, money)

        self.monster.update(monster_id, updated_monster)

        await ctx.send(f"Monster **{monster[1]}** updated successfully.")

    @commands.command(aliases=["dm"])
    async def delete_monster(
        self, ctx, monster_id: int = commands.parameter(description="ID of monster.")
    ):
        """
        Description: Delete a character.

        Params:
        !dm MonsterID

        Example:
        !dm 1
        """

        monster = self.monster.read(monster_id)

        if not monster:
            await ctx.send(f"Monster **{monster[1]}** not found.")
            return

        self.monster.delete(monster_id)

        await ctx.send(f"Monster **{monster[1]}** deleted successfully.")


async def setup(bot):
    await bot.add_cog(Encounters(bot))
