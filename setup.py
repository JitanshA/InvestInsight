from setuptools import setup, find_packages

setup(
    name="invest_insight",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        # List your project's dependencies here.
    ],
    entry_points={
        "console_scripts": [
            # Define your project's CLI entry points here.
        ],
    },
)
