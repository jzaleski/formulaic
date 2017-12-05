import ast, re

from setuptools import find_packages, setup


PKG_NAME = 'formulaic'


_version_re = re.compile(r'__version__\s+=\s+(.*)')
with open('{}/__init__.py'.format(PKG_NAME), 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))


setup(
    name=PKG_NAME,
    version=version,
    description='Simple [declarative] forms',
    url='https://github.com/jzaleski/{}'.format(PKG_NAME),
    author='Jonathan W. Zaleski',
    author_email='JonathanZaleski@gmail.com',
    packages=find_packages(exclude=('tests', 'tests.*')),
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Operating System :: POSIX :: Linux',
    ],
    install_requires=['setuptools', 'six>=1.10.0'],
    tests_require=['flake8>=3.5.0', 'pytest>=3.0.0'],
    setup_requires=['pytest-runner'],
    test_suite='pytest'
)
