import setuptools

with open('requirements.txt', 'r') as fp:
    requirements = [i for i in fp.readlines()]

setuptools.setup(
    name='marketplace-scraper',
    version='0.1.0',
    packages=setuptools.find_packages(),
    install_requires=requirements
)
