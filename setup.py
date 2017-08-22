import os
from pip.req import parse_requirements
from setuptools import setup, find_packages

from robot import __version__


def read(file_name):
    with open(os.path.join(os.path.dirname(__file__), file_name)) as f:
        return f.read()


requirements = read('requirements.txt').splitlines()
str_version = '.'.join(map(str, __version__))

setup(
    name='py-robot-core',
    version=str_version,
    description='Python Library to Build Web Robots',
    long_description=read('README.rst'),
    url='http://http://git.ciag.org.br/ettore.tognoli/py-robot-core/',
    download_url='http://git.ciag.org.br/ettore.tognoli/py-robot-core/tree/%s/' % str_version,
    license='CLOSED',
    author='Éttore Leandro Tognoli',
    author_email='ettore.tognoli@ciag.org.br',
    data_files=['requirements.txt'],
    packages=find_packages(exclude=['tests', 'examples']),
    include_package_data=True,
    keywords=['Robot'],
    classifiers=[
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Development Status :: 3 - Alpha',
    ],
    install_requires=parse_requirements('requirements.txt'),
    tests_require=parse_requirements('requirements-dev.txt'),
)
