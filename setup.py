from setuptools import setup

setup(
    name='UwoCalendar',
    author='Peter Argall',
    author_email='peter@argall.ca',
    url='https://github.com/pargall/UWO-Cal',
    version='1.0.3',
    packages=['uwoCalendar',],
    license='LICENSE.txt',
    long_description=open('README.txt').read(),
    install_requires=[
        "icalendar >= 3.0",
        "lxml >= 3.3.5",
    ],
)