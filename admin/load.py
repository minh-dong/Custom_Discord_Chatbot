from discord.ext import commands
from .ownerPerm import NotOwner, is_owner


def load(bot: commands.Bot) -> None:
    @bot.command(hidden=True)
    @is_owner()
    async def load(ctx, cog: str):
        await bot.load_extension(f"cogs.{cog.lower()}")
        await ctx.send(f"Successfully loaded **{cog}.py**")

    @load.error
    async def say_error(ctx, error):
        if isinstance(error, NotOwner):
            await ctx.send("Permission Denied")
