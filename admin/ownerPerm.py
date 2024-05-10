from discord.ext import commands


class NotOwner(commands.CheckFailure):
    ...


def is_owner():
    async def predicate(ctx):
        if ctx.author.id != ctx.guild.owner_id:
            raise NotOwner("Hey you are not the owner")
        return True
    return commands.check(predicate)