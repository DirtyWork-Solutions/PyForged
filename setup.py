from setuptools import setup, find_packages

setup(
    name='pyforged',
    version='0.2.0',
    packages=find_packages(),
    install_requires=[
        'antlr4-python3-runtime, 4.9.3',
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
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.13',
)