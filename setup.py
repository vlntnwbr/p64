from setuptools import find_packages, setup

NAME = "p64"
DESC = "Decode base64 input n times & optionally open result in chrome."
VERSION = "0.1.0"

if __name__ == "__main__":
    setup(
        name=NAME,
        description=DESC,
        version=VERSION,
        packages=find_packages(),
        include_package_data=True,
        author="Valentin Weber",
        url="https://github.com/vlntnwbr/p64",
        download_url="https://github.com/vlntnwbr/p64/archive/master.zip",
        entry_points={
            "console_scripts": [NAME + " = p46.main:main"]
        }
    )
