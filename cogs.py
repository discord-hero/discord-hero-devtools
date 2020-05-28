import hero
import discord

import time
import datetime

import os

from hero import checks
from hero.conf import Extensions
from django.core import management


class DevTools(hero.Cog):
    core: hero.Core

    @hero.command()
    @checks.is_owner()
    async def devtools(self, ctx: hero.Context):
        """Gives information about Discord Hero DevTools and the Bot that is running """
        time_delta = round(self.core.latency*1000)
        msg = "This is the official Discord Hero Developer Tools!\n" \
              "You can use this to load, reload and unload extensions.\n" \
              "This Bot has an average latency of {}".format(time_delta)

        embed = discord.Embed(
            title="Discord Hero DevTools",
            description=msg
            colour=0x529c43
        )

        await ctx.send(embed=embed)

    @hero.command()
    @checks.is_owner()
    async def dvtls_load(self, ctx: hero.Context, extension: str = ''):
        if extension is None:
            return await ctx.send("Please specify an extension to load!")
        if extension == '*':
            loaded = []
            msg = ""
            for ext in self.core.get_extensions():
                self.core.load_extension(ext)
                loaded.append(ext)

            self.core.sync_db()
            for ext in loaded:
                msg += '{}\n'.format(ext)

            return await ctx.send("Extensions have been successfully loaded!\n{}".format(msg))

        self.core.load_extension(extension)
        self.core.sync_db()

        await ctx.send("Extension {} has been loaded!".format(extension))

    @hero.command()
    @checks.is_owner()
    async def dvtls_reload(self, ctx: hero.Context, extension: str = None):
        if extension is None:
            return await ctx.send("Please specify an extension to reload!")

        if extension == '*':
            loaded = []
            msg = ""
            for ext in self.core.get_extensions():
                self.core.unload_extension(ext)
                self.core.load_extension(ext)
                loaded.append(ext)
            self.core.sync_db()

            for ext in loaded:
                msg += '{}\n'.format(ext)

            return await ctx.send("Extensions have been successfully reloaded!\n{}".format(msg))

        self.core.unload_extension(extension)
        self.core.load_extension(extension)
        self.core.sync_db()

        await ctx.send("Extension {} has been reloaded!".format(extension))

    @hero.command()
    @checks.is_owner()
    async def dvtls_unload(self, ctx: hero.Context, extension: str = ''):
        if extension is None:
            return await ctx.send("Please specify an extension to unload!")

        if extenion == '*':
            loaded = []
            msg = ""
            for ext in self.core.get_extensions():
                self.core.unload_extension(ext)
                loaded.append(ext)

            for ext in loaded:
                msg += '{}\n'.format(ext)

            return await ctx.send("Extensions have been successfully unloaded!\n{}".format(msg))

        self.core.unload_extension(extension)
        await ctx.send("Extension {} has been unloaded!".format(extension))
