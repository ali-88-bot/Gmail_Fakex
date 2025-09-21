from setuptools import setup, find_packages

setup(
    name="gmail-fakex",
    version="0.1.0",
    author="Ali Nedaiy",
    author_email="alinedaiy88@gmail.com",
    description="Temporary Gmail-like email generator using mail.tm API",
    url="https://github.com/ali-88-bot/Gmail_Fakex",
    packages=find_packages(),
    install_requires=[
        "requests",
        "colorama",
        "plyer",
        "beautifulsoup4"
    ],
    python_requires=">=3.6",
)
