from setuptools import setup

setup(
    name='dosocs2',
    version='0.1.0',
    description='SPDX 2.0 document creation and storage',
    long_description='',
    url='https://github.com/ttgurney/dosocs2',
    author='Thomas T. Gurney',
    author_email='tgurney@unomaha.edu',
    license='Apache Software License',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Documentation',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.7',
    ],

    keywords='spdx license licenses',
    packages=['dosocs2'],
    install_requires=[
        'jinja2',
        'psycopg2',
        'python-magic',
        'docopt',
        'sqlsoup'
        ],

    package_data={
        'dosocs2': ['sql/*', 'templates/*'],
    },

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        'console_scripts': [
            'dosocs2=dosocs2.dosocs2:main',
        ],
    },

    zip_safe = False,
)
