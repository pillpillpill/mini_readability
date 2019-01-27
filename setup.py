from os.path import join, dirname

from setuptools import setup, find_packages

setup(
    name='mini_readability',
    version='0.0.1',
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    url='https://github.com/pillpillpill/mini_readability',
    author='Ayrat Khaziev',
    author_email='xa3ieb@gmail.com',
    packages=find_packages(),
    install_requires=[
        'requests',
        'bs4',
        'lxml',
    ],
    python_requires='>=3'
)