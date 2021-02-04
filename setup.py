from setuptools import setup

with open('mytable/version.py') as f:
    __version__ = f.read().split('=', 1)[1].strip()

setup(
    name='mytable',
    version=__version__,
    description="Mytable implements an efficient approach to store struct instances in a binary file.",
    author='Alexander Khlebushchev',
    packages=[
        'mytable',
    ],
    zip_safe=False,
)
