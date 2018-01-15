from setuptools import setup
import sys

import hell


pkgdir = {'': 'python%s' % sys.version_info[0]}

setup(
    name='hell',
    version=hell.__version__,

    description="When you've got to debug your code.",

    url='https://github.com/blackelk/hell',

    author='Constantine Parkhimovich',
    author_email='cparkhimovich@gmail.com',

    license='MIT',

    keywords='debug',

    package_dir=pkgdir,
    py_modules=['hell'],

    install_requires=['termcolor'],

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)

