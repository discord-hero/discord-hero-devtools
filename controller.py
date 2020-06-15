import sys
import traceback

import hero
from hero import async_using_db


class DevToolsController(hero.Controller):
    core: hero.Core

    @async_using_db
    def unload_extension(self, extension: hero.Extension):
        self.core.unload_extension(extension.name)

    @async_using_db
    def load_extension(self, extension_name: str):
        try:
            self.core.load_extension(extension_name)
        except Exception:
            raise
        else:
            extension = self.core.get_extension(extension_name)
            self.core.sync_db(extension.name)

    @async_using_db
    def reload_extension(self, extension: hero.Extension):
        try:
            self.core.reload_extension(extension.name)
        except Exception:
            raise
        else:
            self.core.sync_db(extension.name)

    def print_loading_error(self, extension_name, error: BaseException):
        print(f"Ignoring exception occured when attempting to (re)load extension {extension_name}:", file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
