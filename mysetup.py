from setuptools import setup

setup(
    name = 'SecureDrop',
    version = '1.0.0',
    # ....
    entry_points = {
        'console_scripts': [
            'myscript=userReg.cli:main',
        ],
    }
)
