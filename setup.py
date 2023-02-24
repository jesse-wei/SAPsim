from setuptools import setup

setup(
    name='main',
    version='1.2',
    entry_points={
    'console_scripts': [
        'main=main:main'
    ]}
)

if __name__ == "__main__":
    setup()
