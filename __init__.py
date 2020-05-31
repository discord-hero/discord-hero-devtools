from .cogs import DevTools

from hero import ExtensionConfig, version

__version__ = 'v0.0.2.2.1-beta'

VERSION = version(__version__)


class DevToolsConfig(ExtensionConfig):
    verbose_name = "Developer Tools"
