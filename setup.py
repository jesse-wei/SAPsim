try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

# Don't need to install pathlib because pathlib is in the standard library in 3.4+
install_requires: list[str] = [
    "setuptools",
    "tabulate",
    "bidict",
]
"""All required (i.e., for functionality) dependencies that are installed when running `pip install SAPsim`.

Non-functional (e.g., formatting, documentation) dependencies listed in requirements.txt."""

setup(
    name="SAPsim",
    # Check https://pypi.org/project/SAPsim/ for latest version number
    version="1.0.7",
    description="Simulation of SAP (Simple As Possible) computer programs from COMP311 (Computer Organization) @ UNC.",
    author="Jesse Wei",
    author_email="jesse@cs.unc.edu",
    url="https://github.com/jesse-wei/SAPsim",
    download_url="https://github.com/jesse-wei/SAPsim/releases",
    keywords=[
        "SAP",
        "SAPsim",
        "simple as possible",
        "UNC",
        "COMP311",
    ],
    install_requires=install_requires,
    tests_require=install_requires + ["tox", "pytest", "pytest-cov"],
    # See https://setuptools.pypa.io/en/latest/userguide/package_discovery.html
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
