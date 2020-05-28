import hero
import discord

import time
import datetime

from hero import checks


class DevTools(hero.Cog):
    core: hero.Core

    @hero.command()
    @checks.is_owner()
    async def devtools(self, ctx: hero.Context):
        """Gives information about Discord Hero DevTools and the Bot that is running """
        time_delta = round(core.latency*1000)
        msg = "This is the official Discord Hero Developer Tools!\n" \
              "You can use this to load, reload and unload extensions.\n" \
              "This Bot has an average latency of {}".format(time_delta)

        embed = discord.Embed(
            title="Discord Hero DevTools",
            description=msg
            colour=0x529c43
        )

        await ctx.send(embed=embed)
