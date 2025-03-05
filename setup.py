from setuptools import setup, find_packages

setup(
    name='pyforged',
    version='0.2.0',
    packages=find_packages(),
    install_requires=[
        'antlr4-python3-runtime~=4.9.3',
        'pydantic~=2.10.6'
        'pytest~=8.3.5',
        'pytest-metadata~=3.1.1'
        ],
    entry_points={
        'console_scripts': [],
    },
    package_data={
        '': ['*.yaml', '*.ini'],
    },
    include_package_data=True,
    description='A Python project with utility functions and configuration management',
    author='DirtyWork Solutions Limited',
    author_email='pyforged@open.dirtywork.solutions',
    url='https://github.com/DirtyWork-Solutions/PyForged',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: Implementation :: CPython',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console'
        'Framework :: Pytest',
        'Framework :: Pydantic'
        'Intended Audience :: Developers',
        'Topic :: System',
        'Topic :: System :: Logging',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
        'Topic :: System :: Installation/Setup'

    ],
    python_requires='>=3.13',
)