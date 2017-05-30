#!/usr/bin/env python

from setuptools import setup


MODULE_NAME = 'formulaic'

module_init_file = '{}/__init__.py'.format(MODULE_NAME)
with open(module_init_file) as f:
    exec(
        compile(
            f.read(),
            module_init_file,
            'exec'
        )
    )

setup(
    name=MODULE_NAME,
    version=__version__,
    description='Simple [declarative] forms',
    author='Jonathan W. Zaleski',
    author_email='JonathanZaleski@gmail.com',
    url='https://github.com/jzaleski/formulaic',
    packages=[MODULE_NAME],
    install_requires=['setuptools', 'six>=1.10.0'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite='pytest',
    include_package_data=True,
)
