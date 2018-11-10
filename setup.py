from setuptools import setup

setup(
    name='integra-monitor',
    version="0.0.1",
    packages=['integra'],
    include_package_data=True,
    url='http://integra.org',
    author='Wojciech Gebis',
    author_email='wgebis@gmail.com',
    install_requires=[
        'flask',
        'crcmod',
        'elasticsearch',
        'gunicorn'
    ],
)
