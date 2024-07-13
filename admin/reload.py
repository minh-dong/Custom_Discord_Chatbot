from discord.ext import commands
from .ownerPerm import NotOwner, is_owner
from .getCogs import find_cog, get_all_cogs


def reload(bot: commands.Bot) -> None:
    @bot.command(hidden=True)
    @is_owner()
    async def reload(ctx, cog: str):
        to_reload: str = find_cog(cog, get_all_cogs())
        print(f'Reloading the following file: {to_reload}')
        try:
            await bot.reload_extension(f"{to_reload.lower()}")
        except:
            await ctx.send(f"I am unable to find **{to_reload}** extension")
        else:
            await ctx.send(f"Successfully reloaded **{to_reload}** cog")

    @reload.error
    async def say_error(ctx, error):
        if isinstance(error, NotOwner):
            await ctx.send("Permission Denied")
