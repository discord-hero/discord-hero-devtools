from .cogs import DevTools

from hero import ExtensionConfig, version

__version__ = '0.0.1-beta'

VERSION = version(__version__)


class DevToolsConfig(ExtensionConfig):
    verbose_name = "Developer Tools"
