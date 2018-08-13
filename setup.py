import os

from setuptools import setup, find_packages

__version__ = (0, 0, 1)


def read(file_name):
    with open(os.path.join(os.path.dirname(__file__), file_name)) as f:
        return f.read()


requirements = filter(None, read('requirements.txt').splitlines())
requirements_dev = filter(None, read('requirements-dev.txt').splitlines())
str_version = '.'.join(map(str, __version__))

setup(
    name='ciag-robot',
    version=str_version,
    description='Python Library to Build Web Robots',
    long_description=read('README.rst'),
    url='https://github.com/OpenCIAg/py-robot',
    download_url='https://github.com/OpenCIAg/py-robot/tree/%s/' % str_version,
    license='CLOSED',
    author='Éttore Leandro Tognoli',
    author_email='ettore.tognoli@ciag.org.br',
    data_files=['requirements.txt'],
    packages=find_packages(exclude=['tests', 'examples']),
    include_package_data=True,
    keywords=['Robot', 'Web Crawler'],
    classifiers=[
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Development Status :: 3 - Alpha',
    ],
    install_requires=requirements,
    tests_require=requirements_dev,
)
