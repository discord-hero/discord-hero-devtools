import datetime
import os
import time

import discord

import hero
from hero import checks

from .controller import DevToolsController


class DevTools(hero.Cog):
    core: hero.Core
    ctl: DevToolsController

    @hero.command()
    @checks.is_owner()
    async def load(self, ctx: hero.Context, *extensions: str):
        if not extensions:
            extensions = self.core.get_extensions()

        failed = []
        for extension in extensions:
            try:
                await self.ctl.load_extension(extension)
            except Exception as ex:
                failed.append(extension)
                if hero.TEST:
                    await self.core.report_error(ctx, ex)
                self.ctl.print_loading_error(extension.name, ex)

        msg = "Extensions have been loaded!\n{}".format('\n'.join([f"**{ext}**" for ext in extensions if ext not in failed]))
        if failed:
            msg += "\nFailed:\n"
            msg += '\n'.join([f"**{ext}**" for ext in failed])
        await ctx.send(msg)

    @hero.command()
    @checks.is_owner()
    async def reload(self, ctx: hero.Context, *extensions: hero.Extension):
        await ctx.send(str([cmd for cmd in self.core.all_commands.copy()]))
        if not extensions:
            extensions = self.core.get_extensions()

        failed = []
        for extension in extensions:
            try:
                await self.ctl.reload_extension(extension)
            except Exception as ex:
                failed.append(extension)
                if hero.TEST:
                    await self.core.report_error(ctx, ex)
                self.ctl.print_loading_error(extension.name, ex)

        msg = "Extensions have been reloaded!\n{}".format('\n'.join([f"**{ext}**" for ext in extensions if ext not in failed]))
        if failed:
            msg += "\nFailed:\n"
            msg += '\n'.join([f"**{ext}**" for ext in failed])
        await ctx.send(msg)

    @hero.command()
    @checks.is_owner()
    async def unload(self, ctx: hero.Context, *extensions: hero.Extension):
        if not extensions:
            extensions = self.core.get_extensions()

        for extension in extensions:
            await self.ctl.unload_extension(extension)

        msg = "Extensions have been unloaded!\n{}".format('\n'.join([f"**{ext}**" for ext in extensions]))
        await ctx.send(msg)
