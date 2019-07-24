from setuptools import setup, find_packages

setup(
    name='cataloji',
    version='0.1.0',
    description='A Slack bot to track Emoji usage',
    author='Jay Kline',
    author_email='jay.kline@target.com',
    url='https://github.com/target/cataloji',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask',
        'influxdb',
        'slackeventsapi'
    ],
    extras_require={
        'dev': [
            'flake8'
        ]
    }
)
