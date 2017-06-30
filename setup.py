import ast, re

from setuptools import find_packages, setup


MODULE_NAME = 'formulaic'


_version_re = re.compile(r'__version__\s+=\s+(.*)')
with open('{}/__init__.py'.format(MODULE_NAME), 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))


setup(
    name=MODULE_NAME,
    version=version,
    description='Simple [declarative] forms',
    author='Jonathan W. Zaleski',
    author_email='JonathanZaleski@gmail.com',
    url='https://github.com/jzaleski/formulaic',
    packages=find_packages(exclude=('tests', 'tests.*')),
    install_requires=['setuptools', 'six>=1.10.0'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite='pytest',
    include_package_data=True,
)
