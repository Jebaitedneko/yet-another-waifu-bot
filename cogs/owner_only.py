import discord
from discord.ext.commands import Cog, Context, NotOwner, command
from my_bot import MyBot
from player import players
from bot_config import bot_config
import aiohttp


class OwnerOnly(Cog, name="Owner Commands"):
    
    def __init__(self, bot: MyBot):
        self.bot = bot
    
    async def cog_command_error(self, ctx: Context, error):
        if isinstance(error, NotOwner):
            await ctx.send("You're not my dad.")
        raise error
    
    async def cog_check(self, ctx: Context):
        if await self.bot.is_owner(ctx.message.author):
            return True
        raise NotOwner

    @command()
    async def dismiss(self, ctx: Context):
        await ctx.message.add_reaction('👌')
        await self.bot.logout()
    
    @command()
    async def change_avatar(self, ctx: Context, url: str):
        with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                avatar_b = await resp.read()
                await self.bot.edit_profile(avatar=avatar_b)
    
    @command()
    async def add_players(self, ctx: Context):
        guild = ctx.message.guild
        for member in guild.members:
            if not member.bot:
                players.add_player(member.id, member.name)
        await ctx.send("Updated player database")

    @command()
    async def set_spawn_channel(self, ctx: Context, channel: discord.TextChannel):
        bot_config.update_config(channel.id)
        await ctx.send("Spawn channel set to {}".format(channel.mention))
    
    @command()
    async def say(self, ctx: Context, channel_id: int, *args: str):
        channel = self.bot.get_channel(channel_id)
        msg = ' '.join(args)
        if ctx.message.author.id == 178887072864665600:
            await channel.send(msg)


def setup(bot: MyBot):
    c = OwnerOnly(bot)
    bot.add_cog(c)

