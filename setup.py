from setuptools import setup

import hell

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name = 'hell',
    version = hell.__version__,

    description = "When you've got to debug your code.",
    long_description = long_description,
    long_description_content_type = "text/markdown",

    url = 'https://github.com/blackelk/hell',

    author = 'Constantine Parkhimovich',
    author_email = 'cparkhimovich@gmail.com',

    license = 'MIT',

    keywords = 'debug console',

    py_modules = ['hell'],

    install_requires = ['termcolor'],

    python_requires=">=3.10",

    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
