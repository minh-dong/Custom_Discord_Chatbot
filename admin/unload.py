from discord.ext import commands
from .ownerPerm import NotOwner, is_owner
from .getCogs import find_cog, get_all_cogs


def unload(bot: commands.Bot) -> None:
    @bot.command(hidden=True)
    @is_owner()
    async def unload(ctx, cog: str):
        to_unload: str = find_cog(cog, get_all_cogs())
        print(f'Reloading the following file: {to_unload}')
        try:
            await bot.reload_extension(f"{to_reload.lower()}")
        except:
            await ctx.send(f"I am unable to find **{to_unload}** extension")
        else:
            await ctx.send(f"Successfully unloaded **{to_unload}** cog")

    @unload.error
    async def say_error(ctx, error):
        if isinstance(error, NotOwner):
            await ctx.send("Permission Denied")
