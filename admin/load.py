from discord.ext import commands
from .ownerPerm import NotOwner, is_owner
from .getCogs import find_cog, get_all_cogs


def load(bot: commands.Bot) -> None:
    @bot.command(hidden=True)
    @is_owner()
    async def load(ctx, cog: str):
        to_load: str = find_cog(cog, get_all_cogs())
        print(f'Reloading the following file: {to_reload}')
        try:
            await bot.reload_extension(f"{to_load.lower()}")
        except:
            await ctx.send(f"I am unable to find **{to_load}** extension")
        else:
            await ctx.send(f"Successfully loaded **{to_load}** cog")

    @load.error
    async def say_error(ctx, error):
        if isinstance(error, NotOwner):
            await ctx.send("Permission Denied")
