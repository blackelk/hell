from setuptools import setup

import hell


setup(
    name='hell',
    version=hell.__version__,

    description='Relieves pain of debug.',

    url='https://github.com/blackelk/hell',

    author='Constantine Parkhimovich',
    author_email='cparkhimovich@gmail.com',

    license='MIT',

    keywords='debug',

    py_modules=['hell'],

    install_requires=['termcolor'],

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)

