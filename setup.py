from setuptools import find_packages, setup
from package import Package

setup(
    name='ndtt',
    version='1.0',
    author="Ahmad Bello",
    author_email="ahmadagaie@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    description='A django based application for taking road theory test',
    cmdclass={
        "package": Package
    },
    scripts=['manage.py']
)