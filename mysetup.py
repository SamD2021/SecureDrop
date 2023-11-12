from setuptools import setup

setup(
    name = 'userReg',
    version = '1.0.0',
    # ....
    entry_points = {
        'console_scripts': [
            'SecureDrop=userReg.cli:main',
        ],
    }
)
