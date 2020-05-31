#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Extension setup script

Use `python setup.py publish` to publish your Extension to PyPI.
Alternatively, publish a release on GitHub to trigger this automatically.
Make sure to configure this script beforehand (see below).
"""

import codecs
import os
import re
from setuptools import find_packages, setup, Command
from shutil import rmtree
import stat
import sys


# CONFIGURE THESE #

EXTENSION_NAME = "devtools"

AUTHOR_NAME = "EraseKesu"

AUTHOR_EMAIL = "eitan.olchik@gmail.com"

REPOSITORY_URL = "https://github.com/discord-hero/discord-hero-devtools"  # GitHub recommended


# CUSTOMIZABLE #

PYTHON_REQUIREMENT = '>= 3.7.0'

REQUIREMENTS = [
    "discord-hero>=0.1.0b0",
]


# FROM HERE DO NOT TOUCH #

try:
    from dotenv import load_dotenv
except ImportError:
    pass
else:
    load_dotenv()


here = os.path.abspath(os.path.dirname(__file__))

NAMESPACE_PREFIX = 'hero.extensions.'

_, _EXTENSION_NAME = os.path.split(here)
# if this is a local extension and setup.py is not run under CI,
# we need to point out to the user that they need to rename the
# extension directory in order for it to work locally
if EXTENSION_NAME != _EXTENSION_NAME and not os.getenv('CI', False):
    raise ValueError("directory needs to be named {0} in order for the "
                     "{0} extension to function normally".format(EXTENSION_NAME))

with codecs.open(os.path.join(here, 'README.rst'), encoding='utf-8') as readme_file:
    readme = readme_file.read()


readme_lines = readme.splitlines()
if len(readme_lines) < 4:
    description = readme_lines[0]
else:
    description = ''
    readme_lines = readme_lines[3:]
    for line in readme_lines:
        if line:
            description += ' ' + line if description else line
        else:
            break


with codecs.open(os.path.join(here, '__init__.py'), encoding='utf-8') as f:
    VERSION = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        f.read(), re.MULTILINE).group(1)

packages = [
    '{}{}'.format(NAMESPACE_PREFIX, EXTENSION_NAME)
] + [
    '{}{}.{}'.format(NAMESPACE_PREFIX, EXTENSION_NAME, name)
    for name in find_packages(exclude=['migrations', '*.migrations'])
]


def genpath(package_name):
    if package_name == '{}{}'.format(NAMESPACE_PREFIX, EXTENSION_NAME):
        return '.'
    else:
        package_name = package_name[len('{}{}.'.format(NAMESPACE_PREFIX, EXTENSION_NAME)):]
        _package = ['.'] + package_name.split('.')
        path = os.path.join(*_package)
        return path


package_dir = {name: genpath(name) for name in packages}


class PublishCommand(Command):
    """Support setup.py publish."""

    description = 'Build and publish the package.'
    user_options = [
        ('test', None, 'publish to TestPyPI')
    ]

    def initialize_options(self):
        self.test = False

    def finalize_options(self):
        pass

    def run(self):
        def onerror(func, path, exc_info):
            """``shutil.rmtree`` error handler that helps deleting read-only files on Windows."""
            if not os.access(path, os.W_OK):
                os.chmod(path, stat.S_IWUSR)
                func(path)
            else:
                raise exc_info[0](exc_info[1])

        try:
            print('Removing previous buildsâ€¦')
            rmtree(os.path.join(here, 'dist'), onerror=onerror)
        except (OSError, FileNotFoundError):
            pass

        print('Building Source and Wheel distribution...')
        os.system('{0} setup.py sdist bdist_wheel'.format(sys.executable))

        if self.test:
            print('Uploading the package to TestPyPI via Twine...')
            os.system('twine upload --repository testpypi dist/*')
        else:
            print('Uploading the package to PyPI via Twine...')
            os.system('twine upload dist/*')

        sys.exit()


setup(
    author=AUTHOR_NAME,
    author_email=AUTHOR_EMAIL,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Plugins',
        'Framework :: AsyncIO',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: Apache Software License',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Communications :: Chat',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    cmdclass={
        'publish': PublishCommand,
    },
    description=description,
    install_requires=REQUIREMENTS,
    license="Apache-2.0 OR MIT",
    long_description=readme,
    long_description_content_type='text/x-rst',
    include_package_data=True,
    keywords='discord-hero {} discord bot'.format(EXTENSION_NAME),
    name='discord-hero-{}'.format(EXTENSION_NAME),
    packages=packages,
    package_dir=package_dir,
    python_requires=PYTHON_REQUIREMENT,
    url=REPOSITORY_URL,
    version=VERSION,
    zip_safe=False,
)
