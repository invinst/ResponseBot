from setuptools import setup, find_packages

setup(
    name='responsebot',

    # Versioning our package
    # http://python-packaging-user-guide.readthedocs.org/en/latest/distributing/#choosing-a-versioning-scheme
    #
    # Version number is required to comply with PEP 440 in order to
    # be supported in tools and libraries like pip and setuptools.
    #
    # In this time being, Semantic Versioning (http://semver.org/) is being followed using this numbering scheme:
    #
    #   MAJOR.MINOR.MAINTENANCE
    #
    # - MAJOR version when they make incompatible API changes,
    # - MINOR version when they add functionality in a backwards-compatible manner, and
    # - MAINTENANCE version when they make backwards-compatible bug fixes.
    version='0.2.3',

    description='Automatically response to any tweets mentioning you',

    url='https://github.com/invinst/ResponseBot',

    author='Invisible Institute',
    author_email='dev@invisibleinstitute.com',

    packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    install_requires=[
        'click',
        'tweepy',
        'python-dotenv',
        'python-dateutil',
        'future',
    ],

    # Settings for testing purpose
    # https://pythonhosted.org/setuptools/python3.html
    test_suite='tests',

    # Supports Python 2
    use_2to3=True,

    # Integrating with pytest
    # https://pytest.org/latest/goodpractices.html
    tests_require=['pytest'],
    setup_requires=['pytest-runner'],

    entry_points={
        'console_scripts': ['start_responsebot=responsebot.start_responsebot:main'],
    },
)
