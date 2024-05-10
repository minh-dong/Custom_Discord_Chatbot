from discord.ext import commands
from .ownerPerm import NotOwner, is_owner


def unload(bot: commands.Bot) -> None:
    @bot.command(hidden=True)
    @is_owner()
    async def unload(ctx, cog: str):
        print('We are unloading')
        await bot.unload_extension(f"cogs.{cog.lower()}")
        await ctx.send(f"Successfully unloaded **{cog}.py**")

    @unload.error
    async def say_error(ctx, error):
        if isinstance(error, NotOwner):
            await ctx.send("Permission Denied")