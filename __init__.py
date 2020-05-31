from hero import ExtensionConfig, version

__version__ = '0.0.2b0'

VERSION = version(__version__)


class DevToolsConfig(ExtensionConfig):
    verbose_name = "Developer Tools"
