from discord.ext import commands
from .ownerPerm import NotOwner, is_owner


def reload(bot: commands.Bot) -> None:
    @bot.command(hidden=True)
    @is_owner()
    async def reload(ctx, cog: str):
        await bot.reload_extension(f"cogs.{cog.lower()}")
        await ctx.send(f"Successfully reloaded **{cog}.py**")

    @reload.error
    async def say_error(ctx, error):
        if isinstance(error, NotOwner):
            await ctx.send("Permission Denied")